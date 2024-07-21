
import subprocess
import os
import shutil
import sys

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
        base_dir = "C:\\Users\\BSJ\\Desktop\\testing"
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
            print("testing")
            print(f"{package_name} 패키지의 APK 파일을 추출합니다...")
            subprocess.run(['adb', 'pull', apk_file, package_dir], check=True)
            print("APK 파일 추출이 완료되었습니다.")
        except subprocess.CalledProcessError as e:
            print(f"파일 추출 실패")
            raise e

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

def change_network_security_config(output_path):
    try:
        res_xml_path = os.path.join(output_path, "res", "xml")
        network_security_config_path = "C:\\Users\\BSJ\\Desktop\\network_security_config\\network_security_config.xml"
        # 파일 존재 여부 확인
        if not os.path.exists(network_security_config_path):
            raise FileNotFoundError(f"{network_security_config_path} 파일을 찾을 수 없습니다.")
        shutil.copy(network_security_config_path, res_xml_path)
        print(f"network_security_config.xml 파일이 교체되었습니다: {res_xml_path}")
    except PermissionError as e:
        print(f"{network_security_config_path} 파일 복사 중 오류 발생: {e}")
        raise e
    except FileNotFoundError as e:
        print(e)
        raise e
    except Exception as e:
        print("유효하지 않은 output_path입니다.")
        raise e

def recompile_base_apk(output_path, package_dir):
    try:
        newbase_path = os.path.join(package_dir, "newbase.apk")
        subprocess.run(['java', '-jar', 'C:\\Windows\\apktool.jar', 'b', output_path, '-o', newbase_path], check=True)
        print("리컴파일에 성공하였습니다.")
    except subprocess.CalledProcessError as e:
        print("리컴파일에 실패했습니다. 프로그램을 종료합니다.")
        raise e
    except Exception as e:
        print("디컴파일된 apk 파일 경로를 찾지 못하였습니다. 프로그램을 종료합니다")
        raise e
    # 리컴파일 완료 후 base.apk 파일 삭제
    try:
        base_apk_path = os.path.join(package_dir, "base.apk")
        os.remove(base_apk_path)
        print(f"{base_apk_path} 파일이 삭제되었습니다.")
    except FileNotFoundError as e:
        print(f"{base_apk_path} 파일 삭제 중 오류 발생: {e}")
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
        raise e
    except Exception as e:
        print("설치할 서명된 APK 파일을 찾을 수 없습니다.")
        raise e

def keyChecking():
    key = input("프로그램을 재실행 '1' 입력 \n프로그램 종료 '0' 입력\n키 입력 : ")
    print(key)
    try:
        key = int(key)
        if key == 1:
            return 1
        elif key == 0:
            print("0입력")
            sys.exit(0)  # 프로그램 종료
        else:
            print("else 실행됨")
            return keyChecking()
    except ValueError:
        print("숫자 0 또는 1만 입력해주세요.")
        return keyChecking()
    
def main():

    key = 1

    while key:
        try: 
            package_name = input("패키지 이름을 입력하세요: ")

            # APK 경로 가져오기
            apk_files = get_apk_paths(package_name)

            #APK를 담을 폴더 생성
            package_dir = create_package_directory(package_name)

            # APK 파일 추출
            pull_apks(apk_files, package_dir, package_name)

            # base.apk 파일 디컴파일
            output_path = decompile_base_apk(package_dir)

            # network_security_config.xml 파일 교체
            change_network_security_config(output_path)

            # base.apk 파일 리컴파일
            recompile_base_apk(output_path, package_dir)

            # APK 파일 서명
            sign_apks(package_dir)

            # 서명된 APK 파일 설치
            install_signed_apks(package_name, package_dir)

            keyChecking()
        except:
            print("함수 오류")
            key = keyChecking()

    sys.exit(0)  # 프로그램 종료


if __name__ == "__main__":
    main()
