import subprocess

def get_apk_paths(package_name):

    # 패키지 경로 가져오기
    print("get_apk_paths 함수 실행중")

    package_path = subprocess.run(['adb', 'shell', 'pm', 'list', 'packages', '-f', package_name], capture_output=True, text=True)

    print(package_path)

        # 결과에서 패키지 경로 필터링
    paths = package_path.stdout.strip().split('\n')
    
    apk_paths = []
    for path in paths:
        if package_name in path:
            # Extract the part between "package:" and "/base.apk"
            start_idx = path.find("package:") + len("package:")
            end_idx = path.find("/base.apk")
            apk_path = path[start_idx:end_idx]
            apk_paths.append(apk_path)

    print(apk_paths)

        # 각 APK 파일에 대해 'adb shell ls' 명령어를 실행하여 존재 여부를 확인합니다.
    for apk_path in apk_paths:
        # 'adb shell ls <apk_path>' 명령어 실행
        ls_result = subprocess.run(['adb', 'shell', 'ls', apk_path], capture_output=True, text=True)
        print(f"'{package_name}'의 ls 결과:")
        print(ls_result.stdout.strip())
        if ls_result.returncode != 0:
            print(f"Error: {ls_result.stderr.strip()}")

    print("get_apk_paths 함수 종료") 
    return apk_paths

def pull_apks(apk_paths, destination_dir):
    for apk_path in apk_paths:
        subprocess.run(['adb', 'pull', apk_path, destination_dir])

def main():
    package_name = input("패키지 이름을 입력하세요: ")
    #destination_dir = input("APK 파일을 저장할 디렉토리를 입력하세요: ")

    # APK 경로 가져오기
    apk_paths = get_apk_paths(package_name)
    if not apk_paths:
        print(f"패키지 {package_name}에 대한 APK 파일을 찾을 수 없습니다.")
        return

    # APK 파일 추출
    print(f"{package_name} 패키지의 APK 파일을 추출합니다...")
   #pull_apks(apk_paths, destination_dir)
    #print("APK 파일 추출이 완료되었습니다.")

if __name__ == "__main__":
    main()