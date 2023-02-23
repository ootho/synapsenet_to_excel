from bs4 import BeautifulSoup
from files_io import tax_id_check
import requests
import json
import xlsxwriter
import openpyxl

import bs4_sandbox

# получаем html по списку ИНН
def bs4_scraper(path : str):
    with open(path,'r') as file:
        data = file.read()
        tax_id_list = json.loads(data)
    
    for i in tax_id_list:
        url = f'https://synapsenet.ru/searchorganization/proverka-kontragentov?query={i}'
        page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    with open('html.html','w') as file:
        file.write(str(soup.contents))
    return

bs4_scraper('file.txt')

def write_xlsx(data):
    try:
        workbook = openpyxl.load_workbook('final/report.xlsx')
    except Exception as ex:
        print(ex)
        workbook = openpyxl.Workbook(write_only=False)
    
    worksheet = workbook.active

    # Если лист пустой добавляем заголовки
    row = worksheet.max_row
    if row == 1:
        for idx, column in enumerate(data.keys()):
            worksheet.cell(row=row, column=idx+1, value=column)

    # Добавляем данные в свободную строку
    row += 1
    for idx, value in enumerate(data.values()):
        worksheet.cell(row=row, column=idx+1, value=value)

    #/////////////////////////////////////////////////////////////////////////////
    '''
    если есть, то добавляем новые данные
    ели данные пустые, то меняем цвет ячеек
    '''
    #/////////////////////////////////////////////////////////////////////////////
    # Iterate over the data and write it out row by row.

    # Сохраняем книгу
    workbook.save('final/report.xlsx')
    return

def scraper_main_loop(path):
    with open(path,'r') as file:
        data = file.read()
        tax_id_list = json.loads(data)
    
    # Проходим по списку ИНН
    for tax_id in tax_id_list:

        # Проверяем есть ли данные по этому ИНН в файле Эксель
        if not tax_id_check('final/report.xlsx', tax_id):

            # Запрашиваем и получаем HTML документ
            url = f'https://synapsenet.ru/searchorganization/proverka-kontragentov?query={tax_id}'

            #  Получаем страницу по ссылке
            page = requests.get(url)
            # Если получили страницу, то парсим
#///////////////////////////////////////////////////////////////////////////////
            # Если не получили, то всталяем пустую строку и выделяем цветом
                
            # Парсим документ и получаем словарь с данными
            soup = BeautifulSoup(page.content, 'html.parser')

            with open('html.html','w') as file:
                file.write(str(soup.contents))

            data_dict = bs4_sandbox.html_scraper(soup)

            # Добавляем значения словаря в файл Эксель
            write_xlsx(data_dict)

    return

# scraper_main_loop('file.txt')
