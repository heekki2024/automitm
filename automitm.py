
import subprocess
import os
import shutil
import sys
import excelFunc
import xml.etree.ElementTree as ET

#pip install openpyxl


error = 'none'

def get_apk_paths(package_name):
    try:
        
        print("get_apk_paths 함수 실행중")
        # 패키지 경로 가져오기
        package_path = subprocess.run(['adb', 'shell', 'pm', 'list', 'packages', '-f', package_name], capture_output=True, text=True, check=True)
        
        # 패키지 경로가 비어 있는지 확인
        if not package_path.stdout.strip():
            raise ValueError(f"패키지 '{package_name}'를 찾을 수 없습니다.")
            
        print(f"패키지 경로: {package_path.stdout}")
    except subprocess.CalledProcessError as e:
        print("adb 명령어 실행 중 오류가 발생했습니다.")
        print(f"오류 코드: {e.returncode}")
        print(f"오류 메시지: {e.stderr}")
        raise e
    except ValueError as e:
        print(e)
        raise e
    except Exception as e:
        print("예상치 못한 오류가 발생했습니다.")
        print(f"오류 메시지: {e}")
        raise e
  
    # 결과에서 패키지 경로 필터링
    paths = package_path.stdout.strip().split('\n')
    apk_paths = []

    print(paths)
    for path in paths:
        if package_name in path:
            # Extract the part between "package:" and "/base.apk"
            start_idx = path.find("package:") + len("package:")
            end_idx = path.find("/base.apk")
            apk_path = path[start_idx:end_idx]
            apk_paths.append(apk_path)

    print(apk_paths)

    # 각 APK 파일에 대해 'adb shell ls' 명령어를 실행하여 존재 여부를 확인합니다.
    apk_files = []
    for apk_path in apk_paths:
        # 'adb shell ls <apk_path>' 명령어 실행
        ls_result = subprocess.run(['adb', 'shell', 'ls', apk_path], capture_output=True, text=True)
        print(f"'{package_name}'의 ls 결과:")
        print(ls_result.stdout.strip())
        if ls_result.returncode != 0:
            print(f"Error: {ls_result.stderr.strip()}")
        else:
            # ls 결과에서 .apk 파일만 필터링
            files = ls_result.stdout.strip().split('\n')
            for file in files:
                if file.endswith('.apk'):
                    full_path = f"{apk_path}/{file}"
                    apk_files.append(full_path)
    return apk_files

def create_package_directory(package_name):
    try:
        # 첫 사용전 testing폴더 경로 바꾸기
        # base_dir = "C:\\Users\\BSJ\\Desktop\\testing"
        base_dir = "C:\\Users\\xten\\Desktop\\testing"

        package_dir = os.path.join(base_dir, package_name)
        os.makedirs(package_dir, exist_ok=True)
        print(f"{package_dir} 폴더가 생성되었습니다.")
        return package_dir
    except Exception as e:
        print(f"{package_dir} 폴더 생성 중 오류 발생: {e}")
        raise e

def pull_apks(apk_files, package_dir, package_name):
    for apk_file in apk_files:
        try:
            print(f"{package_name} 패키지의 APK 파일을 추출합니다...")
            subprocess.run(['adb', 'pull', apk_file, package_dir], check=True)
            print("APK 파일 추출이 완료되었습니다.")
        except subprocess.CalledProcessError as e:
            print(f"파일 추출 실패")
            raise e
        
def merge_apks(package_dir):
    try:
        print("apk들을 merge 합니다...")
        subprocess.run(['java', '-jar', r'C:\Windows\APKEditor-1.3.8.jar', 'm', '-i', package_dir , '-o', ], check=True)


