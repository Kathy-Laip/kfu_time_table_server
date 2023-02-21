import sqlalchemy
from connection import Connection
from config import Config
from flask import Flask, request
import excel
import pymysql
import json
import re


app = Flask(__name__)
app.config.from_object(Config)
my_db = sqlalchemy.create_engine(Config.SQLALCHEMY_DATABASE_URI)
connection = Connection(my_db)

data = connection.get_data_from_table('select account.id, name, surname, id_groups,login, password from account inner join id_groups on id_gr = id_groups.id;')

# time_table_groups = excel.get_timetable()

table_group = connection.get_data_from_table('select * from id_groups')

def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

gr = {}
for i in range(len(table_group)):
    gr[table_group[i][0]] = table_group[i][1]

# n = 1
# for i in range(len(time_table_groups)):
#     value = get_key(gr, time_table_groups[i]['group'])
#     connection.execute_query('insert into timetable.table(id, id_group, week, day, time, subject, teacher, classroom, address) values ({},{},"{}","{}","{}","{}","{}","{}","{}")'.format(n, value, time_table_groups[i]['week'], time_table_groups[i]['day'], time_table_groups[i]['time'], time_table_groups[i]['subject'], time_table_groups[i]['teacher'], time_table_groups[i]['classroom'], time_table_groups[i]['address']))
#     n += 1

time_table_end = connection.get_data_from_table('select * from timetable.table')
print(time_table_end)


@app.route("/signin", methods=["POST"])
def log_in_user():
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

@app.route('/get_timetable', methods=["POST"])
def get_timetable():
    json_obj = json.loads(request.get_data())
    group = json_obj["group"]
    time_table_odd = []
    time_table_even = []

    time_table_end = connection.get_data_from_table('select * from timetable.table')
    get_group_value = get_key(gr, group)
    for i in range(len(time_table_end)):
        if(time_table_end[i][1] == get_group_value):
            time_table_end[i][2].replace('[', '').replace(']', '').replace('\'', '')
            if(time_table_end[i][2] == 'н/н'):
                time_table_odd.append({
                    "day" : time_table_end[i][3],
                    "time": time_table_end[i][4],
                    "subject": time_table_end[i][5],
                    "teacher": time_table_end[i][6],
                    "classroom": time_table_end[i][7],
                    "address": time_table_end[i][8]
                })
            elif(time_table_end[i][2] == 'ч/н'):
                time_table_even.append({
                    "day" : time_table_end[i][3],
                    "time": time_table_end[i][4],
                    "subject": time_table_end[i][5],
                    "teacher": time_table_end[i][6],
                    "classroom": time_table_end[i][7],
                    "address": time_table_end[i][8]
                })
            else:
                time_table_odd.append({
                    "day" : time_table_end[i][3],
                    "time": time_table_end[i][4],
                    "subject": time_table_end[i][5],
                    "teacher": time_table_end[i][6],
                    "classroom": time_table_end[i][7],
                    "address": time_table_end[i][8]
                })
                time_table_even.append({
                    "day" : time_table_end[i][3],
                    "time": time_table_end[i][4],
                    "subject": time_table_end[i][5],
                    "teacher": time_table_end[i][6],
                    "classroom": time_table_end[i][7],
                    "address": time_table_end[i][8]
                })
    return time_table_even, time_table_odd



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5050", debug=True)