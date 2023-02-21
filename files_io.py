import json
import time
import xlsxwriter

def write_json_array(json_obj : str, path : str):
    with open(path, 'w') as file:
        json.dump(json_obj, file, ensure_ascii = False)

def timestamp():
    with open('temp_data/last_request_time', 'w') as file:
        t = str(round(time.time()))
        file.write(t)

def write_xlsx():
    # Собираем документы в кучу
    with open('temp_data/1234567890', 'r') as file:
        data = file.read()
        data = json.loads(data)

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('final/report.xlsx')
    worksheet = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    data = {"a":1234, "b":431, "c":"abcdef"}

    # Iterate over the data and write it out row by row.
    for key, val in data.items():
        worksheet.write(row, col,     key)
        worksheet.write(row, col + 1, val)
        row += 1

    workbook.close()
    
    return