from flask import Flask
from flask_cors import CORS
from api import Api
from datetime import timedelta
from utils import generate_secret_key


app = Flask(__name__, static_folder='vue-edu-management-sys/dist', static_url_path="/vue-edu-management-sys/dist")
app.secret_key = generate_secret_key()
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
# app.config["SESSION_COOKIE_SAMESITE"] = "None"
# app.config["SESSION_COOKIE_SECURE"] = False
CORS(app, origins='*', supports_credentials=True)

app.register_blueprint(Api, url_prefix='/api')


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file(path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
