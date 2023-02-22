from bs4 import BeautifulSoup
import requests
import json

def bs4_scraper():
    with open('file.txt','r') as file:
        data = file.read()
        tax_id_list = json.loads(data)

    for i in tax_id_list:
        url = f'https://synapsenet.ru/searchorganization/proverka-kontragentov?query={i}'
        page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    with open('html.html','w') as file:
        file.write(str(soup.contents))
    return

bs4_scraper()

import xlsxwriter

#Передаём сюда словарь сразу со всеми объектами
def write_xlsx(data):
    # Create a workbook and add a worksheet.
    print(data)
    workbook = xlsxwriter.Workbook('final/report.xlsx')
    worksheet = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.
    col = 0

    #если в файле есть названия колонок, то оставляем как есть, если нет то вставляем из первого файла в списке
    columns = []
    rows_count = worksheet.dim_rowmax
    if rows_count == None:
        rows_count = 0
        for i in data.keys():
            worksheet.write(0, col, i)
            columns.append(i)
            col += 1

    for col_idx, column in enumerate(columns):
        value = data.get(column, None)
        if value is not None:
            worksheet.write(rows_count + 1, col_idx, value)

#/////////////////////////////////////////////////////////////////////////////
    '''
    если есть, то добавляем новые данные
    ели данные пустые, то меняем цвет ячеек
    '''
#/////////////////////////////////////////////////////////////////////////////
    # Iterate over the data and write it out row by row.
    
    workbook.close()
    
    return