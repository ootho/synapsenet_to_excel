import time, re
from bs4 import BeautifulSoup

def html_scraper(soup, initial_id):
    def pick(key_value: dict) -> dict:
        name, eval_list = list(key_value.items())[0]
        info = ''
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

        {"timestamp" : ['str(round(time.time()))']},

        {"КПП" : ['soup.find(title="Код причины постановки на учет").find_next().text']},

        {"ОГРН" : ['soup.find(title="Основной государственный регистрационный номер").find_next().text']},

        {"Название организации" : ['soup.find(class_="oct-full-title").text if soup.find(class_="oct-full-title") else soup.find(class_="org-card-title oct-with-flag").find("h1").text', 
                       'if not "Проверка контрагента" in soup.title.text.split(",")[0] else soup.title.text.split(",")[0]']},

        {"Статус" : ['soup.find(class_="oc-operating-status").find_next().find_next().text']},

        {"Дата регистрации" : ['soup.find(class_="oc-op-reg-date").text.replace("дата регистрации ", "").strip()']},

        {"Адрес" : ['soup.find(class_="oc-full-adress").text']},

        {"Номер телефона" : ['soup.find(class_="org-contacts-block").find(class_="orgs-open-form").text']},

        {"Электронная почта" : ['soup.find(class_="org-contacts-block").find_next_sibling().find(class_="orgs-open-form").text']},

        {"Последнее изменение адреса" : ['soup.find(class_="org-last-change").text.replace("последнее изменение","").strip()']},

        {"Директор" : ['soup.find(class_="org-director-block").find_next().find_next().text']},

        {"Директор назначен" : ['soup.find(class_="org-director-block").find(class_="org-last-change").text']},

        {"Реестр СМиСП" : ['soup.find(class_="org-smp-block").find_next().text']},

        {"ОКПО" : ['[x.find_next().find_next().text for x in soup.find_all(class_="oc-okpo-line") if x.find_next().text == "ОКПО"][0]']},

        {"ОКАТО" : ['[x.find_next().find_next().text for x in soup.find_all(class_="oc-okpo-line") if x.find_next().text == "ОКАТО"][0]']},

        {"ОКТМО" : ['[x.find_next().find_next().text for x in soup.find_all(class_="oc-okpo-line") if x.find_next().text == "ОКТМО"][0]']},

        {"ОКФС" : ['[x.find_next().find_next().text for x in soup.find_all(class_="oc-okpo-line") if x.find_next().text == "ОКФС"][0]']},

        {"ОКОГУ" : ['[x.find_next().find_next().text for x in soup.find_all(class_="oc-okpo-line") if x.find_next().text == "ОКОГУ"][0]']},

        {"ОКОПФ" : ['[x.find_next().find_next().text for x in soup.find_all(class_="oc-okpo-line") if x.find_next().text == "ОКОПФ"][0]']},

        {"ПФР" : ['soup.find(title="Пенсионный фонд России").find_next().find("strong").text']},

        {"ФСС" : ['soup.find(title="Фонд социального страхования").find_next().find("strong").text']},

        {"Топ 5 поставщиков" : ['str([i.text for i in soup.find("div", {"class":"osb-top-script", "data-toptype":"1"}).find(class_="oc-top-table").find_all("a", {"class":"org-link"})])']},

        {"Топ 5 заказчиков" : ['str([i.text for i in soup.find("div", {"class":"osb-top-script", "data-toptype":"2"}).find(class_="oc-top-table").find_all("a", {"class":"org-link"})])']}
        
    ]

    d = {}
    for query in queries:
        d.update(pick(query))

    try:
        for i in soup.find(class_="org-card-right-column").find_all(class_="org-card-right"):
            if "Краткая справка" in str(i.find(class_="org-card-h2")):
                source = str(i.find(class_="org-card-footnote"))
                pattern = r'<p>Основной вид деятельности — «(.*?)»\.</p>'
                match = re.search(pattern, source)
                info = match.group(1)
            d.update({"Основной вид деятельности" : info})
    except Exception as x:
        # print(x)
        pass

    for n in range(1,4):
        soup_array = soup.find("table",{"data-fintype":n})
        if soup_array:
            for i in soup_array.children:
                try:
                    name = ["Баланс ","Выручка ", "Прибыль "][n] + i.find("td").text
                    info = i.find("td").find_next().text.replace('\xa0','')
                    d.update({name : float(info)})
                except Exception as x:
                    # print(x)
                    pass

    for n in range (1,5):
        try:
            for i in soup.find("table",{"data-indicators":n}).children:
                d.update({i.find("td").text : i.find("td").find_next().find_next().text.replace('\xa0','')})
        except Exception as x:
            # print(x)
            pass

    for n in ["Истец в делах", "Ответчик в делах", "Производств с долгом", "Производств завершено"]:
        try:
            d.update({n : soup.find(text=n.lower()).find_next().text})
        except Exception as x:
            # print(x)
            pass

    try:
        for c,i in enumerate(soup.find_all("div",{"data-tendertype":"1"})[1].children):
            if c<4:
                name = f"В роли заказчика {i.find_next().text}"
                data = i.find_next().find_next().text.replace('\xa0','')
                d.update({name : data})
                del name, data
    except Exception as x:
        # print(x)
        pass

    try:
        for c,i in enumerate(soup.find_all("div",{"data-tendertype":"2"})[1].children):
            if c<2:
                name = f"В роли поставщика {i.find_next().text}"
                data = i.find_next().find_next().text.replace('\xa0','')
                d.update({name : data})
                del name, data
    except Exception as x:
        # print(x)
        pass

    for n in ["Связанные организации", "Правопреемство", "Дочерние организации", "Филиалы"]:
        try:
            info = soup.find(text=n.lower()).find_next().text
            d.update({n : info})
        except Exception as x:
            # print(x)
            pass
           
    for n in ["Связанные организации", "Правопреемство", "Дочерние организации", "Филиалы"]:
        try:
            info = soup.find(text=n.lower()).find_next().text
            d.update({n : info})
        except Exception as x:
            # print(x)
            pass

    # d.update({"name" : query})

    return d

# Для отладки
# with open('html.html','r') as file:
#     soup1 = BeautifulSoup(file.read(), 'lxml')
#     print(html_scraper(soup1, '7736050003'))
