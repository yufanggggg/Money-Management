from flask import Flask #載入模組
from flask import render_template,redirect,url_for,session, request
from flask import flash #將訊息由後端傳到前端
from flask_wtf import Form
from wtforms import *
import pymysql
import pymysql.cursors
# import matplotlib
# import matplotlib.pyplot as plt
# from matplotlib.font_manager import FontProperties as font
import json

# font1= font(fname="C:/Users/User/Downloads/text_props.py")
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

#查詢當前資料庫函式
def record_database(account):
    select_sql=f"select `Date`,`class`,`income`,`spent`,`balance` from {account}"
    cursor.execute(select_sql)
    records=cursor.fetchall()
    return records

#更新資料庫Balance函式
def update_balance(loginaccount,e):
    update_sql=f"update {loginaccount} set balance= %s "
    cursor.execute(update_sql,e)
    conn.commit()

#刪除支出資料庫函式
def delete_cost(loginaccount,b,c,d,e):
    delete_sql=f"delete FROM {loginaccount} where `Date`= (SELECT * FROM (SELECT `Date` FROM {loginaccount} where class = %s and Date = %s )AS A where `spent`= %s or `income` = %s)"
    cursor.execute(delete_sql,(b,c,d,e))
    conn.commit()

#刪除收入資料庫函式
def delete_income(loginaccount,b,c,d,e):
    delete_sql=f"delete FROM {loginaccount} where `Date`= (SELECT * FROM (SELECT `Date`  FROM {loginaccount} where class = %s and Date = %s )AS A where `spent`= %s or `income` = %s)"
    cursor.execute(delete_sql,(b,c,d,e))
    conn.commit()

#新增資料函式
def insert_record(loginaccount,a,b,c,d,e):
    insert_sql=f"INSERT INTO {loginaccount} (`Date`,`class`,`income`,`spent`,`balance`) VALUES(%s,%s,%s,%s,%s)" 
    val=(a,b,c,d,e)
    cursor.execute(insert_sql, val)
    conn.commit()

#新增table
def create_table(account):
    create_table=f"CREATE TABLE IF NOT EXISTS {account} ( `Date` Date NOT NULL,\
    `class` varchar(20) NOT NULL,\
    `income` int(20) NOT NULL,\
    `spent` int(20) NOT NULL, \
    `balance` int(20) NOT NULL \
    )"
    cursor.execute(create_table)
    conn.commit()


@app.route('/testing')
def testing():
    
    return session


@app.route('/')
def home():
    return render_template('register.html')

@app.route("/register",methods=["POST"])
def new_member():
    try:
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
            message='帳號已被註冊'
            return render_template('register.html',message=message)
        else:
            sql = "INSERT INTO `sign-in-member` (`member_account`, `member_pwd`) VALUES (%s, %s)"
            cursor.execute(sql, (account, pwd))
            conn.commit()
            print("新帳號")
            message=f'{account}註冊成功，請登入'
            return render_template('login.html',account=account,message=message)
    except: print('faliure')

@app.route('/start')
def login():
    return render_template('login.html')

@app.route('/login',methods=["POST"])
def membercheck():
    loginaccount=request.form['account']
    print(f'loginaccount: {loginaccount}')
    loginpwd=request.form['pwd']
    print(f'loginpwd: {loginpwd}')
    check_sql='SELECT * from `sign-in-member`'
    cursor.execute(check_sql)
    result=cursor.fetchall()
    account_set=set()
    pwd_set=set()
    for i in range(len(result)):
        account_set.add(result[i][0])
    for i in range(len(result)):
        pwd_set.add(result[i][1])
    print(result)
    print(account_set)
    print(pwd_set)
    print(type(result))
    
    for i in range(len(result)):
        if loginaccount in account_set:
            print('true')
            if loginpwd in pwd_set:
                if loginpwd == result[i][1]:
                    print('match')
                    session['memberacc']=loginaccount
                    session['memberpwd']=loginpwd
                    print(f'loginaccount:{loginaccount},memberpwd:{loginpwd}')
                    create_table(loginaccount)
                    return redirect('/index.html')
                else:
                    continue
            else:
                return redirect('/login_again')

        else:
            print('帳號不存在，請註冊')
            message='帳號不存在，請註冊'
            return render_template('register.html',message=message)
            break
        
        


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
    message=f'期待再次見到您！'
    return render_template("login.html",message=message)

