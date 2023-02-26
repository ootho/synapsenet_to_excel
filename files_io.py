import openpyxl
from openpyxl.styles import PatternFill

# Запись данных в xlsx файл
def write_xlsx(data):
    # Пробуем открыть файл, если нет, то создаём
    try:
        workbook = openpyxl.load_workbook('final/report.xlsx')
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

    # Добавляем новые данные в первую найденую пустую строку
    row += 1
    for idx, value in enumerate(data.values()):
        cell = worksheet.cell(row=row, column=idx+1, value=value)

        # Если получили только ИНН и timestamp, значит данные не обнаружены, пишем в таблицу то что есть и выделаем строку цветом
        if len([x for x in list(data.values()) if x!='na'])==2:
            red_fill = PatternFill(start_color='FFFF0000', end_color='FFFF0000', fill_type='solid')
            # Присваиваем Fill ячейке
            cell.fill = red_fill

    # Сохраняем книгу
    workbook.save('final/report.xlsx')
    return


# Проверка есть ли ИНН в файле xlsx
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