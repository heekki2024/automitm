# import subprocess
# import os
# import shutil
# import sys


# def get_apk_paths(package_name):
#     print("get_apk_paths 함수 실행중")

#     # 패키지 경로 가져오기
#     package_path = subprocess.run(['adb', 'shell', 'pm', 'list', 'packages', '-f', package_name], capture_output=True, text=True)
#     print(f"-------------{package_path} --------------")

#     # 결과에서 패키지 경로 필터링
#     paths = package_path.stdout.strip().split('\n')
#     apk_paths = []

#     print(paths)
#     for path in paths:
#         if package_name in path:
#             # Extract the part between "package:" and "/base.apk"
#             start_idx = path.find("package:") + len("package:")
#             end_idx = path.find("/base.apk")
#             apk_path = path[start_idx:end_idx]
#             apk_paths.append(apk_path)

#     print(apk_paths)

#     # 각 APK 파일에 대해 'adb shell ls' 명령어를 실행하여 존재 여부를 확인합니다.
#     apk_files = []
#     for apk_path in apk_paths:
#         # 'adb shell ls <apk_path>' 명령어 실행
#         ls_result = subprocess.run(['adb', 'shell', 'ls', apk_path], capture_output=True, text=True)
#         print(f"'{package_name}'의 ls 결과:")
#         print(ls_result.stdout.strip())
#         if ls_result.returncode != 0:
#             print(f"Error: {ls_result.stderr.strip()}")
#         else:
#             # ls 결과에서 .apk 파일만 필터링
#             files = ls_result.stdout.strip().split('\n')
#             for file in files:
#                 if file.endswith('.apk'):
#                     full_path = f"{apk_path}/{file}"
#                     apk_files.append(full_path)

#     print("get_apk_paths 함수 종료")
#     return apk_files

# def pull_apks(apk_files, destination_dir):
#     for apk_file in apk_files:
#         subprocess.run(['adb', 'pull', apk_file, destination_dir])

# def decompile_base_apk(package_name, destination_dir):
#     base_apk_path = os.path.join(destination_dir, "base.apk")

#     print(base_apk_path)

#     if os.path.exists(base_apk_path):
#         output_path = f"{destination_dir}2"

#         print(output_path)

#         subprocess.run(['java', '-jar', 'C:\\Windows\\apktool.jar', 'd', '-f', '-s', base_apk_path, '-o', output_path])

#         print(f"base.apk 디컴파일 완료: {output_path}")
#     else:
#         print(f"{base_apk_path} 파일을 찾을 수 없습니다.")
#         sys.exit(1)  # 프로그램 종료

#     return output_path, destination_dir

# def change_network_security_config(output_path):
#     res_xml_path = os.path.join(output_path, "res", "xml")
#     network_security_config_path = "C:\\Users\\xten\\Desktop\\network_security_config\\network_security_config.xml"
#     if os.path.exists(os.path.join(res_xml_path, "network_security_config.xml")):
#         shutil.copy(network_security_config_path, res_xml_path)
#         print(f"network_security_config.xml 파일이 교체되었습니다: {res_xml_path}")
#     else:
#         print("network_security_config.xml 파일을 찾을 수 없습니다.")
#         sys.exit(1)  # 프로그램 종료

# def recompile_base_apk(output_path, destination_dir):
#     newbase_path = os.path.join(destination_dir, "newbase.apk")

#     if os.path.exists(output_path):
#         try:
#             subprocess.run(['java', '-jar', 'C:\\Windows\\apktool.jar', 'b', output_path, '-o', newbase_path])
#             print("리컴파일에 성공하였습니다.")
#         except subprocess.CalledProcessError:
#             print("리컴파일에 실패했습니다. 프로그램을 종료합니다.")
#             sys.exit(1)  # 프로그램 종료
#     else:
#         print("디컴파일된 apk 파일 경로를 찾지 못하였습니다. 프로그램을 종료합니다")
#         sys.exit(1)  # 프로그램 종료


#     # 리컴파일 완료 후 base.apk 파일 삭제
#     base_apk_path = os.path.join(destination_dir, "base.apk")
#     if os.path.exists(base_apk_path):
#         try:
#             os.remove(base_apk_path)
#             print(f"{base_apk_path} 파일이 삭제되었습니다.")
#         except Exception as e:
#             print(f"{base_apk_path} 파일 삭제 중 오류 발생: {e}")
#             sys.exit(1)  # 프로그램 종료

