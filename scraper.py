from bs4 import BeautifulSoup
from files_io import duplicates_check
import requests
from files_io import write_xlsx
import bs4_sandbox

def scraper_main_loop(tax_id_list):
    # Проходим по списку ИНН
    for tax_id in tax_id_list:

        # Проверяем есть ли данные по этому ИНН в файле Эксель
        if not duplicates_check('final/report.xlsx', 'ИНН', tax_id):

            #  Получаем страницу и преобразуем в объект bs4
            url = f'https://synapsenet.ru/searchorganization/proverka-kontragentov?query={tax_id}'
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            # Проверяем сколько организаций мы нашли по ИНН
            soups = []
            check_if_many = soup.find_all(class_="org-pcl-go-but")
            if len(check_if_many)>0:
                # Если мы нашли более одной организации по ИНН, то извлекаем ссылки на них
                hrefs = [i['href'] for i in soup.find_all(class_="org-pcl-go-but")]

                # Пробегаем по спику ссылок
                for ref in hrefs:
                    url = f'https://synapsenet.ru/searchorganization/proverka-kontragentov?query={ref}'
                    page = requests.get(url)
                    soup = BeautifulSoup(page.content, 'html.parser')
                    # Добавляем объекты bs4 в список soups
                    soups.append(soup)
            else:
                # Если по ИНН найдена одна организация, то добавляем её в список
                soups.append(soup)
            
            # Записываем данные в файл для отладки
            # with open('html.html','w') as file:
            #     file.write(str(soup.contents))

            # with open('html.html','r') as file:
            #     soup1 = BeautifulSoup(file.read(), 'html.parser')

            for one_soup in soups:
                # Собираем необходимые данные с помощью bs4 и получаем словарь
                data_dict = bs4_sandbox.html_scraper(one_soup, tax_id)
                
                # Если несколько организаций с одним ИНН проверяем по КПП:
                duplicates = False
                if len(check_if_many)>0:
                    duplicates = duplicates_check('final/report.xlsx', 'КПП', data_dict['КПП'])

                # Добавляем значения словаря в файл Эксель
                if not duplicates: write_xlsx(data_dict)

    return
