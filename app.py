from flask import Flask
from src.errors.error_handlers import handle_custom_error
from src.errors.custom_error import CustomError
from src.api.http import Http
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.wsgi_app = Http(app.wsgi_app)
app.register_error_handler(CustomError, handle_custom_error)
app.config.from_pyfile('./config/config_dev.py', silent=True)

from src.api.resource.user import bp
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run()