# def sign_apks(destination_dir):
#     for file in os.listdir(destination_dir):
#         if file.endswith(".apk"):
#             apk_path = os.path.join(destination_dir, file)
#             try:
#                 subprocess.run(['java', '-jar', 'C:\\Windows\\uber-apk-signer-1.3.0.jar', '-a', apk_path, '--allowResign'], check=True)
#                 print(f"{file} 파일 서명 완료.")
#             except subprocess.CalledProcessError:
#                 print(f"{file} 파일 서명 실패.")
#                 sys.exit(1)  # 프로그램 종료

# def install_signed_apks(package_name, destination_dir):
#     # 기존 패키지 삭제
#     try:
#         subprocess.run(['adb', 'uninstall', package_name], check=True)
#         print(f"{package_name} 패키지 삭제 완료.")
#     except subprocess.CalledProcessError:
#         print(f"{package_name} 패키지 삭제 실패.")
#         sys.exit(1)  # 프로그램 종료

#     # 서명된 APK 파일 설치
#     apk_files_to_install = []
#     for file in os.listdir(destination_dir):
#         if file.endswith("-aligned-debugSigned.apk") and not file.endswith(".idsig"):
#             apk_files_to_install.append(os.path.join(destination_dir, file))
    
#     if apk_files_to_install:
#         try:
#             subprocess.run(['adb', 'install-multiple'] + apk_files_to_install, check=True)
#             print("서명된 APK 파일 설치 완료.")
#         except subprocess.CalledProcessError:
#             print("서명된 APK 파일 설치 실패.")
#             sys.exit(1)  # 프로그램 종료
#     else:
#         print("설치할 서명된 APK 파일을 찾을 수 없습니다.")
#         sys.exit(1)  # 프로그램 종료

# def main():
#     package_name = input("패키지 이름을 입력하세요: ")
#     destination_dir = input("APK 파일을 저장할 디렉토리를 입력하세요: ")

#     # APK 경로 가져오기
#     apk_files = get_apk_paths(package_name)
#     if not apk_files:
#         print(f"패키지 {package_name}에 대한 APK 파일을 찾을 수 없습니다.")
#         return

#     # APK 파일 추출
#     print(f"{package_name} 패키지의 APK 파일을 추출합니다...")
#     pull_apks(apk_files, destination_dir)
#     print("APK 파일 추출이 완료되었습니다.")

#     # base.apk 파일 디컴파일
#     output_path, destination_dir = decompile_base_apk(package_name, destination_dir)

#     # network_security_config.xml 파일 교체
#     change_network_security_config(output_path)

#     # base.apk 파일 리컴파일
#     recompile_base_apk(output_path, destination_dir)

#     # APK 파일 서명
#     sign_apks(destination_dir)

#     # 서명된 APK 파일 설치
#     install_signed_apks(package_name, destination_dir)

# if __name__ == "__main__":
#     main()

import subprocess
import os
import shutil
import sys


def create_package_directory(package_name):
    base_dir = "C:\\Users\\xten\\Desktop\\testing"
    package_dir = os.path.join(base_dir, package_name)

    try:
        os.makedirs(package_dir, exist_ok=True)
        print(f"{package_dir} 폴더가 생성되었습니다.")
    except Exception as e:
        print(f"{package_dir} 폴더 생성 중 오류 발생: {e}")
        keyChecking() # 재시작

    return package_dir

def get_apk_paths(package_name):
    print("get_apk_paths 함수 실행중")

    # 패키지 경로 가져오기
    package_path = subprocess.run(['adb', 'shell', 'pm', 'list', 'packages', '-f', package_name], capture_output=True, text=True)
    print(f"-------------{package_path} --------------")

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


    if not apk_files:
        print(f"패키지 {package_name}에 대한 APK 파일을 찾을 수 없습니다.")
        keyChecking() # 재시작

    print("get_apk_paths 함수 종료")
    return apk_files

def pull_apks(apk_files, package_dir, package_name):
    print(f"{package_name} 패키지의 APK 파일을 추출합니다...")

    for apk_file in apk_files:
        subprocess.run(['adb', 'pull', apk_file, package_dir])
    print("APK 파일 추출이 완료되었습니다.")


