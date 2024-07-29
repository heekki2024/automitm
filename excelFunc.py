# from tkinter import Tk, filedialog, messagebox
# import tkinter as tk
# import openpyxl
# import configparser
# import os
# import sys
# import pdb  



# CONFIG_FILE = 'config.ini'

# def load_config():
#     root = tk.Tk()
#     root.withdraw()  # 숨겨진 Tkinter 창 생성
#     config = configparser.ConfigParser()
    
#     def on_closing():
#         root.destroy()
#         sys.exit()


#     root.protocol("WM_DELETE_WINDOW", on_closing)
#     if os.path.exists(CONFIG_FILE):
#         config.read(CONFIG_FILE)
#         input_path = config['PATHS'].get('input_path', '')
#         output_path = config['PATHS'].get('output_path', '')

#         if os.path.exists(input_path) and os.path.exists(output_path):
#             yes_or_no = messagebox.askyesno("알림", f"이전에 지정된 Excel 입출력 경로값이 있습니다.\n입력 : {input_path}\n출력 : {output_path}\n계속 이 경로를 사용하시겠습니까?")
#             root.destroy()
#             if yes_or_no:
#                 return config
#             else:
#                 return None
#         else:
#             # messagebox.showinfo("알림", "해당 경로에 Excel입출력 파일이 존재하지 않습니다\nExcel입출력 파일 경로를 다시 지정합니다.")
#             root.destroy()
#             return None
#     else:
#         root.destroy()
#         return None

# def save_config(config):
#     with open(CONFIG_FILE, 'w') as configfile:
#         config.write(configfile)

# def select_file_path():
#     root = Tk()
#     root.withdraw()
#     file_path = filedialog.askopenfilename(
#         title="파일을 선택하세요",
#         filetypes=(("엑셀 파일", "*.xlsx"), ("모든 파일", "*.*"))
#     )
#     root.destroy()
#     return file_path

# def center_window(root, width, height):
#     # 화면 너비와 높이 가져오기
#     screen_width = root.winfo_screenwidth()
#     screen_height = root.winfo_screenheight()

#     # 창의 위치 계산
#     x = (screen_width - width) // 2
#     y = (screen_height - height) // 2

#     # 창의 위치와 크기 설정
#     root.geometry(f'{width}x{height}+{x}+{y}')


# def set_paths_gui():
#     root = Tk()
#     root.title("파일 경로 설정")
#     root.attributes('-topmost', True)
#     center_window(root, 580, 120)

#     def on_closing():
#         root.destroy()
#         sys.exit()
#     root.protocol("WM_DELETE_WINDOW", on_closing)


#     config = configparser.ConfigParser()
#     config.read(CONFIG_FILE)

#     #  pdb.set_trace()  # Add a breakpoint here to inspect the config object

#     if not os.path.exists(config['PATHS']['input_path']):
#         config['PATHS']['input_path'] = ''
#     if not os.path.exists(config['PATHS']['output_path']):
#         config['PATHS']['output_path'] = ''
#     if 'PATHS' not in config:
#         config['PATHS'] = {'input_path': '', 'output_path': ''}

#     input_var = tk.StringVar(value=config['PATHS']['input_path'])
#     output_var = tk.StringVar(value=config['PATHS']['output_path'])


#     if os.path.exists(config['PATHS']['input_path']):
#         input_var = tk.StringVar(value=config['PATHS']['input_path'])
#         print('testing')
#     if os.path.exists(config['PATHS']['output_path']):
#         output_var = tk.StringVar(value=config['PATHS']['output_path'])
#         print('testing1')



#     def update_input_path():
#         new_path = select_file_path()
#         if new_path:
#             input_var.set(new_path)

#     def update_output_path():
#         new_path = select_file_path()
#         if new_path:
#             output_var.set(new_path)

#     tk.Label(root, text="Excel 입력 파일 경로:").grid(row=0, column=0, padx=10, pady=5)
#     tk.Entry(root, textvariable=input_var, width=50).grid(row=0, column=1, padx=10, pady=5)
#     tk.Button(root, text="변경", command=update_input_path).grid(row=0, column=2, padx=10, pady=5)

