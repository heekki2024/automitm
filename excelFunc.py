from tkinter import Tk, filedialog, messagebox
import tkinter as tk
import openpyxl
import configparser
import os

CONFIG_FILE = 'config.ini'

def load_config():
    root = Tk()
    root.withdraw()  # 숨겨진 Tkinter 창 생성
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        yes_or_no = messagebox.askyesno("알림", f"이전에 지정된 엑셀 입출력 경로가 있습니다.\n{config['PATHS']['input_path']}\n{config['PATHS']['output_path']}\n계속 이 경로를 사용하시겠습니까?")
        root.destroy()
        if yes_or_no:
            return config
        else:
            return None
    else:
        root.destroy()
        return None

def save_config(config):
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def select_file_path():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="파일을 선택하세요",
        filetypes=(("엑셀 파일", "*.xlsx"), ("모든 파일", "*.*"))
    )
    root.destroy()
    return file_path 

def set_paths_gui():
    root = Tk()
    root.title("파일 경로 설정")
    root.attributes('-topmost', True)

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    if 'PATHS' not in config:
        config['PATHS'] = {'input_path': '', 'output_path': ''}
    
    input_var = tk.StringVar(value=config['PATHS']['input_path'])
    output_var = tk.StringVar(value=config['PATHS']['output_path'])

    def update_input_path():
        new_path = select_file_path()
        if new_path:
            input_var.set(new_path)

    def update_output_path():
        new_path = select_file_path()
        if new_path:
            output_var.set(new_path)

    tk.Label(root, text="입력 파일 경로:").grid(row=0, column=0, padx=10, pady=5)
    tk.Entry(root, textvariable=input_var, width=50).grid(row=0, column=1, padx=10, pady=5)
    tk.Button(root, text="변경", command=update_input_path).grid(row=0, column=2, padx=10, pady=5)

    tk.Label(root, text="출력 파일 경로:").grid(row=1, column=0, padx=10, pady=5)
    tk.Entry(root, textvariable=output_var, width=50).grid(row=1, column=1, padx=10, pady=5)
    tk.Button(root, text="변경", command=update_output_path).grid(row=1, column=2, padx=10, pady=5)

    def save_and_close():
        config['PATHS']['input_path'] = input_var.get()
        config['PATHS']['output_path'] = output_var.get()
        save_config(config)
        root.destroy()



    tk.Button(root, text="저장 및 닫기", command=save_and_close).grid(row=2, column=0, columnspan=3, pady=10)

    root.mainloop()
    
    return config['PATHS']['input_path'], config['PATHS']['output_path']


def excelStartPoint(input_path):

   
    # 엑셀 불러오기
    wb = openpyxl.load_workbook(input_path)
    ws = wb['Sheet1']

    try:
        startPoint = int(input("시작 부분의 숫자를 입력해 주세요: "))
        endPoint = int(input("끝 부분의 숫자를 입력해 주세요: "))
    except ValueError:
        raise ValueError("시작 및 끝 부분의 숫자는 정수여야 합니다.")

    if startPoint > endPoint:
        raise ValueError("startPoint는 endPoint보다 작거나 같아야 합니다.")

    return startPoint, endPoint, ws

def excelEndPoint(output_path, app_name, result, error, detail):
 

    if not output_path:
        raise ValueError("저장할 파일 경로를 선택해 주세요.")

    wb = openpyxl.load_workbook(output_path)
    ws = wb['Sheet1']
    
    last_row = ws.max_row + 1  # 다음에 기록할 행 번호
    ws[f'A{last_row}'] = app_name
    ws[f'B{last_row}'] = result
    ws[f'C{last_row}'] = error
    ws[f'D{last_row}'] = detail
    
    wb.save(output_path)
