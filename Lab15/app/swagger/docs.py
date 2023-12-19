from flask_swagger_ui import get_swaggerui_blueprint
from yaml import load, Loader

SWAGGER_URL = "/api/docs"
API_URL = "E:\\Лабораторні\\3 курс\\Python WEB\\Lab15\\app\\swagger\\users.yaml"

swagger_yml = load(open(API_URL, 'r'), Loader=Loader)

swagger_bp = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'spec': swagger_yml
    }
)