def decompile_base_apk(package_dir):
    base_apk_path = os.path.join(package_dir, "base.apk")

    print(base_apk_path)

    if os.path.exists(base_apk_path):
        output_path = f"{package_dir}2"

        print(output_path)

        subprocess.run(['java', '-jar', 'C:\\Windows\\apktool.jar', 'd', '-f', '-s', base_apk_path, '-o', output_path])

        print(f"base.apk 디컴파일 완료: {output_path}")
    else:
        print(f"{base_apk_path} 파일을 찾을 수 없습니다.")
        keyChecking() # 재시작

    return output_path

def change_network_security_config(output_path):
    res_xml_path = os.path.join(output_path, "res", "xml")
    network_security_config_path = "C:\\Users\\xten\\Desktop\\network_security_config\\network_security_config.xml"
    if os.path.exists(os.path.join(res_xml_path, "network_security_config.xml")):
        shutil.copy(network_security_config_path, res_xml_path)
        print(f"network_security_config.xml 파일이 교체되었습니다: {res_xml_path}")
    else:
        print("network_security_config.xml 파일을 찾을 수 없습니다.")
        keyChecking() # 재시작

def recompile_base_apk(output_path, package_dir):
    newbase_path = os.path.join(package_dir, "newbase.apk")

    if os.path.exists(output_path):
        try:
            subprocess.run(['java', '-jar', 'C:\\Windows\\apktool.jar', 'b', output_path, '-o', newbase_path])
            print("리컴파일에 성공하였습니다.")
        except subprocess.CalledProcessError:
            print("리컴파일에 실패했습니다. 프로그램을 종료합니다.")
            keyChecking() # 재시작
    else:
        print("디컴파일된 apk 파일 경로를 찾지 못하였습니다. 프로그램을 종료합니다")
        keyChecking() # 재시작


    # 리컴파일 완료 후 base.apk 파일 삭제
    base_apk_path = os.path.join(package_dir, "base.apk")
    if os.path.exists(base_apk_path):
        try:
            os.remove(base_apk_path)
            print(f"{base_apk_path} 파일이 삭제되었습니다.")
        except Exception as e:
            print(f"{base_apk_path} 파일 삭제 중 오류 발생: {e}")
            keyChecking() # 재시작

def sign_apks(package_dir):
    for file in os.listdir(package_dir):
        if file.endswith(".apk"):
            apk_path = os.path.join(package_dir, file)
            try:
                subprocess.run(['java', '-jar', 'C:\\Windows\\uber-apk-signer-1.3.0.jar', '-a', apk_path, '--allowResign'], check=True)
                print(f"{file} 파일 서명 완료.")
            except subprocess.CalledProcessError:
                print(f"{file} 파일 서명 실패.")
                keyChecking() # 재시작

def install_signed_apks(package_name, package_dir):
    # 기존 패키지 삭제
    try:
        subprocess.run(['adb', 'uninstall', package_name], check=True)
        print(f"{package_name} 패키지 삭제 완료.")
    except subprocess.CalledProcessError:
        print(f"{package_name} 패키지 삭제 실패.")
        keyChecking() # 재시작

    # 서명된 APK 파일 설치
    apk_files_to_install = []
    for file in os.listdir(package_dir):
        if file.endswith("-aligned-debugSigned.apk") and not file.endswith(".idsig"):
            apk_files_to_install.append(os.path.join(package_dir, file))
    
    if apk_files_to_install:
        try:
            subprocess.run(['adb', 'install-multiple'] + apk_files_to_install, check=True)
            print("서명된 APK 파일 설치 완료.")
        except subprocess.CalledProcessError:
            print("서명된 APK 파일 설치 실패.")
            keyChecking() # 재시작
    else:
        print("설치할 서명된 APK 파일을 찾을 수 없습니다.")
        keyChecking() # 재시작


def keyChecking():
    key = input ("프로그램을 재실행 '1' 입력 \n프로그램 종료 '0' 입력\n키 입력 : ")

    if key == 1:
        return
    elif key == 0:
        sys.exit(1)  # 프로그램 종료
    else:
        keyChecking()

def main():

    global key
    key = 1

    while key:

        package_name = input("패키지 이름을 입력하세요: ")

        #APK를 담을 폴더 생성
        package_dir = create_package_directory(package_name)

        # APK 경로 가져오기
        apk_files = get_apk_paths(package_name)

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
    sys.exit(1)  # 프로그램 종료


if __name__ == "__main__":
    main()
