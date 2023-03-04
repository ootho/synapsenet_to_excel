import openpyxl, os, time
from openpyxl.styles import PatternFill

# Запись данных в xlsx файл
def write_xlsx(data):
    # Пробуем открыть файл, если нет, то создаём
    try:
        workbook = openpyxl.load_workbook('xlsx/report.xlsx')
    except Exception as ex:
        print(ex)
        workbook = openpyxl.Workbook(write_only=False)
    
    # Выбираем страницу
    worksheet = workbook.active

    # Если лист пустой, то добавляем заголовки
    row = worksheet.max_row
    if row == 1:
        for idx, column in enumerate(data.keys()):
            worksheet.cell(row=row, column=idx+1, value=column)

    # Если в словаре передаются данные, которым не соответствует ни одна колонка, создаём новую колонку
    for idx, column in enumerate(data.keys()):
        if column not in [cell.value for cell in worksheet[1]]:
            worksheet.cell(row=1, column=worksheet.max_column + 1, value=column)

    row += 1
    for idx, column in enumerate(worksheet[1], start=1):
        if column.value in data:
            cell = worksheet.cell(row=row, column=idx, value=data[column.value])

        # Если получили только ИНН и timestamp, значит данные не обнаружены, пишем в таблицу то что есть и выделаем строку цветом
        if len([x for x in list(data.values()) if x!='na'])==2:
            red_fill = PatternFill(start_color='FFFF0000', end_color='FFFF0000', fill_type='solid')
            # Присваиваем Fill ячейке
            cell.fill = red_fill

    # Сохраняем книгу
    workbook.save('xlsx/report.xlsx')
    return


# Проверка есть ли ИНН в файле xlsx, true - дубликат, false - нет
def duplicates_check(path : str, name : str, feature : str) -> bool:
    try:
        # Загрузка Excel файла
        wb = openpyxl.load_workbook(filename=path, read_only=True)

        # Получение активного листа
        sheet = wb.active

        # Получение индекса столбца по нужному заголовку (ИНН или КПП)
        column_num = next(sheet.values).index(name)

        # Перебор ячеек в столбце
        for row in sheet.iter_rows(min_row=2, min_col=column_num, max_col=column_num):
            for cell in row:
                if cell.value == feature:
                    # Признак найден
                    return True
    except Exception as x:
        print (x)
        # Признак не найден
        return False

def preparing_to_upload():
    wb = openpyxl.load_workbook(filename='xlsx/report.xlsx')
    ws = wb.active

    for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
        for cell in row:
            if cell.value == 'timestamp':
                ws.delete_cols(cell.column)

    wb.save('sent/report.xlsx')

def not_exist_or_modified_more_than_day_ago():
    try:
        now = time.time()
        mtime = os.path.getmtime('/mnt/d/WORK/Coding/synapsenet_to_excel/xlsx/report.xlsx')
        return (now - mtime) > 10 #(24 * 60 * 60) 
    except Exception as x:
        # print(x)
        return True
    
def delete_file():
    try:
        os.remove('/mnt/d/WORK/Coding/synapsenet_to_excel/xlsx/report.xlsx')
    except Exception as x:
        print(x)
