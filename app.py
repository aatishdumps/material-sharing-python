from flask import Flask
import pymysql
from flaskext.mysql import MySQL

app = Flask(__name__)

app.secret_key = "secret_key"
app.config["APP_NAME"] = "ScholarShare"
app.config["MYSQL_DATABASE_HOST"] = "localhost"
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "aatishk60"
app.config["MYSQL_DATABASE_DB"] = "flask"

mysql = MySQL(app,cursorclass=pymysql.cursors.DictCursor)
mydb = mysql.connect()
mycursor = mydb.cursor()


@app.context_processor
def inject_app_name():
    return {"APP_NAME": app.config["APP_NAME"]}


from routes import *

if __name__ == "__main__":
    app.run(debug=True)
