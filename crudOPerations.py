from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL
import os


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = os.environ['user_name']
app.config['MYSQL_PASSWORD'] = os.environ['password']
app.config['MYSQL_DB'] = 'flaskCrud'

mysql = MySQL(app)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS user (id INT AUTO_INCREMENT PRIMARY KEY, \
                    name VARCHAR(20), email VARCHAR(50))")
        table = "INSERT INTO user (name, email) VALUES (%s, %s)"
        val = (name, email)
        cur.execute(table, val)
        mysql.connection.commit()
        cur.close()
        return "Data inserted successfully"
    return render_template("create.html")


if __name__ == "__main__":
    app.run(debug=True)