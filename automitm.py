
from multiprocessing import Value
import subprocess
import os
import shutil
import sys
import excelFunc
import xml.etree.ElementTree as ET
from tkinter import Tk, filedialog, messagebox



CONFIG_FILE = 'config.ini'

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
        global error
        error = '패키지 발견 실패'        
        raise e
    except ValueError as e:
        print(e)
        error = '패키지 발견 실패'        

        raise e
    except Exception as e:
        print("예상치 못한 오류가 발생했습니다.")
        print(f"오류 메시지: {e}")
        error = '패키지 발견 실패'        

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

def create_package_directory(package_name, base_dir):
    try:

        package_dir = os.path.join(base_dir, package_name)
        os.makedirs(package_dir, exist_ok=True)
        print(f"{package_dir} 폴더가 생성되었습니다.")
        return package_dir
    except Exception as e:
        global error
        error = f"{package_dir} 폴더 생성 중 오류 발생: {e}"
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
            global error
            error = '파일 추출 실패'        
            raise e
        

def merge_apks(package_dir, base_dir):
    try:

        merged_apk_path = os.path.join(f"{package_dir}2", "merged.apk")

        print("apk들을 Merge 합니다...")
        subprocess.run(['java', '-jar', r'C:\Windows\APKEditor-1.3.9.jar', 'm', '-i', package_dir , '-o', merged_apk_path], check=True)
        print("MERGE가 완료되었습니다.")
        return merged_apk_path
    except subprocess.CalledProcessError as e:
        base_name = os.path.basename(base_dir)
        print(f"파일 MERGE 실패.\nBase폴더인 {base_name}에 이미 merge된 파일이 있는지 확인하세요")
        global error
        error = '파일 MERGE 실패'        
        raise e

