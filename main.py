from flask import Flask, request
import scraper

app = Flask(__name__)

@app.route("/tax_id/", methods=['POST'])
def tax_id():
    tax_id_list = request.get_json()
    # получаем список ИНН и передаём в основной цикл
    try:
        scraper.scraper_main_loop(tax_id_list)
        # возвращаем ответ об успешной отправке данных
        return "Tax IDs received, the report has been sent!"
    except Exception as x:
        # возвращаем ошибку
        return x