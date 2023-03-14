import datetime

from flask import Flask, request

import main
from files_io import not_exist_or_modified_more_than_day_ago,\
                     delete_file, copy_template

app = Flask(__name__)


@app.route("/tax_id/", methods=['POST'])
def tax_id():
    date = datetime.datetime.now()
    # Проверяем данные на адекватность
    tax_id_list = request.get_json()
    try:
        # Если файл старый, то удаляем
        if not_exist_or_modified_more_than_day_ago():
            delete_file()
            # Копируем темплейт в папку
            copy_template()
            main.main_loop(tax_id_list, date)
        else:
            # Если файл модицифирован менее дня назад, то принимаем, 
            # что произошла ошибка и дописываем в него
            main.main_loop(tax_id_list, date)
        # Возвращаем ответ об успешной отправке данных
        return "Tax IDs received, the report has been sent!"
    except Exception as x:
        # возвращаем ошибку
        return x
