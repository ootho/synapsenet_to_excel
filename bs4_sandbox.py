from bs4 import BeautifulSoup
import requests
from scraper import write_xlsx

with open('html.html','r') as file:
    page = file.read()

soup = BeautifulSoup(page, 'html.parser')

d = {}
d.update({"ИНН" : soup.find(title="Идентификационный номер налогоплательщика").find_next().text})
d.update({"Название" : soup.find(class_="oct-full-title").text})
d.update({"ОГРН" : soup.find(title="Основной государственный регистрационный номер").find_next().text})
d.update({"КПП" : soup.find(title="Код причины постановки на учет").find_next().text})
d.update({"Статус" : soup.find(class_="oc-operating-status").find_next().find_next().text})
d.update({"Дата регистрации" : soup.find(class_="oc-op-reg-date").text.replace('дата регистрации ', '').strip()})
d.update({"Адрес" : soup.find(class_="oc-full-adress").text})
d.update({"Последнее изменение адреса" : soup.find(class_="org-last-change").text.replace('последнее изменение','').strip()})
d.update({"Номер телефона" : soup.find(class_="org-contacts-block").find(class_="orgs-open-form").text})
d.update({"Электронная почта" : soup.find(class_="org-contacts-block").find_next_sibling().find(class_="orgs-open-form").text})

# [print(i) for i in d.items()]
#возвращаем словарь с полями для заполнения документа

write_xlsx(d)
