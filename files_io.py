import json, time, xlsxwriter, openpyxl

# Записаь списка в json файл
def write_json_array(json_obj : str, path : str):
    with open(path, 'w') as file:
        json.dump(json_obj, file, ensure_ascii = False)
    return

# Запись времени последнего запроса в файл
def timestamp():
    with open('temp_data/last_request_time', 'w') as file:
        t = str(round(time.time()))
        file.write(t)
    return

# Проверка есть ли ИНН в файле xlsx
def duplicates_check(path : str, name : str, tax_id : str) -> bool:
    try:
        # Загрузка Excel файла
        wb = openpyxl.load_workbook(filename=path, read_only=True)

        # Получение активного листа
        sheet = wb.active

        # Получение индекса столбца по заголовку "ИНН"
        column_num = next(sheet.values).index(name)

        # Перебор ячеек в столбце
        for row in sheet.iter_rows(min_row=2, min_col=column_num, max_col=column_num):
            for cell in row:
                if cell.value == tax_id:
                    # ИНН найден
                    return True
    except Exception as ex:
        print (ex)
        # ИНН не найден
        return False

def kpp_check(kpp : str) -> bool:
    try:
        # Загрузка Excel файла
        wb = openpyxl.load_workbook(filename=path, read_only=True)

        # Получение активного листа
        sheet = wb.active

        # Получение индекса столбца по заголовку "ИНН"
        column_num = next(sheet.values).index('ИНН')

        # Перебор ячеек в столбце
        for row in sheet.iter_rows(min_row=2, min_col=column_num, max_col=column_num):
            for cell in row:
                if cell.value == tax_id:
                    # ИНН найден
                    return True
    except Exception as ex:
        print (ex)
        # ИНН не найден
        return False

# print(tax_id_check('final/report.xlsx', '7721793895'))