#     tk.Label(root, text="Excel 출력 파일 경로:").grid(row=1, column=0, padx=10, pady=5)
#     tk.Entry(root, textvariable=output_var, width=50).grid(row=1, column=1, padx=10, pady=5)
#     tk.Button(root, text="변경", command=update_output_path).grid(row=1, column=2, padx=10, pady=5)

#     def save_and_close():
#         config['PATHS']['input_path'] = input_var.get()
#         config['PATHS']['output_path'] = output_var.get()
#         save_config(config)
#         root.destroy()



#     tk.Button(root, text="저장 및 닫기", command=save_and_close).grid(row=2, column=0, columnspan=3, pady=10)

#     root.mainloop()

#     return config['PATHS']['input_path'], config['PATHS']['output_path']


# def excelStartPoint(input_path):


#     # 엑셀 불러오기
#     wb = openpyxl.load_workbook(input_path)
#     ws = wb['Sheet1']

#     try:
#         def confirm():
#             nonlocal startPoint, endPoint
#             try:
#                 startPoint = int(ent1.get())
#                 endPoint = int(ent2.get())
#                 if startPoint > endPoint:
#                     messagebox.showerror("입력 오류", "시작점이 끝점보다 수가 적어야 합니다")
#                     return  # 잘못된 입력이므로 확인 버튼을 다시 누르도록 함
#                 root.quit()
#             except ValueError:
#                 messagebox.showerror("입력 오류", "숫자를 입력해 주세요")
#         startPoint = None
#         endPoint = None
            
#         root = Tk()
#         root.title("앱 패키지 범위 지정")
#         root.attributes('-topmost', True)

#         # 창을 화면 가운데로 이동
#         center_window(root, 400, 300)
#         def on_closing():
#             root.destroy()
#             sys.exit()

#         root.protocol("WM_DELETE_WINDOW", on_closing)

#         relative_path = os.path.join("images", "logo.png")

#         lab_d = tk.Label(root)
#         img = tk.PhotoImage(file = relative_path, master = root)
#         lab_d.config(image = img)
#         lab_d.pack()


#         #startPoint 라벨
#         lab1 = tk.Label(root)
#         lab1.config(text = 'Excel 시작점')
#         lab1.pack()

#         #startPoint 입력창
#         ent1 = tk.Entry(root)

#         ent1.pack()


#         #endPoint 라벨
#         lab2 = tk.Label(root)
#         lab2.config(text = 'Excel 끝점')
#         lab2.pack()

#         #endPoint 입력창
#         ent2 = tk.Entry(root)

#         ent2.pack()

#         btn = tk.Button(root)
#         btn.config(text = '확인')

#         btn.config(command = confirm)
#         btn.pack()
                
#         root.mainloop()
#         root.destroy()
#     except Exception as e:
#         return e

#     return startPoint, endPoint, ws

# def excelEndPoint(output_path, app_name, result, error, detail):


#     if not output_path:
#         raise ValueError("저장할 파일 경로를 선택해 주세요.")

#     wb = openpyxl.load_workbook(output_path)
#     ws = wb['Sheet1']

#     last_row = ws.max_row + 1  # 다음에 기록할 행 번호
#     ws[f'A{last_row}'] = app_name
#     ws[f'B{last_row}'] = result
#     ws[f'C{last_row}'] = error
#     ws[f'D{last_row}'] = detail

#     wb.save(output_path)

from tkinter import Tk, filedialog, messagebox
import tkinter as tk
import openpyxl
import configparser
import os
import sys
import pdb  



CONFIG_FILE = 'config.ini'

def load_config():
    root = tk.Tk()
    root.withdraw()  # 숨겨진 Tkinter 창 생성
    config = configparser.ConfigParser()
    
    def on_closing():
        root.destroy()
        sys.exit()


    root.protocol("WM_DELETE_WINDOW", on_closing)
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)

        root.destroy()
        return config

    else:
        config = set_paths_gui()   


        root.destroy()
        return config


