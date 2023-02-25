import time
from bs4 import BeautifulSoup


def html_scraper(soup, initial_id):
    # функция ставит na если ничего не нашли
    def pick(key_value: dict) -> dict:
        name, eval_list = list(key_value.items())[0]
        info = 'na'
        for i in eval_list:
            try:
                info = eval(i, {"soup": soup, "time": time, "initial_id": initial_id})
                break
            except Exception:
                continue
        return {name: info}

    
    queries=[
        {"ИНН" : ['soup.find(title="Идентификационный номер налогоплательщика").find_next().text', 
                  'initial_id']},

        {"КПП" : ['soup.find(title="Код причины постановки на учет").find_next().text']},

        {"ОГРН" : ['soup.find(title="Основной государственный регистрационный номер").find_next().text']},

        {"Название организации" : ['soup.find(class_="oct-full-title").text', 
                       'soup.title.text.split(',')[0]']},

        {"Статус" : ['soup.find(class_="oc-operating-status").find_next().find_next().text']},

        {"Дата регистрации" : ['soup.find(class_="oc-op-reg-date").text.replace("дата регистрации ", "").strip()']},

        {"Адрес" : ['soup.find(class_="oc-full-adress").text']},

        {"Номер телефона" : ['soup.find(class_="org-contacts-block").find(class_="orgs-open-form").text']},

        {"Электронная почта" : ['soup.find(class_="org-contacts-block").find_next_sibling().find(class_="orgs-open-form").text']},

        {"Последнее изменение адреса" : ['soup.find(class_="org-last-change").text.replace("последнее изменение","").strip()']},

        {"timestamp" : ['str(round(time.time()))']}

    ]

    d = {}
    for query in queries:
        d.update(pick(query))

    # d.update({"name" : query})

    return d

# Для отладки
# with open('html.html','r') as file:
#     soup1 = BeautifulSoup(file.read(), 'html.parser')
#     html_scraper(soup1)
