from flask import Flask
from flask_mysqldb import MySQL
from config import config

app = Flask(__name__)

connection = MySQL(app)


@app.route('/test')

def property_available():
    try:
        return "ok"

    except Exception as ex:
        return "Error"


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()
