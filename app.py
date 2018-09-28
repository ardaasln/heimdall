from flask import Flask
from src.errors.error_handlers import handle_custom_error
from src.errors.custom_error import CustomError
from src.api.http import Http

app = Flask(__name__)
app.wsgi_app = Http(app.wsgi_app)
app.register_error_handler(CustomError, handle_custom_error)
app.config.from_pyfile('./config/config.py', silent=True)

from src.api.resource.user import bp
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run()

