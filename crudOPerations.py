from flask import Flask
from flask_mysqldb import MySQL
import os


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.environ['user_name']
app.config['MYSQL_PASSWORD'] = os.environ['password']
app.config['MYSQL_DB'] = 'flaskCrud'

mysql = MySQL(app)

if __name__ == "__main__":
    app.run(debug=True)