@app.route('/login_again')
def login_again():
    message=f'密碼錯誤，請重新登入'
    return render_template("login.html",message=message)

@app.route('/record', methods = ['POST','GET'])
def record_create():
    loginaccount=session['memberacc'] 
    a=request.args.get('id')   
    b=request.form.to_dict()
    print(f'a:{a},b:{b}')

#查閱資料庫
    records=record_database(loginaccount)
    print(records)
    num=len(records)

    #有新增資料
    if b !={}: 
        #前端空值處理
        if b['Cost'] =="":
            b['Cost']=0
        if b['Income'] =="":
            b['Income']=0
        if b['Balance']=="新增" :
            b['Balance']=int(b['Income'])-int(b['Cost'])

        #balance處理 
        if num>0: #新增前已有資料存在
            b['Balance']=records[-1][-1]+b['Balance']

            print('original DB with record,now balance is changed:' + str(b['Balance']))
        else:
            b['Balance']=b['Balance']

            print('original DB without record,balance is update:'+str(b['Balance']))

        #寫入資料庫
        insert_record(loginaccount,b['Date'],b['Money_Class'],int(b['Income']),int(b['Cost']),b['Balance'])

        # 更新balance
        update_balance(loginaccount,b['Balance'])
    
        return render_template("tables.html",num=num,records=records,b=b
    ,Date=b['Date'],Money_Class=b['Money_Class'],Income=int(b['Income']),Cost=int(b['Cost']),Balance=b['Balance'],account=loginaccount
    )

    #無新增資料
    else:
        records=record_database(loginaccount)
        print(records)
        num=len(records)

        if num>0: #當前有資料存在
           Balance=records[-1][-1]
        else:
            Balance=0

        print(f'b is empty {records},balance:{Balance}')
        
        return render_template("tables.html",num=num,records=records,Balance=Balance,account=loginaccount)

#刪除
@app.route('/delete', methods = ['POST','GET'])
def delete():
    loginaccount=session['memberacc']
    a=request.args.get('id')
    print(f'id:{a}')
    print(type(a))
    #查閱刪除前資料庫
    records=record_database(loginaccount)
    num=len(records)
    print(records)
    date_value=records[int(a)][0]
    class_name=records[int(a)][1]
    income_value=records[int(a)][2]
    cost_value=records[int(a)][3]

    #刪除項目
    print(f'delete item:{records[int(a)][1]}, income:{records[int(a)][2]}, cost:{records[int(a)][3]}')
    
    #當前紀錄超過一筆
    if num>1:
        #刪除項目為支出
        if records[int(a)][2]==0:
            print(f'cost is:{records[int(a)][3]}')
            
            #資料庫Balance更新
            Balance=records[int(a)][-1]+records[int(a)][-2]-records[int(a)][-3]
            print(f'original balance:{records[int(a)][-1]};new balance:{Balance}')
            update_balance(loginaccount,Balance)

            #資料庫刪除指令
            delete_cost(loginaccount,class_name,date_value,cost_value,cost_value)

            #刪除指令後，資料庫再查詢
            records=record_database(loginaccount)
            num=len(records)
            print(records)
            print(f'records after delete:{records}')
            return render_template("tables.html",num=num,records=records,Balance=Balance,account=loginaccount)
        
        #刪除項目為收入
        else:
            print(f'income is:{records[int(a)][2]}')

            #資料庫Balance更新
            Balance=records[int(a)][-1]+records[int(a)][-2]-records[int(a)][-3]
            print(f'original balance:{records[int(a)][-1]};new balance:{Balance}')
            update_balance(loginaccount,Balance)

            #資料庫刪除指令
            delete_income(loginaccount,class_name,date_value,income_value,income_value)

            #刪除指令後，資料庫再查詢
            records=record_database(loginaccount)
            num=len(records)
            print(records)
            return render_template("tables.html",num=num,records=records,Balance=Balance,account=loginaccount)
    
    #當前紀錄僅有一筆
    else:
        #資料庫刪除指令
        delete_sql=f"delete FROM {loginaccount} "
        cursor.execute(delete_sql)
        conn.commit()
        records=record_database(loginaccount)
        num=len(records)
        Balance=0
        print(records)

        return render_template("tables.html",num=0,records=records,Balance=Balance,account=loginaccount)

