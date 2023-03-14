import os
import requests

import bs4_sandbox
from bs4 import BeautifulSoup

from files_io import duplicates_check, write_xlsm, preparing_to_upload, delete_file

URL = 'https://synapsenet.ru/searchorganization/proverka-kontragentov?query='

def main_loop(tax_id_list, date):
    # Задержка чтобы избежать блокировки со стороны сайта
    # time.sleep(2)
    # Проходим по списку ИНН
    for idx, tax_id in enumerate(tax_id_list):
        print(f'{idx}\t{tax_id}')
        # Проверяем есть ли данные по этому ИНН в файле Эксель
        if not duplicates_check('wip/report.xlsm', 'ИНН', tax_id):
            #  Получаем страницу и преобразуем в объект bs4
            url = f'{URL}{tax_id}'
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'lxml')
            # Проверяем сколько организаций мы нашли по ИНН
            soups = []
            check_if_many = soup.find_all(class_="org-pcl-go-but")
            if len(check_if_many) > 0:
                # Если мы нашли более одной организации по ИНН, то извлекаем ссылки на них
                hrefs = [i['href']
                         for i in soup.find_all(class_="org-pcl-go-but")]
                # Печатаем сообщение с этим ИНН
                print(f'Нашли более 1 организации по ИНН :{tax_id}')
                # Пробегаем по спику ссылок
                for ref in hrefs:
                    # Задержка чтобы избежать блокировки со стороны сайта
                    # time.sleep(2)
                    url = f'{URL}{ref}'
                    page = requests.get(url)
                    soup = BeautifulSoup(page.content, 'lxml')
                    # Добавляем объекты bs4 в список soups
                    soups.append(soup)
            else:
                # Если по ИНН найдена одна организация, то добавляем её в список
                soups.append(soup)

            os.makedirs(f'html/{date}/', exist_ok=True)

            # Записываем данные об организациях файлы для отладки
            with open(f'html/{date}/{tax_id}.html', 'w') as file:
                file.write(str(soup.contents))
            exit

            for one_soup in soups:
                # Собираем необходимые данные с помощью bs4 и получаем словарь
                data_dict = bs4_sandbox.html_scraper(one_soup, tax_id)

                # Если несколько организаций с одним ИНН проверяем по КПП:
                duplicates = False
                if len(check_if_many) > 0:
                    duplicates = duplicates_check(
                        'wip/report.xlsm', 'КПП', data_dict['КПП'])

                # Добавляем значения словаря в файл Эксель
                if not duplicates:
                    write_xlsm(data_dict)

    # После того, как всё записали отправляем файл в другую папку
    preparing_to_upload()
    delete_file()

    return "Tax IDs received, the report has been sent!"
