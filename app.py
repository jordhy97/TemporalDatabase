from flask import Flask

import psql

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    psql.connect('database.ini')
    app.run()