def decompile_merged_apk(merged_apk_path, package_dir):
    try:
        # base_apk_path = os.path.join(package_dir, "base.apk")
        # print(base_apk_path)
        print("r 옵션 없이 디컴파일 하는 중 ...")
        output_path = f"{package_dir}3"
        # print(output_path)
        subprocess.run(['java', '-jar', 'C:\\Windows\\apktool.jar', 'd', '-f', '-s', merged_apk_path, '-o', output_path], check=True)
        print(f"merged 디컴파일 완료: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"{merged_apk_path} 디컴파일 중 오류 발생: {e}")
        global error
        error = '디컴파일 실패'
        raise e
    except Exception as e:
        error = '디컴파일 실패'
        print(f"{merged_apk_path} 파일을 찾을 수 없습니다.")
        raise e

def decompile_merged_apk_with_r(merged_apk_path, package_dir):
    try:
        # base_apk_path = os.path.join(package_dir, "base.apk")
        # print(base_apk_path)
        print("r 옵션이 있는 상태로 디컴파일 하는 중 ...")
        output_path = f"{package_dir}3"
        # print(output_path)
        subprocess.run(['java', '-jar', 'C:\\Windows\\apktool.jar', 'd', '-f', '-r', '-s', merged_apk_path, '-o', output_path], check=True)
        print(f"merged.apk 디컴파일 완료: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"{merged_apk_path} 디컴파일 중 오류 발생: {e}")
        global error
        error = '디컴파일 실패 with r'        
        raise e
    except Exception as e:
        print(f"{merged_apk_path} 파일을 찾을 수 없습니다.")
        error = '디컴파일 실패 with r'        
        raise e
    
    

def decompile_base_apk(package_dir):
    try:
        base_apk_path = os.path.join(package_dir, "base.apk")
        print(base_apk_path)
        
        print("r 옵션 없이 디컴파일 하는 중 ...")
        output_path = f"{package_dir}3"
        # print(output_path)
        subprocess.run(['java', '-jar', 'C:\\Windows\\apktool.jar', 'd', '-f', '-s', base_apk_path, '-o', output_path], check=True)
        print(f"base.apk 디컴파일 완료: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"{base_apk_path} 디컴파일 중 오류 발생: {e}")
        global error
        error = '디컴파일 실패'
        raise e
    except Exception as e:
        error = '디컴파일 실패'
        print(f"{base_apk_path} 파일을 찾을 수 없습니다.")
        raise e


def decompile_base_apk_with_r(package_dir):
    try:
        base_apk_path = os.path.join(package_dir, "base.apk")
        print(base_apk_path)
        
        print("r 옵션이 있는 상태로 디컴파일 하는 중 ...")
        output_path = f"{package_dir}3"
        # print(output_path)
        subprocess.run(['java', '-jar', 'C:\\Windows\\apktool.jar', 'd', '-f', 'r', '-s', base_apk_path, '-o', output_path], check=True)
        print(f"base.apk 디컴파일 완료: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"{base_apk_path} 디컴파일 중 오류 발생: {e}")
        global error
        error = '디컴파일 실패'
        raise e
    except Exception as e:
        error = '디컴파일 실패'
        print(f"{base_apk_path} 파일을 찾을 수 없습니다.")
        raise e







def check_AndroidManifest(output_path):
    try:
        AndroidManifest_path = os.path.join(output_path, "AndroidManifest.xml")

        if not os.path.exists(AndroidManifest_path):
            raise FileNotFoundError(f"{AndroidManifest_path} 파일을 찾을 수 없습니다.")

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
            print("AndroidManifest.xml 저장 완료")
            return False,None


    except ET.ParseError as e:
        print(f"XML 파싱 오류: {e}")
        raise e
    
    except FileNotFoundError as e:
        print(f"파일을 찾을 수 없습니다: {e}")
        raise e

    except Exception as e:
        print(f"알 수 없는 오류: {e}")
        raise e




def modify_network_security_config(network_Security_Config_name, output_path):
    try:
        network_Security_Config_name_path = os.path.join(output_path, "res", 'xml', f"{network_Security_Config_name}.xml")

        # network_security_config.xml 파일 파싱
        tree = ET.parse(network_Security_Config_name_path)
        root = tree.getroot()

        # 새로운 base-config 태그 내용
        new_base_config = ET.Element('base-config', {'cleartextTrafficPermitted': 'true'})
        trust_anchors = ET.SubElement(new_base_config, 'trust-anchors')
        ET.SubElement(trust_anchors, 'certificates', {'src': 'system'})
        ET.SubElement(trust_anchors, 'certificates', {'src': 'user'})

        # 기존 base-config 태그 찾기
        base_config = root.find('base-config')

        if base_config is not None:
            # base-config 태그와 내용 제거
            root.remove(base_config)

        # 새로운 base-config 태그 추가
        root.append(new_base_config)

        # 변경된 내용 저장
        tree.write(network_Security_Config_name_path, encoding='utf-8', xml_declaration=True)
        print(f"{network_Security_Config_name_path} 파일이 수정되었습니다.")

    except ET.ParseError as e:
        print(f"XML 파싱 오류: {e}")
        raise e
    except FileNotFoundError as e:
        print(f"파일을 찾을 수 없습니다: {e}")
        raise e
    except Exception as e:
        print(f"알 수 없는 오류: {e}")
        raise e

def copy_network_security_config(output_path, modified_network_security_config_path):
    try:
        network_security_config_dir = os.path.join(output_path, "res", "xml")

        # 파일 존재 여부 확인
        if not os.path.exists(network_security_config_dir):
            global error
            error = 'copy_network_security_config 복사 및 붙여넣기 실패'
            raise FileNotFoundError(r"res\xml 폴더를 찾을 수 없습니다.")
        
        
        if not os.path.exists(modified_network_security_config_path):
            error = 'copy_network_security_config 복사 및 붙여넣기 실패'
            raise FileNotFoundError(f"변조된 network_security_config 파일을 찾을 수 없습니다.")

        
        shutil.copy2(modified_network_security_config_path, network_security_config_dir)
        print(f"network_security_config.xml 파일이 {network_security_config_dir}로 복사되었습니다.")
    except PermissionError as e:
        error = 'copy_network_security_config 복사 및 붙여넣기 실패'
        print(f"{modified_network_security_config_path} 파일 복사 중 오류 발생: {e}")
        raise e
    except FileNotFoundError as e:
        error = 'copy_network_security_config 복사 및 붙여넣기 실패'
        print(e)
        raise e
    except Exception as e:
        error = 'copy_network_security_config 복사 및 붙여넣기 실패'
        print("유효하지 않은 output_path입니다.")
        raise e

def copy_network_security_config_with_r(output_path, modified_network_security_config_with_r_path):
    try:
        network_security_config_dir = os.path.join(output_path, "res", "xml")


        # 파일 존재 여부 확인
        if not os.path.exists(network_security_config_dir):
            global error
            error = 'copy_network_security_config_with_r 복사 및 붙여넣기 실패'
            raise FileNotFoundError(r"res\xml 폴더를 찾을 수 없습니다.")
        
        if not os.path.exists(modified_network_security_config_with_r_path):
            error = 'copy_network_security_config_with_r 복사 및 붙여넣기 실패'
            raise FileNotFoundError(f"변조된 network_security_config 파일을 찾을 수 없습니다.")
 
        shutil.copy2(modified_network_security_config_with_r_path, network_security_config_dir)
        print(f"network_security_config.xml 파일이 {network_security_config_dir}로 복사되었습니다.")
    except PermissionError as e:
        error = 'copy_network_security_config_with_r 복사 및 붙여넣기 실패'
        print(f"{modified_network_security_config_with_r_path} 파일 복사 중 오류 발생: {e}")
        raise e
    except FileNotFoundError as e:
        error = 'copy_network_security_config_with_r 복사 및 붙여넣기 실패'
        print(e)
        raise e
    except Exception as e:
        error = 'copy_network_security_config_with_r 복사 및 붙여넣기 실패'
        print("유효하지 않은 output_path입니다.")
        raise e

        
def remove_build_fail_output_path(output_path):
    try:
        if os.path.exists(output_path):
            for root, dirs, files in os.walk(output_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(output_path)
            print(f"{output_path} 폴더가 삭제되었습니다.")
        else:
            print(f"{output_path} 폴더가 존재하지 않습니다.")
    except PermissionError as e:
        print(f"{output_path} 폴더 삭제 중 권한 오류 발생: {e}")
        global error
        error = '빌드 실패 폴더 삭제 실패'
        raise e
    except FileNotFoundError as e:
        print(f"{output_path} 폴더를 찾을 수 없습니다: {e}")
        error = '빌드 실패 폴더 삭제 실패'

        raise e
    except Exception as e:
        print("알 수 없는 이유로 폴더 삭제에 실패하였습니다")
        error = '빌드 실패 폴더 삭제 실패'

        raise e

def recompile_merged_apk(output_path, package_dir):
    try:
        new_merged_path = os.path.join(package_dir, "new_merged.apk")
        subprocess.run(['java', '-jar', 'C:\\Windows\\apktool.jar', 'b', output_path, '-o', new_merged_path], check=True)
        print("리컴파일에 성공하였습니다.")
    except subprocess.CalledProcessError:
        print("리컴파일에 실패했습니다")

        global error
        error = '리컴파일 실패'

        raise
    except Exception:
        print("디컴파일된 apk 파일 경로를 찾지 못하였습니다. 프로그램을 종료합니다")


        error = '리컴파일 실패'

        raise
    
def recompile_base_apk(output_path, package_dir):
    try:
        new_base_path = os.path.join(package_dir, "new_base.apk")
        subprocess.run(['java', '-jar', 'C:\\Windows\\apktool.jar', 'b', output_path, '-o', new_base_path], check=True)
        print("리컴파일에 성공하였습니다.")
    except subprocess.CalledProcessError as e:
        print("리컴파일에 실패했습니다")

        global error
        error = '리컴파일 실패'

        raise e
    except Exception as e:
        print("디컴파일된 apk 파일 경로를 찾지 못하였습니다. 프로그램을 종료합니다")


        error = '리컴파일 실패'

        raise e



def sign_merged_apks(package_dir):
    # for file in os.listdir(package_dir):
    #     if file.endswith(".apk"):
            built_apk_path = os.path.join(package_dir, "new_merged.apk")
            try:
                subprocess.run(['java', '-jar', 'C:\\Windows\\uber-apk-signer-1.3.0.jar', '-a', built_apk_path], check=True)
                print(f"new_merged.apk 파일 서명 완료.")
            except subprocess.CalledProcessError as e:
                print(f"new_merged.apk 파일 서명 실패.")

                global error
                error = '서명 실패'
        
                raise e

def sign_splited_apks(package_dir):
    for file in os.listdir(package_dir):
        if file.endswith(".apk") and file != "base.apk":
            built_apk_path = os.path.join(package_dir, file)
            try:
                subprocess.run(['java', '-jar', 'C:\\Windows\\uber-apk-signer-1.3.0.jar', '-a', built_apk_path, '--allowResign'], check=True)
                print(f"{file} 서명 완료.")
            except subprocess.CalledProcessError as e:
                print(f"{file} 서명 실패")
                global error
                error = '서명 실패'
        
                raise e

def remove_app(package_name):
    # 기존 패키지 삭제
    try:
        subprocess.run(['adb', 'uninstall', package_name], check=True)
        print(f"{package_name} 패키지 삭제 완료.")
    except subprocess.CalledProcessError as e:
        print(f"{package_name} 패키지 삭제 실패.")
        global error
        error = '삭제 실패'

        raise e    

def install_signed_merged_apk(package_dir):

    # 서명된 APK 파일 설치
    apk_files_to_install = []
    for file in os.listdir(package_dir):
        if file.endswith("-aligned-debugSigned.apk") and not file.endswith(".idsig"):
            apk_files_to_install.append(os.path.join(package_dir, file))
    try:
        subprocess.run(['adb', 'install'] + apk_files_to_install, check=True)
        print("서명된 APK 파일 설치 완료.")
    except subprocess.CalledProcessError as install_error:
        print("서명된 APK 파일 설치 실패.")
        print("base apk만 변조 진행")

        global error
        # error = '설치 실패'
        
        
        raise install_error
    
    
    except Exception as e:
        print("설치할 서명된 APK 파일을 찾을 수 없습니다.")


        error = '설치 실패'

        raise e

def install_signed_apks(package_dir):

    # 서명된 APK 파일 설치
    apk_files_to_install = []
    for file in os.listdir(package_dir):
        if file.endswith("-aligned-debugSigned.apk") and not file.endswith(".idsig"):
            apk_files_to_install.append(os.path.join(package_dir, file))
    try:
        subprocess.run(['adb', 'install-multiple'] + apk_files_to_install, check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        print("서명된 APK 파일 설치 완료.")
    except subprocess.CalledProcessError as e:
        print("서명된 APK 파일 설치 실패.")
        global error
        error = '설치 실패'

        raise e
    except Exception as e:
        print("설치할 서명된 APK 파일을 찾을 수 없습니다.")


        error = '설치 실패'

        raise e


error = None
def main():

    config = excelFunc.load_config()

    (excel_input_path,
     excel_output_path, 
     base_dir, 
     network_security_config_path, 
     network_security_config_with_r_path) = excelFunc.initialize_paths(config)

    (startPoint,
     endPoint, 
     ws, 
     excel_input_path,
     excel_output_path,
     base_dir,
     network_security_config_path,
     network_security_config_with_r_path
     ) = excelFunc.excelStartPoint(excel_input_path, excel_output_path, base_dir, network_security_config_path, network_security_config_with_r_path)
                          

    global error
    for row in range(startPoint, endPoint + 1, 1):
        try: 
            print("\n|------------FULL AUTO MITM 실행중------------|\n")

            error = 'none'   

            ranking = ws[f'A{row}'].value if ws[f'A{row}'].value is not None else ''
            category = ws[f'B{row}'].value if ws[f'B{row}'].value is not None else ''
            app_name = ws[f'C{row}'].value if ws[f'C{row}'].value is not None else ''
            package_name = ws[f'D{row}'].value if ws[f'D{row}'].value is not None else ''
            totaluser = ws[f'E{row}'].value if ws[f'E{row}'].value is not None else ''
            totaltime = ws[f'F{row}'].value if ws[f'F{row}'].value is not None else ''
            monthuser = ws[f'G{row}'].value if ws[f'G{row}'].value is not None else ''

            business_name = ws[f'L{row}'].value if ws[f'L{row}'].value is not None else ''
            order = ws [f'M{row}'].value if ws[f'M{row}'].value is not None else ''

            # 값 검증
            if not app_name:
                raise ValueError(f"행 {row}에서 app_name이 비어있거나 유효하지 않습니다.")
            if not package_name:
                raise ValueError(f"행 {row}에서 package_name이 비어있거나 유효하지 않습니다.")

            # APK 경로 가져오기
            apk_files = get_apk_paths(package_name)

            #APK를 담을 폴더 생성
            package_dir = create_package_directory(package_name, base_dir)

            # APK 파일 추출
            pull_apks(apk_files, package_dir, package_name)
            try: 
                # APK 파일들 MERGE
                merged_apk_path = merge_apks(package_dir, base_dir)
                
                
                # base.apk 파일 디컴파일
                try:
                    output_path = decompile_merged_apk(merged_apk_path, package_dir)
                    
                    have_networkSecurityConfig,network_Security_Config_name = check_AndroidManifest(output_path)

                    recompile_done = False  # recompile_merged_apk가 실행되었는지 확인하는 플래그


                    if have_networkSecurityConfig == True:
                        #network_security_config.xml 내용 수정
                        modify_network_security_config(network_Security_Config_name, output_path)

                        
                        try:
                            recompile_merged_apk(output_path, package_dir)

                            recompile_done = True  # 성공적으로 실행되면 플래그를 True로 설정

                        except Exception:
                            print("\n--------리컴파일 실패-------- \n디컴파일 된 폴더 삭제 후\n apktool d 의 -r 옵션을 추가해 재디컴파일\n")

                            remove_build_fail_output_path(output_path)
                            
                            raise RuntimeError



                    elif have_networkSecurityConfig == False:
                        # network_security_config.xml 파일 교체
                        copy_network_security_config(output_path, network_security_config_path)
                        try:
                            recompile_merged_apk(output_path, package_dir)

                            recompile_done = True  # 성공적으로 실행되면 플래그를 True로 설정

                        except Exception:
                            print("\n--------리컴파일 실패-------- \n디컴파일 된 폴더 삭제 후\n apktool d 의 -r 옵션을 추가해 재디컴파일\n")

                            remove_build_fail_output_path(output_path)

                            raise RuntimeError



                except Exception as e:

                    if not isinstance(e, RuntimeError):
                        print("\n--------에러 발생--------\n")

                    output_path = decompile_merged_apk_with_r(merged_apk_path, package_dir)

                    copy_network_security_config_with_r(output_path, network_security_config_with_r_path)

        

        
                    # APK 파일 서명

                try:
                    if not recompile_done:  # recompile_merged_apk가 아직 실행되지 않은 경우에만 실행
                        recompile_merged_apk(output_path, package_dir)

                    sign_merged_apks(package_dir)

                    #안드로이드 내 앱 삭제
                    remove_app(package_name)

                    # 서명된 APK 파일 설치
                    install_signed_merged_apk(package_dir)
                except Exception as e:

                    print(f"{package_dir}2 폴더 제거")
                    print(f"{package_dir}3 폴더 제거")

                    package_dir2 = f"{package_dir}2"
                    package_dir3 = f"{package_dir}3"
                    try:
                        shutil.rmtree(package_dir2)
                    except Exception as e:
                        print(f"Error occurred while removing {package_dir2}: {e}")

                    try:
                        shutil.rmtree(package_dir3)
                    except Exception as e:
                        print(f"Error occurred while removing {package_dir3}: {e}")


                    for filename in os.listdir(package_dir):
                        if 'new_merged' in filename:
                            file_path = os.path.join(package_dir, filename)
                            os.remove(file_path)
                            print(f"Deleted: {file_path}")
                


                    try:
                        output_path = decompile_base_apk(package_dir)

                        have_networkSecurityConfig,network_Security_Config_name = check_AndroidManifest(output_path)

                        recompile_done = False  # recompile_merged_apk가 실행되었는지 확인하는 플래그

                        if have_networkSecurityConfig == True:
                            #network_security_config.xml 내용 수정
                            modify_network_security_config(network_Security_Config_name, output_path)

                            try:
                                recompile_base_apk(output_path, package_dir)

                                recompile_done = True  # 성공적으로 실행되면 플래그를 True로 설정
                                
                            except:

                                print("\n--------리컴파일 실패-------- \n디컴파일 된 폴더 삭제 후\n apktool d 의 -r 옵션을 추가해 재디컴파일\n")

                                remove_build_fail_output_path(output_path)

                                raise RuntimeError

                        elif have_networkSecurityConfig == False:
                            # network_security_config.xml 파일 교체
                            copy_network_security_config(output_path, network_security_config_path)
                            try:
                                recompile_base_apk(output_path, package_dir)

                                recompile_done = True  # 성공적으로 실행되면 플래그를 True로 설정


                            except:
                                print("\n--------리컴파일 실패-------- \n디컴파일 된 폴더 삭제 후\n apktool d 의 -r 옵션을 추가해 재디컴파일\n")

                                remove_build_fail_output_path(output_path)

                                raise RuntimeError

                                
                    except Exception as e:

                        if not isinstance(e, RuntimeError):
                            print("\n--------디컴파일 실패--------\n")

                        output_path = decompile_base_apk_with_r(package_dir)

                        copy_network_security_config_with_r(output_path, network_security_config_with_r_path)

                    try:
                        if not recompile_done:  # recompile_merged_apk가 아직 실행되지 않은 경우에만 실행
                            recompile_base_apk(output_path, package_dir)

                        sign_splited_apks(package_dir)

                        # 서명된 APK 파일 설치
                        install_signed_apks(package_dir)
                    except Exception as e:
                        print("최종 설치 실패")

                        raise e
                        # pass

            except:
                    try:
                        
                        output_path = decompile_base_apk(package_dir)

                        have_networkSecurityConfig,network_Security_Config_name = check_AndroidManifest(output_path)

                        recompile_done = False  # recompile_merged_apk가 실행되었는지 확인하는 플래그

                        if have_networkSecurityConfig == True:
                            #network_security_config.xml 내용 수정
                            modify_network_security_config(network_Security_Config_name, output_path)

                            try:
                                recompile_base_apk(output_path, package_dir)

                                recompile_done = True  # 성공적으로 실행되면 플래그를 True로 설정
                                
                            except:

                                print("\n--------리컴파일 실패-------- \n디컴파일 된 폴더 삭제 후\n apktool d 의 -r 옵션을 추가해 재디컴파일\n")

                                remove_build_fail_output_path(output_path)

                                raise RuntimeError

                        elif have_networkSecurityConfig == False:
                            # network_security_config.xml 파일 교체
                            copy_network_security_config(output_path, network_security_config_path)
                            try:
                                recompile_base_apk(output_path, package_dir)

                                recompile_done = True  # 성공적으로 실행되면 플래그를 True로 설정


                            except:
                                print("\n--------리컴파일 실패-------- \n디컴파일 된 폴더 삭제 후\n apktool d 의 -r 옵션을 추가해 재디컴파일\n")

                                remove_build_fail_output_path(output_path)

                                raise RuntimeError

                                
                    except Exception as e:

                        if not isinstance(e, RuntimeError):
                            print("\n--------디컴파일 실패--------\n")

                        output_path = decompile_base_apk_with_r(package_dir)

                        copy_network_security_config_with_r(output_path, network_security_config_with_r_path)

                    try:
                        if not recompile_done:  # recompile_merged_apk가 아직 실행되지 않은 경우에만 실행
                            recompile_base_apk(output_path, package_dir)

                        sign_splited_apks(package_dir)

                        # 서명된 APK 파일 설치
                        install_signed_apks(package_dir)
                    except Exception as e:
                        print("최종 설치 실패")

                        raise e
                        # pass
                    

            excelFunc.excelEndPoint(excel_output_path, ranking, category, app_name, package_name, totaluser, totaltime, monthuser, None, None, None, business_name, order)
            print(f"결과는 output엑셀인 {excel_output_path}에서 확인")
        except subprocess.CalledProcessError as e: 
            print("\n-------------오류 발생-------------\n")
            print(e)
            result = '아니오'
            
            excelFunc.excelEndPoint(excel_output_path, ranking, category, app_name, package_name, totaluser, totaltime, monthuser, result, error, str(e.stderr), business_name, order)

            
        except Exception as e:
            print("\n-------------오류 발생-------------\n")
            print(e)
            result = '아니오'
            
            excelFunc.excelEndPoint(excel_output_path, ranking, category, app_name, package_name, totaluser, totaltime, monthuser, result, error, str(e), business_name, order)


    sys.exit(0)  # 프로그램 종료


if __name__ == "__main__":
    main()
    