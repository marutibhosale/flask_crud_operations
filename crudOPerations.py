from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL
import os
from jinja2 import UndefinedError


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


@app.route('/show')
def show():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user")
    data = cur.fetchall()
    cur.close()
    return render_template("show.html", data=data)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == "POST":
        if request.form['update']:
            name = request.form['name']
            email = request.form['email']

            cur = mysql.connection.cursor()
            cur.execute("""UPDATE user SET name=%s, email=%s WHERE id=%s""", (name, email, id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for("show"))

    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE id=%s", (id,))
        data = cur.fetchall()
        cur.close()
        return render_template("update.html", data=data)
    except UndefinedError:
        return "Sorry! id " + str(id) + " not exist"

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if request.method == "POST":
        cur = mysql.connection.cursor()
        cur.execute("""DELETE FROM user WHERE id=%s""", (id,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("show"))

    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE id=%s", (id,))
        data = cur.fetchall()
        cur.close()
        return render_template("delete.html", data=data)
    except UndefinedError:
        return "Sorry! id " + str(id) + " not exist"


if __name__ == "__main__":
    app.run(debug=True)