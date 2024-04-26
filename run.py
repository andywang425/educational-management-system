from waitress import serve
from app import app


print('Start serving on http://0.0.0.0:80')
serve(app, host='0.0.0.0', port=80)
