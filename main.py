from flask import Flask, request
import files_io
import scraper

app = Flask(__name__)

'''
["7721793895",
"7736050003",
"7710140679"]
'''

# Газпром по ИНН "7736050003" сразу две организации, брать обе

@app.route("/tax_id/", methods=['POST'])
def tax_id():
    data = request.get_json()
    # сохраняем список ИНН
    path = 'file.txt'
    files_io.write_json_array(data, path)
    # сохраняем файл со временем последнего запроса
    files_io.timestamp()
    # обращаемся к synapsenet и получаем html по списку ИНН
    scraper.scraper_main_loop(path)
    return "Tax ids received!"

@app.route("/synapse_responce/", methods=['POST'])
def synapse_responce():
    data = request.get_json()
    file_name = data['ИНН']
    path = str(f'temp_data/{file_name}')
    files_io.write_json_array(data, path)
    return "Json received succesfully!"

# @app.route("/write_xlsx/", methods=['POST'])
# def write_xlsx():
#     files_io.write_xlsx()
#     return "Write is done!"
