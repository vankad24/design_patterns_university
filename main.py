import connexion
from flask import request

from src.core.response_format import ResponseFormat
from src.logics.response_csv import ResponseCsv
from src.models.product_group import ProductGroupModel

app = connexion.FlaskApp(__name__)

"""
Проверить доступность REST API
"""
@app.route("/api/accessibility", methods=['GET'])
def formats():
    return "SUCCESS"

"""
Получить csv модель
"""
@app.route("/api/get_csv", methods=['GET'])
def return_csv():
    data = [ProductGroupModel.create("test")]
    result = ResponseCsv().build(ResponseFormat.CSV, data)
    return result


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
