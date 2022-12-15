from flask import Flask #載入模組
from flask import render_template,redirect,url_for,session, request
from flask import flash #將訊息由後端傳到前端
from flask_wtf import Form
from wtforms import *
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
                return render_template('index.html',account=loginaccount)
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
        return render_template("index.html",account=session['memberacc'])
    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    print(session)
    del session['memberacc']
    del session['memberpwd']
    print(session)
    return render_template("login.html")

@app.route('/login_again')
def login_again():
    flash('Wrong Password')
    
    return redirect("login_again.html")

@app.route('/record', methods = ['POST'])
def record_create():
    b=request.form.to_dict()
    print(b)
    #前端空值處理
    if b['Cost'] =="":
        b['Cost']=0
    if b['Income'] =="":
        b['Income']=0
    if b['Balance']=="新增":
        b['Balance']=int(b['Income'])-int(b['Cost'])
    


    #查閱資料庫
    select_sql="select `Date`,`class`,`income`,`spent`,`balance` from `record`"
    cursor.execute(select_sql)
    records=cursor.fetchall()
    print(records)
    num=len(records)

    # balance處理  
    if num>0:
        sum_balance=[]
        for i in range(num):
            sum_balance.append(records[i][-1])
        b['Balance']=sum_balance[-1]+b['Balance']
    else:
        b['Balance']=b['Balance']

    #寫入資料庫
    insert_sql="INSERT INTO `record` (`Date`,`class`,`income`,`spent`,`balance`) VALUES(%s,%s,%s,%s,%s)" 
    val=(b['Date'],b['Money_Class'],int(b['Income']),int(b['Cost']),b['Balance'])
    cursor.execute(insert_sql, val)
    conn.commit()


    # 更新balance
    update_sql="update `record` set balance= %s "
    cursor.execute(update_sql, b['Balance'])
    conn.commit()
    
    
    return render_template("record.html"
    ,num=num,records=records
    ,Date=b['Date'],Money_Class=b['Money_Class'],Income=int(b['Income']),Cost=int(b['Cost']),Balance=b['Balance']
    )

#刪除
@app.route('/delete',methods = ['GET'])
def delete():
    b=request.form.to_dict()

    #查閱資料庫
    select_sql="select `Date`,`class`,`income`,`spent`,`balance` from `record`"
    cursor.execute(select_sql)
    records=cursor.fetchall()
    num=len(records)
    print(records)
    # balance處理  
    if num>0:
        sum_balance=[]
        for i in range(num):
            sum_balance.append(records[i][-1])
        b['Balance']=sum_balance[-1]+records[i][-2]-records[i][-3]
    else:
        b['Balance']=0

    # 更新balance
    update_sql="update `record` set balance= %s "
    cursor.execute(update_sql, b['Balance'])
    conn.commit()

    #資料庫更新
    delete_sql="delete FROM `money management`.record where `NO` = (SELECT * FROM (SELECT MAX(NO) FROM `money management`.record )AS A)"
    cursor.execute(delete_sql)
    conn.commit()
    return render_template("delete.html",num=num,records=records,Balance=b['Balance'])

#至修改mode
@app.route('/editmode',methods = ['GET'])
def edit_mode():
    b=request.form.to_dict()
    #查閱資料庫
    select_sql="select `Date`,`class`,`income`,`spent`,`balance` from `record`"
    cursor.execute(select_sql)
    records=cursor.fetchall()
    print(records)
    num=len(records)

    # balance處理  
    if num>0:
        sum_balance=[]
        for i in range(num):
            sum_balance.append(records[i][-1])
        b['Balance']=sum_balance[-1]+records[i][-2]-records[i][-3]
    else:
        b['Balance']=0

    # 更新balance
    update_sql="update `record` set balance= %s "
    cursor.execute(update_sql, b['Balance'])
    conn.commit()
    return render_template("editmode.html"
    ,num=num,records=records,Balance=b['Balance']
    )

@app.route('/submit_update',methods = ['GET'])
def submit_update():
    b=request.form.to_dict()
    print(b)
    print(request.args.get('edit_Date'))
    #查閱資料庫
    select_sql="select `Date`,`class`,`income`,`spent`,`balance` from `record`"
    cursor.execute(select_sql)
    records=cursor.fetchall()
    print(records)
    num=len(records)
        #日期
    if request.args.get('edit_Date')!=records[-1][0]:
        update_date_sql="update record set date = %s where `NO` = (SELECT * FROM (SELECT MAX(NO) FROM record )AS A)"
        cursor.execute(update_date_sql,b['Date'])
        conn.commit()
    #金錢類別
    if request.args.get('edit_Money_Class')!=records[-1][1]:
        update_class_sql="update record set class = %s where `NO` = (SELECT * FROM (SELECT MAX(NO) FROM record )AS A)"
        cursor.execute(update_class_sql.b['Money_Class'])
        conn.commit()
    #金額
    if request.args.get('edit_Income')!=records[-1][2]:
        update_incomemoney_sql="update record set Income = %s where `NO` = (SELECT * FROM (SELECT MAX(NO) FROM record )AS A)"
        cursor.execute(update_incomemoney_sql,b['Income'])
        conn.commit()
    if request.args.get('edit_Cost')!=records[-1][3]:
        update_costmoney_sql="update record set cost = %s where `NO` = (SELECT * FROM (SELECT MAX(NO) FROM record )AS A)"
        cursor.execute(update_costmoney_sql,b['Cost'])
        conn.commit()
    return render_template("record.html"
    ,num=num,records=records
    ,Date=b['edit_Date'],Money_Class=b['edit_Money_Class'],Income=int(b['edit_Income']),Cost=int(b['Cost']),Balance=b['edit_Balance']
    )


#    # balance處理  
#     if num>0:
#         sum_balance=[]
#         for i in range(num):
#             sum_balance.append(records[i][-1])
#         b['Balance']=sum_balance[-1]+records[i][-2]-records[i][-3]
#     else:
#         b['Balance']=0

#     # 更新balance
#     update_sql="update `record` set balance= %s "
#     cursor.execute(update_sql, b['Balance'])
#     conn.commit()

    # return render_template("record.html"
    # ,num=num,records=records
    # ,Balance=b['Balance']
    # )

#至修改送出

# @app.route('/updatesubmit',methods = ['GET'])
# def updatesubmit():

#     #查閱資料庫
#     select_sql="select `Date`,`class`,`income`,`spent`,`balance` from `record`"
#     cursor.execute(select_sql)
#     records=cursor.fetchall()
#     num=len(records)
#     #資料庫更新
#     b=request.form.to_dict()
#     print(b)

if (__name__) == ('__main__'):
    app.run(debug=True) #啟動網站伺服器，可透過port參數設定阜號