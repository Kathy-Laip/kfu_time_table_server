import sqlalchemy
from connection import Connection
from config import Config
from flask import Flask, request
import pymysql


app = Flask(__name__)
app.config.from_object(Config)
my_db = sqlalchemy.create_engine(Config.SQLALCHEMY_DATABASE_URI)
connection = Connection(my_db)
print('Connection')
data = connection.get_data_from_table('select * from account;')

print(data)