def save_config(config):
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def select_file_path():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="파일을 선택하세요",
        #튜플타입
        filetypes=[("모든 파일", "*.*")]
    )
    root.destroy()
    return file_path

def select_folder_path():
    root = tk.Tk()
    root.withdraw()  # 메인 윈도우를 숨깁니다
    folder_path = filedialog.askdirectory(
        title="폴더를 선택하세요"
    )
    root.destroy()  # 메인 윈도우를 종료합니다
    return folder_path

def center_window(root, width, height):
    # 화면 너비와 높이 가져오기
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # 창의 위치 계산
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # 창의 위치와 크기 설정
    root.geometry(f'{width}x{height}+{x}+{y}')


def set_paths_gui():
    root = Tk()
    root.title("파일 경로 설정")
    root.attributes('-topmost', True)
    center_window(root, 700, 230)

    def on_closing():
        root.destroy()
        sys.exit()
    root.protocol("WM_DELETE_WINDOW", on_closing)


    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)

    #  pdb.set_trace()  # Add a breakpoint here to inspect the config object
    if os.path.exists(CONFIG_FILE):
        if not os.path.exists(config['PATHS']['input_path']):
            config['PATHS']['input_path'] = ''
        else:
            input_var = tk.StringVar(value=config['PATHS']['input_path'])
            
        if not os.path.exists(config['PATHS']['output_path']):
            config['PATHS']['output_path'] = ''
        else:
            output_var = tk.StringVar(value=config['PATHS']['output_path'])
        
        if not os.path.exists(config['PATHS']['base_path']):
            config['PATHS']['base_path'] = ''
        else:
            base_var = tk.StringVar(value=config['PATHS']['base_path'])

        if not os.path.exists(config['PATHS']['network_security_config_path']):
            config['PATHS']['network_security_config'] = '' 
        else:
            network_security_config_path_var = tk.StringVar(value=config['PATHS']['network_security_config_path'])

        if not os.path.exists(config['PATHS']['network_security_config_with_r_path']):
            config['PATHS']['network_security_config_with_r'] = ''     
        else:
            network_security_config_with_r_path_var = tk.StringVar(value=config['PATHS']['network_security_config_with_r_path'])
        
    else:
        # config 파일이 존재하지 않을 경우 한번에 config설정. 값은 없음
        config['PATHS'] = {'input_path': '', 'output_path': '', 'base_path': '', 'network_security_config_path': '', 'network_security_config_with_r_path': ''}

    input_var = tk.StringVar(value=config['PATHS']['input_path'])
    output_var = tk.StringVar(value=config['PATHS']['output_path'])
    base_var = tk.StringVar(value=config['PATHS']['base_path'])
    network_security_config_path_var = tk.StringVar(value=config['PATHS']['network_security_config_path'])
    network_security_config_with_r_path_var = tk.StringVar(value=config['PATHS']['network_security_config_with_r_path'])


    def update_input_path():
        new_path = select_file_path()
        if new_path:
            input_var.set(new_path)

    def update_output_path():
        new_path = select_file_path()
        if new_path:
            output_var.set(new_path)

    def update_base_path():
        new_path = select_folder_path()
        if new_path:
            base_var.set(new_path)

    def update_network_security_config_path_path():
        new_path = select_file_path()
        if new_path:
            network_security_config_path_var.set(new_path)

    def update_network_security_config_with_r_path():
        new_path = select_file_path()
        if new_path:
            network_security_config_with_r_path_var.set(new_path)

    tk.Label(root, text="Excel 입력 파일 경로 :").grid(row=0, column=0, padx=10, pady=5)
    tk.Entry(root, textvariable=input_var, width=50).grid(row=0, column=1, padx=10, pady=5)
    tk.Button(root, text="변경", command=update_input_path).grid(row=0, column=2, padx=10, pady=5)

    tk.Label(root, text="Excel 출력 파일 경로 :").grid(row=1, column=0, padx=10, pady=5)
    tk.Entry(root, textvariable=output_var, width=50).grid(row=1, column=1, padx=10, pady=5)
    tk.Button(root, text="변경", command=update_output_path).grid(row=1, column=2, padx=10, pady=5)

    tk.Label(root, text="Base 폴더 경로 :").grid(row=2, column=0, padx=10, pady=5)
    tk.Entry(root, textvariable=base_var, width=50).grid(row=2, column=1, padx=10, pady=5)
    tk.Button(root, text="변경", command=update_base_path).grid(row=2, column=2, padx=10, pady=5)

    tk.Label(root, text="network_security_config 파일 경로 :").grid(row=3, column=0, padx=10, pady=5)
    tk.Entry(root, textvariable=network_security_config_path_var, width=50).grid(row=3, column=1, padx=10, pady=5)
    tk.Button(root, text="변경", command=update_network_security_config_path_path).grid(row=3, column=2, padx=10, pady=5)

    tk.Label(root, text="network_security_config_with_r 파일 경로 :").grid(row=4, column=0, padx=10, pady=5)
    tk.Entry(root, textvariable=network_security_config_with_r_path_var, width=50).grid(row=4, column=1, padx=10, pady=5)
    tk.Button(root, text="변경", command=update_network_security_config_with_r_path).grid(row=4, column=2, padx=10, pady=5)

    def save_and_close():
        if not input_var.get() or not output_var.get() or not base_var.get() or not network_security_config_path_var.get() or not network_security_config_with_r_path_var.get():
            messagebox.showwarning("경고", "모든 경로를 설정해야 합니다.")
            return  # 경로가 지정되지 않은 경우 함수를 종료하고 계속 실행     
           
        config['PATHS']['input_path'] = input_var.get()
        config['PATHS']['output_path'] = output_var.get()
        config['PATHS']['base_path'] = base_var.get()
        config['PATHS']['network_security_config_path'] = network_security_config_path_var.get()      
        config['PATHS']['network_security_config_with_r_path'] = network_security_config_with_r_path_var.get()        

        save_config(config)
        root.destroy()



    tk.Button(root, text=" 저장 ", command=save_and_close).grid(row=5, column=0, columnspan=3, pady=10)

    root.mainloop()

    # return config['PATHS']['input_path'], config['PATHS']['output_path']
    return config

