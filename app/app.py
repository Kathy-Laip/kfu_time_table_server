import sqlalchemy
from connection import Connection
from config import Config
from flask import Flask, request
import pymysql
import json
import re


app = Flask(__name__)
app.config.from_object(Config)
my_db = sqlalchemy.create_engine(Config.SQLALCHEMY_DATABASE_URI)
connection = Connection(my_db)

data = connection.get_data_from_table('select account.id, name, surname, id_groups,login, password from account inner join id_groups on id_gr = id_groups.id;')

@app.route("/signin", methods=["POST"])
def logInUser():
    json_obj = json.loads(request.get_data())
    login = json_obj["login"]
    password = json_obj["password"]

    ans = {}
    data = ''

    dataFromDB = connection.get_data_from_table('select account.id, name, surname, id_groups, login, password from account inner join id_groups on id_gr = id_groups.id where login = "{}" and password = "{}";'.format(login, password))
    if len(dataFromDB) == 0:
        ans["error"] = "true"
        ans["data"] = data
    else: 
        data = dataFromDB[0][3]
        ans["error"] = "false"
        ans["data"] = data


    json_data = json.dumps(ans)

    return json_data

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5050", debug=True)