#至修改mode
@app.route('/editmode',methods = ['POST','GET'])
def edit_mode():
    loginaccount=session['memberacc']
    a=request.args.get('id')
    #查閱資料庫
    records=record_database(loginaccount)
    print(f'original data:{records}')
    print(f'original:{type(records)}')
    num=len(records)
    print(f'original:{num}')

    date_value=records[int(a)][0]
    class_name=records[int(a)][1]
    income_value=records[int(a)][2]
    cost_value=records[int(a)][3]

    print(f'id:{a}')
    print(type(a))
    

    # balance處理→取消修改列對balance影響  
    #當前紀錄超過一筆
    if num>1:
        Balance=records[-1][-1]+cost_value-income_value
    else:
       Balance=0

    # 更新資料庫balance
    update_balance(loginaccount,Balance)
  
    return render_template("editmode.html"
    ,num=num,records=records,Balance=Balance,a=int(a),account=loginaccount)

@app.route('/submit_update',methods =['POST','GET'])
def submit_update():
    loginaccount=session['memberacc']
    # a=request.form['confirming']
    a=request.args.get('id')
    print(f'id:{a}')
    print(type(a))

    #查閱資料庫

    records=record_database(loginaccount)
    print(records)
    num=len(records)
    print(num)
    d=request.form.to_dict()
    print(f'editing dic:{d}')

    #欲修改內容
    date_value=records[int(a)][0]
    class_name=records[int(a)][1]
    income_value=records[int(a)][2]
    cost_value=records[int(a)][3]
    print(f'editing content:{date_value},{class_name},{income_value},{cost_value}')


    #修改後內容
    update_date=d['edit_Date']
    update_class=d['edit_Money_Class']
    update_income=d['edit_Income']
    update_spent=d['edit_Cost']
    Balance= records[int(a)][-1]
    print(f'new content:{update_date},{update_class},{update_income},{update_spent}')
    #收入&支出 → list → 處理空值 → 0才能運算。
    print(update_income)
    print(type(update_income))

    b=update_income
    c=update_spent
    print(f'original:{update_income};income:{b}')
    print(f'original:{update_spent};spent:{c}')

    # balance處理  
    if num>1: #當前紀錄超過一筆
        print('Aa')
        if cost_value==0: #cost=0→ 修改收入
            print(f'A++ update balance: {Balance}')
            #資料庫刪除修改舊內容
            delete_income(loginaccount,class_name,date_value,income_value,income_value)

        elif income_value==0: #income=0→ 修改支出
            print(f'B++ update balance: {Balance}')
            #資料庫刪除修改舊內容
            delete_cost(loginaccount,class_name,date_value,cost_value,cost_value)

        #Balance最後更新、資料庫新增修改內容
        Balance=Balance+int(b)-int(c)
        insert_record(loginaccount,update_date,update_class,int(b),int(c),Balance)
        # 更新資料庫balance
        update_balance(loginaccount,Balance)

    else:#當前紀錄僅有一筆
        print(f'bb++ update balance: {Balance}')
        #整個資料庫刪除
        delete_sql=f"delete FROM {loginaccount} "
        cursor.execute(delete_sql)
        conn.commit()

        #Balance最後更新、資料庫新增修改內容
        Balance=int(b)-int(c)
        insert_record(loginaccount,update_date,update_class,int(b),int(c),Balance)
        # 更新資料庫balance
        update_balance(loginaccount,Balance)

    records=record_database(loginaccount)
    print(records)
    num=len(records)

    return render_template("tables.html",num=num,records=records,Balance=Balance,account=loginaccount)

 #查看總收入圖表