def excelStartPoint(input_path):


    # 엑셀 불러오기
    wb = openpyxl.load_workbook(input_path)
    ws = wb['Sheet1']

    try:
        def confirm():
            nonlocal startPoint, endPoint
            try:
                startPoint = int(ent1.get())
                endPoint = int(ent2.get())
                if startPoint > endPoint:
                    messagebox.showerror("입력 오류", "시작점이 끝점보다 수가 적어야 합니다")
                    return  # 잘못된 입력이므로 확인 버튼을 다시 누르도록 함
                root.quit()
            except ValueError:
                messagebox.showerror("입력 오류", "숫자를 입력해 주세요")

        def path_change():
            set_paths_gui()
            

        startPoint = None
        endPoint = None
            
        root = Tk()
        root.title("앱 패키지 범위 지정")
        root.attributes('-topmost', True)

        # 창을 화면 가운데로 이동
        center_window(root, 400, 300)
        def on_closing():
            root.destroy()
            sys.exit()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        relative_path = os.path.join("images", "logo.png")

        lab_d = tk.Label(root)
        img = tk.PhotoImage(file = relative_path, master = root)
        lab_d.config(image = img)
        lab_d.pack()


        #startPoint 라벨
        lab1 = tk.Label(root)
        lab1.config(text = 'Excel 시작점')
        lab1.pack()

        #startPoint 입력창
        ent1 = tk.Entry(root)

        ent1.pack()


        #endPoint 라벨
        lab2 = tk.Label(root)
        lab2.config(text = 'Excel 끝점')
        lab2.pack()

        #endPoint 입력창
        ent2 = tk.Entry(root)

        ent2.pack()

        #확인

        btn = tk.Button(root)
        btn.config(text = '확인')

        btn.config(command = confirm)
        btn.pack()

        #파일 경로 변경

        btn = tk.Button(root)
        btn.config(text = '파일 경로 변경')

        btn.config(command = path_change)
        btn.pack()
                
        root.mainloop()
        root.destroy()
    except Exception as e:
        return e

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
