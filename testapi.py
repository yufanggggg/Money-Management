from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask import request
import pymysql
import pymysql.cursors
app = Flask(__name__ )
#Restful API
api=Api(app)
cost=['交通','飲食','生活','娛樂','其他支出','投資']
earning=['薪水','獎金','獲利','意外財','其他收入']
class UserList(Resource):
    def __init__(self,asset):
        self.__asset=asset
        self.balance=asset
    def get(self):
        try:
            conn=pymysql.connect(host='localhost',
                            user='root',
                            password='987654321',
                            database='Money Management',
                            )   
            cursor=conn.cursor()
            cursor.execute("""select * from `record`""")
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def post(self,j,money):
        try:
            conn=pymysql.connect(host='localhost',
                            user='root',
                            password='987654321',
                            database='Money Management',
                            )   
            cursor=conn.cursor()
            _account = request.form['account']
            _pwd = request.form['pwd']
            insert_user_cmd = """INSERT INTO otg_demo_users(name, age, city) 
                                VALUES(%s, %s, %s)"""
            cursor.execute(insert_user_cmd, (_name, _age, _city))
            conn.commit()
            response = jsonify(message='User added successfully.', id=cursor.lastrowid)
            #response.data = cursor.lastrowid
            response.status_code = 200
        except Exception as e:
            print(e)
            response = jsonify('Failed to add user.')         
            response.status_code = 400 
        finally:
            cursor.close()
            conn.close()
            return(response)
            
#Get a user by id, update or delete user
class User(Resource):
    def get(self, user_id):
        try:
            conn=pymysql.connect(host='localhost',
                            user='root',
                            password='987654321',
                            database='Money Management',
                            )   
            cursor=conn.cursor()
            cursor.execute('select * from otg_demo_users where id = %s',user_id)
            rows = cursor.fetchall()
            return jsonify(rows)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    def put(self, user_id):
        try:
            conn=pymysql.connect(host='localhost',
                            user='root',
                            password='987654321',
                            database='Money Management',
                            )   
            cursor=conn.cursor()
            _name = request.form['name']
            _age = request.form['age']
            _city = request.form['city']
            update_user_cmd = """update otg_demo_users 
                                 set name=%s, age=%s, city=%s
                                 where id=%s"""
            cursor.execute(update_user_cmd, (_name, _age, _city, user_id))
            conn.commit()
            response = jsonify('User updated successfully.')
            response.status_code = 200
        except Exception as e:
            print(e)
            response = jsonify('Failed to update user.')         
            response.status_code = 400
        finally:
            cursor.close()
            conn.close()    
            return(response)       

    def delete(self, user_id):
        try:
            conn=pymysql.connect(host='localhost',
                            user='root',
                            password='987654321',
                            database='Money Management',
                            )   
            cursor=conn.cursor()
            cursor.execute('delete from otg_demo_users where id = %s',user_id)
            conn.commit()
            response = jsonify('User deleted successfully.')
            response.status_code = 200
        except Exception as e:
            print(e)
            response = jsonify('Failed to delete user.')         
            response.status_code = 400
        finally:
            cursor.close()
            conn.close()    
            return(response)       

#API resource routes
api.add_resource(UserList, '/users', endpoint='users')
api.add_resource(User, '/user/<int:user_id>', endpoint='user')
if (__name__) == ('__main__'):
    app.run(debug=True)