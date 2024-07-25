import openpyxl

def excelStartPoint():
    fpath = r'C:\Users\BSJ\Desktop\testApps.xlsx'
    fpath = r"C:\Users\xten\Desktop\testApp.xlsx"

    #엑셀 불러오기
    wb = openpyxl.load_workbook(fpath)

    #엑셀 시트선택
    ws = wb['Sheet1']

    startPoint = int(input("시작 부분의 숫자를 입력해 주세요 : "))
    endPoint = int(input("끝 부분의 숫자를 입력해 주세요 : "))
    return startPoint, endPoint, ws

def excelEndPoint(startPoint, endPoint, app_name, result, error, detail):
    # fpath = r'C:\Users\BSJ\Desktop\result.xlsx'
    fpath = r"C:\Users\xten\Desktop\result.xlsx"
    wb = openpyxl.load_workbook(fpath)

    ws = wb['Sheet1']
    
    # startPoint와 endPoint가 올바른 범위인지 확인
    if startPoint > endPoint:
        raise ValueError("startPoint는 endPoint보다 작거나 같아야 합니다.")
    
    for row in range(startPoint, endPoint + 1):
        # 각 반복에서 새로운 마지막 행을 찾습니다.
        last_row = ws.max_row
        ws[f'A{last_row + 1}'] = app_name
        ws[f'B{last_row + 1}'] = result
        ws[f'C{last_row + 1}'] = error
        ws[f'D{last_row + 1}'] = detail
        
    wb.save(fpath)