def decompile_base_apk(package_dir):
    try:
        base_apk_path = os.path.join(package_dir, "base.apk")
        print(base_apk_path)
        output_path = f"{package_dir}2"
        print(output_path)
        subprocess.run(['java', '-jar', 'C:\\Windows\\apktool.jar', 'd', '-f', '-s', base_apk_path, '-o', output_path], check=True)
        print(f"base.apk 디컴파일 완료: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"{base_apk_path} 디컴파일 중 오류 발생: {e}")
        raise e
    except Exception as e:
        print(f"{base_apk_path} 파일을 찾을 수 없습니다.")
        raise e

def decompile_base_apk_with_r(package_dir):
    try:
        base_apk_path = os.path.join(package_dir, "base.apk")
        print(base_apk_path)
        output_path = f"{package_dir}2"
        print(output_path)
        subprocess.run(['java', '-jar', 'C:\\Windows\\apktool.jar', 'd', '-f', '-r' '-s', base_apk_path, '-o', output_path], check=True)
        print(f"base.apk 디컴파일 완료: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"{base_apk_path} 디컴파일 중 오류 발생: {e}")
        raise e
    except Exception as e:
        print(f"{base_apk_path} 파일을 찾을 수 없습니다.")
        raise e

def check_AndroidManifest(output_path):
    try:
        AndroidManifest_path = os.path.join(output_path, "AndroidManifest.xml")

        # AndroidManifest.xml 파일 파싱
        tree = ET.parse(AndroidManifest_path)
        root = tree.getroot()

        # Android 네임스페이스 정의
        android_ns = 'http://schemas.android.com/apk/res/android'

        # 네임스페이스 등록
        ET.register_namespace('android', android_ns)

        #<application> 태그 찾기
        application_tag = root.find('application')

        if application_tag is None:
            raise Exception("<application> 태그를 찾을 수 없습니다.")
            
        # android:networkSecurityConfig 옵션 확인
        networkSecurityConfig_value = application_tag.get(f'{{{android_ns}}}networkSecurityConfig')
        if networkSecurityConfig_value:
            print(f"android:networkSecurityConfig 옵션이 있습니다. 값: {networkSecurityConfig_value}")

            network_Security_Config_name = os.path.basename(networkSecurityConfig_value)
            print(f"가장 하단 디렉토리 또는 파일 이름: {network_Security_Config_name}")

            tree.write(AndroidManifest_path, encoding='utf-8', xml_declaration=True)

            return True, network_Security_Config_name

        else:
            print("android:networkSecurityConfig 옵션이 없습니다.")

            # android:usesCleartextTraffic 옵션 확인
            usesCleartextTraffic_value = application_tag.get(f'{{{android_ns}}}usesCleartextTraffic')
            if usesCleartextTraffic_value is not None:
                print(f"android:usesCleartextTraffic 옵션이 있습니다. 값: {usesCleartextTraffic_value}")

                del application_tag.attrib[f'{{{android_ns}}}usesCleartextTraffic']
                print("android:usesCleartextTraffic 옵션이 제거되었습니다.")

            else:
                print("android:usesCleartextTraffic 옵션이 없습니다.")

            # android:networkSecurityConfig 옵션 추가
            application_tag.set(f'{{{android_ns}}}networkSecurityConfig', '@xml/network_security_config')
            print("android:networkSecurityConfig 옵션이 추가되었습니다.")

            tree.write(AndroidManifest_path, encoding='utf-8', xml_declaration=True)

            return False




    except ET.ParseError as e:
        print(f"XML 파싱 오류: {e}")
    except FileNotFoundError as e:
        print(f"파일을 찾을 수 없습니다: {e}")
    except Exception as e:
        print(f"알 수 없는 오류: {e}")


        if not os.path.exists(AndroidManifest_path):
            raise FileNotFoundError(f"{AndroidManifest_path} 파일을 찾을 수 없습니다.")

        
            


def copy_network_security_config(output_path):
    try:
        network_security_config_dir = os.path.join(output_path, "res", "xml")

        #변조된 파일 경로
        # modified_network_security_config_path = r"C:\Users\BSJ\Desktop\network_security_config\network_security_config.xml"
        modified_network_security_config_path = r"C:\Users\xten\Desktop\network_security_config\network_security_config.xml"

        # 파일 존재 여부 확인
        if not os.path.exists(network_security_config_dir):
            raise FileNotFoundError(f"res\xml 폴더를 찾을 수 없습니다.")
        
        if not os.path.exists(modified_network_security_config_path):
            raise FileNotFoundError(f"변조된 network_security_config 파일을 찾을 수 없습니다.")

        
        shutil.copy2(modified_network_security_config_path, network_security_config_dir)
        print(f"network_security_config.xml 파일이 {network_security_config_dir}로 복사되었습니다.")
    except PermissionError as e:
        print(f"{modified_network_security_config_path} 파일 복사 중 오류 발생: {e}")
        raise e
    except FileNotFoundError as e:
        print(e)
        raise e
    except Exception as e:
        print("유효하지 않은 output_path입니다.")
        raise e

def change_network_security_config_with_r(output_path):
    try:
        network_security_config_path = os.path.join(output_path, "res", "xml", "network_security_config.xml")

        #변조된 파일 경로
        # modified_network_security_config_path = r"C:\Users\BSJ\Desktop\network_security_config_without_r\network_security_config.xml"
        modified_network_security_config_path = r"C:\Users\xten\Desktop\network_security_config_with_r\network_security_config.xml"

        # 파일 존재 여부 확인
        if not os.path.exists(network_security_config_path):
            raise FileNotFoundError(f"{network_security_config_path} 파일을 찾을 수 없습니다.")
        

        if not os.path.exists(modified_network_security_config_path):
            raise FileNotFoundError(f"{modified_network_security_config_path} 파일을 찾을 수 없습니다.")


        shutil.copy(modified_network_security_config_path, network_security_config_path)
        print(f"network_security_config.xml 파일이 교체되었습니다")
    except PermissionError as e:
        print(f"{modified_network_security_config_path} 파일 복사 중 오류 발생: {e}")
        raise e
    except FileNotFoundError as e:
        print(e)
        raise e
    except Exception as e:
        print("유효하지 않은 output_path입니다.")
        raise e


def remove_decompile_fail_output_path(output_path):
    try:
        os.remove(output_path)
    except Exception as e:
        print("알수 없는 이유로 폴더 삭제에 실패하였습니다")
        raise e
        

def recompile_base_apk(output_path, package_dir):
    try:
        newbase_path = os.path.join(package_dir, "newbase.apk")
        subprocess.run(['java', '-jar', 'C:\\Windows\\apktool.jar', 'b', output_path, '-o', newbase_path], check=True)
        print("리컴파일에 성공하였습니다.")
    except subprocess.CalledProcessError as e:
        print("리컴파일에 실패했습니다. 프로그램을 종료합니다.")

        global error
        error = '리컴파일 실패'

        raise e
    except Exception as e:
        print("디컴파일된 apk 파일 경로를 찾지 못하였습니다. 프로그램을 종료합니다")

        # global error
        # error = '리컴파일 실패'

        raise e
    # 리컴파일 완료 후 base.apk 파일 삭제
    try:
        base_apk_path = os.path.join(package_dir, "base.apk")
        os.remove(base_apk_path)
        print(f"{base_apk_path} 파일이 삭제되었습니다.")
    except FileNotFoundError as e:
        print(f"{base_apk_path} 파일을 찾지 못하였습니다: {e}")
        raise e
    except Exception as e:
        print(f"{base_apk_path} 파일 삭제 중 오류 발생: {e}")
        raise e


def sign_apks(package_dir):
    for file in os.listdir(package_dir):
        if file.endswith(".apk"):
            apk_path = os.path.join(package_dir, file)
            try:
                subprocess.run(['java', '-jar', 'C:\\Windows\\uber-apk-signer-1.3.0.jar', '-a', apk_path, '--allowResign'], check=True)
                print(f"{file} 파일 서명 완료.")
            except subprocess.CalledProcessError as e:
                print(f"{file} 파일 서명 실패.")

                global error
                error = '서명 실패'
        

                raise e

def install_signed_apks(package_name, package_dir):
    # 기존 패키지 삭제
    try:
        subprocess.run(['adb', 'uninstall', package_name], check=True)
        print(f"{package_name} 패키지 삭제 완료.")
    except subprocess.CalledProcessError as e:
        print(f"{package_name} 패키지 삭제 실패.")
        raise e
    # 서명된 APK 파일 설치
    apk_files_to_install = []
    for file in os.listdir(package_dir):
        if file.endswith("-aligned-debugSigned.apk") and not file.endswith(".idsig"):
            apk_files_to_install.append(os.path.join(package_dir, file))
    try:
        subprocess.run(['adb', 'install-multiple'] + apk_files_to_install, check=True)
        print("서명된 APK 파일 설치 완료.")
    except subprocess.CalledProcessError as e:
        print("서명된 APK 파일 설치 실패.")

        global error
        error = '설치 실패'

        raise e
    except Exception as e:
        print("설치할 서명된 APK 파일을 찾을 수 없습니다.")

        # global error
        # error = '설치 실패'

        raise e


def main():

    global error
    error = 'none'    
    startPoint, endPoint, ws = excelFunc.excelStartPoint()
    
    for row in range(startPoint, endPoint + 1, 1):
        try: 
            print("\n\n\n\n-----FULL AUTO MITM 실행중-----\n\n\n\n")

            app_name = ws[f'A{row}'].value
            package_name = ws[f'B{row}'].value

            # APK 경로 가져오기
            apk_files = get_apk_paths(package_name)

            #APK를 담을 폴더 생성
            package_dir = create_package_directory(package_name)

            # APK 파일 추출
            pull_apks(apk_files, package_dir, package_name)

            # base.apk 파일 디컴파일
            output_path = decompile_base_apk(package_dir)

            have_networkSecurityConfig,network_Security_Config_name = check_AndroidManifest(output_path)

            if have_networkSecurityConfig == True:
                
            elif have_networkSecurityConfig == False:
                # network_security_config.xml 파일 교체
                copy_network_security_config(output_path)

                recompile_base_apk(output_path, package_dir)



            try:
                # base.apk 파일 리컴파일
                recompile_base_apk(output_path, package_dir)
            except:
                print("--------리컴파일 실패-------- \n디컴파일 된 폴더 삭제 후\n apktool d 의 -r 옵션 없이 재디컴파일")
                remove_decompile_fail_output_path(output_path)

                output_path = decompile_base_apk_with_r(package_dir)

                change_network_security_config_with_r(output_path)

                recompile_base_apk(output_path, package_dir)


            # APK 파일 서명
            sign_apks(package_dir)

            # 서명된 APK 파일 설치
            install_signed_apks(package_name, package_dir)

            
            excelFunc.excelEndPoint(startPoint, endPoint, app_name, None, None, None)
            print("결과는 엑셀으로")
        except Exception as e:
            print("-------------오류 발생-------------")
            result = '아니오'
            
            excelFunc.excelEndPoint(startPoint, endPoint, app_name, result, error, str(e))
            # subprocess.run(['adb', 'uninstall', package_name], check=True)
            print(f"{package_name} 패키지 삭제 완료.")


    sys.exit(0)  # 프로그램 종료


if __name__ == "__main__":
    main()
