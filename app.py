from flask_restful import Resource, Api
from flask import Flask #載入模組
from flask import render_template,redirect,url_for,session, request
from flask import flash #將訊息由後端傳到前端

# from flask_restful import Resource, Api #Flask Restful 

import pymysql
import pymysql.cursors
#建立物件，表整個伺服器運作。也可以設定靜態檔案路徑處理(加入更多參數)
conn=pymysql.connect(host='localhost',
                            user='root',
                            password='987654321',
                            database='Money Management',
                            )   
cursor=conn.cursor()
app = Flask(__name__ ,
static_folder="templates",#靜態檔案的資料夾名稱，預設為:static
static_url_path="/"#靜態檔案對應的網址路徑，預設為:/static
) #所有在templates資料夾底下的檔案，都對應到網址路徑/檔案名稱
app.secret_key='abc'


@app.route('/')
def home():
    return render_template('register.html')

@app.route("/register",methods=["POST"])
def new_member():
    account=request.form['account']
    pwd=request.form['pwd']
    check_sql='select `member_account` from `sign-in-member`'
    cursor.execute(check_sql)
    
    result=cursor.fetchall()
    # print(result)
    result_set=set()
    for i in range(len(result)):
        result_set.add(result[i][0])

    # print(result_set)
    if account in result_set:
        message=flash('帳號已被註冊')
        return render_template('register_again.html')
    else:
        sql = "INSERT INTO `sign-in-member` (`member_account`, `member_pwd`) VALUES (%s, %s)"
        cursor.execute(sql, (account, pwd))
        conn.commit()
        print("新帳號")
        return render_template('login_first.html',account=account)

@app.route('/error')
def error():
    message=request.args.get('msg')
    return render_template('error.html',message=message)

@app.route('/start')
def login():
    return render_template('login.html')

@app.route('/login',methods=["POST"])
def membercheck():
    loginaccount=request.form['account']
    loginpwd=request.form['pwd']
    check_sql='SELECT * from `sign-in-member`'
    cursor.execute(check_sql)
    result=cursor.fetchall()
    print(result)
    print(type(result))
    
    for i in range(len(result)):
        if loginaccount in result[i][0] and loginaccount !="":
            if loginpwd == result[i][1]:
                session['memberacc']=loginaccount
                session['memberpwd']=loginpwd
                return render_template('index.html')
            else:
                loginaccount=request.form['account']
                return redirect('/login_again')

        else:
            continue
        message=flash('帳號不存在，請註冊')
        return render_template('register_again.html')


@app.route('/member')
def index():
    if  'memberacc' and 'memberpwd' in session:    
        return render_template("index.html")
    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    del session['memberacc']
    del session['memberpwd']
    return render_template("login.html")

@app.route('/login_again')
def login_again():
    flash('Wrong Password')
    
    return redirect("login_again.html")

# Restful API
api=Api(app)
class TEST(Resource):
    def get(self,accountid):

        return member
    def post(self,accountid):
        return {'message':'hello world'}
api.add_resource(TEST, '/test')

if (__name__) == ('__main__'):
    app.run(debug=True) #啟動網站伺服器，可透過port參數設定阜號