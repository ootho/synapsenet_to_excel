from flask import Flask, request
from files_io import not_exist_or_modified_more_than_day_ago, delete_file
import main, datetime

app = Flask(__name__)

@app.route("/tax_id/", methods=['POST'])
def tax_id():
    tax_id_list = request.get_json()
    date = datetime.datetime.now()
    # получаем список ИНН и передаём в основной цикл
    try:
        if not_exist_or_modified_more_than_day_ago():
            delete_file()
            main.main_loop(tax_id_list, date)
        else:
            main.main_loop(tax_id_list, date)
        # возвращаем ответ об успешной отправке данных
        return "Tax IDs received, the report has been sent!"
    except Exception as x:
        # возвращаем ошибку
        return x