@app.route('/index.html',methods = ['GET'])
def total_charts():
    loginaccount=session['memberacc']
    print(loginaccount)
    income_class=['薪水','獎金','股息','意外財','其他收入']
    income_salary=[]
    income_bonus=[]
    income_interest=[]
    income_accident=[]
    income_other=[]
    spent_class=['交通','飲食','生活','娛樂','股票投資','其他支出']
    spent_trans=[]
    spent_food=[]
    spent_life=[] 
    spent_fun=[]
    spent_invest=[]
    spent_other=[]       
    spent_money=[]
    spent_money_class=[]
    income_money=[]
    income_money_class=[]
    date=[]
    income=[]
    spent=[]

    #income圓餅圖
    select_income_sql=f"select `class`,sum(`income`)  FROM {loginaccount} where `spent`= 0 group by class"
    cursor.execute(select_income_sql)
    income_records=cursor.fetchall()
    income_num=len(income_records)
    for i in range(income_num):
        income_money.append(int(income_records[i][1]))
        income_money_class.append(income_records[i][0])

    #spent圓餅圖
    select_spent_sql=f"select `class`,sum(`spent`)  FROM {loginaccount} where `income`=0 group by class "
    cursor.execute(select_spent_sql)
    spent_records=cursor.fetchall()
    print(spent_records)
    spent_num=len(spent_records)
    for i in range(spent_num):
        spent_money.append(int(spent_records[i][1]))
        spent_money_class.append(spent_records[i][0])

    #每月開銷、收入線圖
    select_sql=f"select date_format(`Date`,'%y-%c') 'Year-Month',sum(`income`), sum(`spent`)  FROM {loginaccount} group by 1  order by 1"
    cursor.execute(select_sql)
    records=cursor.fetchall()
    print(records)
    print(type(records))
    num=len(records)
    print(num)

    for i in range(num):
        income.append(int(records[i][1]))
        spent.append(int(records[i][2]))

    #每月開銷、收入長條分布圖
    select_total_sql=f"select date_format(`Date`,'%y-%c') 'Year-Month',`class`, `income`, `spent` FROM {loginaccount} order by 1"
    cursor.execute(select_total_sql)
    total_records=cursor.fetchall()
    for i in income_class:
        if i=='薪水':
            select_income_sql=f"select date_format(`Date`,'%y-%c') 'Year-Month',`class`, sum(`income`)  FROM {loginaccount} where `income` in (select `income`  FROM {loginaccount} where `class`= '薪水') group by 1 order by 1"      
            cursor.execute(select_income_sql)
            salary=cursor.fetchall()
            print(f'salary is {salary}')
        if i=='獎金':
            select_income_sql=f"select date_format(`Date`,'%y-%c') 'Year-Month',`class`, sum(`income`)  FROM {loginaccount} where `income` in (select `income`  FROM {loginaccount} where `class`= '獎金') group by 1 order by 1"      
            cursor.execute(select_income_sql)
            bonus=cursor.fetchall()
        if i=='股息':
            select_income_sql=f"select date_format(`Date`,'%y-%c') 'Year-Month',`class`, sum(`income`)  FROM {loginaccount} where `income` in (select `income`  FROM {loginaccount} where `class`= '股息') group by 1 order by 1"      
            cursor.execute(select_income_sql)
            interest=cursor.fetchall()
        if i=='意外財':
            select_income_sql=f"select date_format(`Date`,'%y-%c') 'Year-Month',`class`, sum(`income`)  FROM {loginaccount} where `income` in (select `income`  FROM {loginaccount} where `class`='意外財') group by 1 order by 1"      
            cursor.execute(select_income_sql)
            accident=cursor.fetchall()
            print(f'accident is {accident}')
        if i=='其他收入':
            select_income_sql=f"select date_format(`Date`,'%y-%c') 'Year-Month',`class`, sum(`income`)  FROM {loginaccount} where `income` in (select `income`  FROM {loginaccount} where `class`= '其他收入') group by 1 order by 1"  
            cursor.execute(select_income_sql)
            otherincome=cursor.fetchall()

    for i in spent_class:
        if i=='交通':
            select_spent_sql=f"select date_format(`Date`,'%y-%c') 'Year-Month',`class`, sum(`spent`)  FROM {loginaccount} where `spent` in (select `spent`  FROM {loginaccount} where `class`= '交通') group by 1 order by 1"      
            cursor.execute(select_spent_sql)
            trans=cursor.fetchall()
            print(f'trans is {trans}')
        if i=='飲食':
            select_spent_sql=f"select date_format(`Date`,'%y-%c') 'Year-Month',`class`, sum(`spent`)  FROM {loginaccount} where `spent` in (select `spent`  FROM {loginaccount} where `class`= '飲食') group by 1 order by 1"      
            cursor.execute(select_spent_sql)
            food=cursor.fetchall()
        if i=='生活':
            select_spent_sql=f"select date_format(`Date`,'%y-%c') 'Year-Month',`class`, sum(`spent`)  FROM {loginaccount} where `spent` in (select `spent`  FROM {loginaccount} where `class`= '生活') group by 1 order by 1"      
            cursor.execute(select_spent_sql)
            life=cursor.fetchall()
        if i=='娛樂':
            select_spent_sql=f"select date_format(`Date`,'%y-%c') 'Year-Month',`class`, sum(`spent`)  FROM {loginaccount} where `spent` in (select `spent`  FROM {loginaccount} where `class`= '娛樂') group by 1 order by 1"      
            cursor.execute(select_spent_sql)
            fun=cursor.fetchall()
        if i=='股票投資':
            select_spent_sql=f"select date_format(`Date`,'%y-%c') 'Year-Month',`class`, sum(`spent`)  FROM {loginaccount} where `spent` in (select `spent`  FROM {loginaccount} where `class`= '股票投資') group by 1 order by 1"      
            cursor.execute(select_spent_sql)
            invest=cursor.fetchall()
        if i=='其他支出':
            select_spent_sql=f"select date_format(`Date`,'%y-%c') 'Year-Month',`class`, sum(`spent`)  FROM {loginaccount} where `spent` in (select `spent`  FROM {loginaccount} where `class`= '其他支出') group by 1 order by 1"      
            cursor.execute(select_spent_sql)
            otherspent=cursor.fetchall()
    total_num=len(total_records)
    for i in range(total_num):
        if total_records[i][0] not in date:
            date.append(total_records[i][0])
        else: continue
    print(f'date:{date}')

    def chart_list(inputvalue,resultvalue):
        for i in range(len(inputvalue)):
            if len(inputvalue)>1 :
                print(f'{len(inputvalue)};;;inputvalue:{inputvalue}')
                for j in range(len(date)):
                    print(f'inputvalue:{inputvalue[i][0]},date:{date[j]}')

                    if inputvalue[i][0]==date[j]:
                        resultvalue.append(int(inputvalue[i][2]))
                        i+=1
                        if j==len(date)-1 or i ==len(inputvalue)-1:
                            break
                        else:continue
                    else:
                        resultvalue.append(0)
                        continue
            elif len(inputvalue)==1:
                print(inputvalue)
                for j in range(len(date)):
                    if inputvalue[0][0]==date[j]:
                        resultvalue.append(int(inputvalue[0][2]))
                        j+=1
                        if j==len(date):
                            break
                        else:continue
                    else:
                        resultvalue.append(0)
                        j+=1
            else:break
            break
        return resultvalue
    chart_list(salary,income_salary )
    chart_list(bonus,income_bonus )
    chart_list(interest,income_interest )
    chart_list(accident,income_accident)
    chart_list(otherincome,income_other )
    chart_list(trans,spent_trans )
    chart_list(food,spent_food  )
    chart_list(life,spent_life )
    chart_list(fun,spent_fun  )
    chart_list(invest,spent_invest )
    chart_list(otherspent,spent_other)
    print(f"income salary:{income_salary}")

    #dashboard
    select_sql=f"select `Date`,`class`,`income`,`spent`,`balance`  FROM {loginaccount}"
    cursor.execute(select_sql)
    records=cursor.fetchall()
    print(records)
    if records!=():
        balance=records[0][-1]
        select_income_sql=f"select sum(`income`)  FROM {loginaccount} where `spent`= 0"
        cursor.execute(select_income_sql)
        income_records=cursor.fetchall()
        if income_records[0][0]==None:
            income_int=0
        else:
            income_int=int(income_records[0][0])

        select_spent_sql=f"select sum(`spent`)  FROM {loginaccount} where `income`= 0"
        cursor.execute(select_spent_sql)
        spent_records=cursor.fetchall()
        print(spent_records)
        print(type(spent_records))
        if spent_records[0][0]==None:
            spent_int=0
        else:
            spent_int=int(spent_records[0][0])
        
    else:
        balance=0
        income_int=0
        spent_int=0



    def easy_read_amount(inputmoney):
        total_money_length=len(str(inputmoney)) 
        initial_value_qty=total_money_length%3 #1(餘數)
        comma_qty=total_money_length//3  #無條件捨去
        final_length=initial_value_qty+comma_qty+1
        result=str(inputmoney)[0:initial_value_qty]+","
        if comma_qty>0:
            for i in range(1,comma_qty+1):
                if i!=comma_qty:
                    result=result+str(inputmoney)[initial_value_qty+3*(i-1):initial_value_qty+3*i]+","
                    print(f'{i}:{result}')
                else:
                    result=result+str(inputmoney)[initial_value_qty+3*(i-1):initial_value_qty+3*i]
        else:
            result=inputmoney
        return f'${result}'
    spent_int=easy_read_amount(spent_int)
    income_int=easy_read_amount(income_int)
    balance=easy_read_amount(balance)
    print(f'balance:{balance}\n income:{income_records} \n spent:{spent_records}')

    print(f'income salary: {salary}\n trans: {trans}\n income accident: {accident}')


    date= json.dumps(date)
    spent_money= json.dumps(spent_money)
    spent_money_class=json.dumps(spent_money_class)
    income_money= json.dumps(income_money)
    income_money_class=json.dumps(income_money_class)
    income= json.dumps(income)
    spent= json.dumps(spent)


    income_salary=json.dumps(income_salary)
    income_bonus=json.dumps(income_bonus)
    income_interest=json.dumps(income_interest)
    income_accident=json.dumps(income_accident)
    income_other=json.dumps(income_other)

    spent_trans=json.dumps(spent_trans)
    spent_food=json.dumps(spent_food)
    spent_life=json.dumps(spent_life) 
    spent_fun=json.dumps(spent_fun)
    spent_invest=json.dumps(spent_invest)
    spent_other=json.dumps(spent_other)   
    return render_template("index.html", spent_money=spent_money, spent_money_class=spent_money_class
    , income_money=income_money, income_money_class=income_money_class, date=date,income=income,spent=spent,income_salary=income_salary, income_bonus=income_bonus, income_interest=income_interest,
    income_accident=income_accident, income_other=income_other,spent_trans=spent_trans,spent_food=spent_food,spent_life=spent_life,spent_fun=spent_fun,
    spent_invest=spent_invest,spent_other=spent_other,account=loginaccount,balance=balance,income_int=income_int, spent_int=spent_int
    )

if (__name__) == ('__main__'):
    app.run(debug=True) #啟動網站伺服器，可透過port參數設定阜號