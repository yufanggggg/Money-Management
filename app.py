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
def record_database():
    select_sql="select `Date`,`class`,`income`,`spent`,`balance` from `record`"
    cursor.execute(select_sql)
    records=cursor.fetchall()
    return records

#更新資料庫Balance函式
def update_balance(e):
    update_sql="update `record` set balance= %s "
    cursor.execute(update_sql,e)
    conn.commit()

#刪除支出資料庫函式
def delete_cost(b,c,d,e):
    delete_sql="delete FROM `record` where `Date`= (SELECT * FROM (SELECT `Date` FROM `record` where class = %s and Date = %s )AS A where `spent`= %s or `income` = %s)"
    cursor.execute(delete_sql,(b,c,d,e))
    conn.commit()

#刪除收入資料庫函式
def delete_income(b,c,d,e):
    delete_sql="delete FROM `record` where `Date`= (SELECT * FROM (SELECT `Date` FROM `record` where class = %s and Date = %s )AS A where `spent`= %s or `income` = %s)"
    cursor.execute(delete_sql,(b,c,d,e))
    conn.commit()

#新增資料函式
def insert_record(a,b,c,d,e):
    insert_sql="INSERT INTO `record` (`Date`,`class`,`income`,`spent`,`balance`) VALUES(%s,%s,%s,%s,%s)" 
    val=(a,b,c,d,e)
    cursor.execute(insert_sql, val)
    conn.commit()


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
        message='帳號已被註冊'
        return render_template('register.html',message=message)
    else:
        sql = "INSERT INTO `sign-in-member` (`member_account`, `member_pwd`) VALUES (%s, %s)"
        cursor.execute(sql, (account, pwd))
        conn.commit()
        print("新帳號")
        message=f'{account}註冊成功，請登入'
        return render_template('login.html',account=account,message=message)

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
                    return render_template("/index.html")
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
    return render_template("login.html")

@app.route('/login_again')
def login_again():
    message=f'密碼錯誤，請重新登入'
    return render_template("login.html",message=message)

@app.route('/record', methods = ['POST','GET'])
def record_create():
    loginaccount=session['memberacc']    
    b=request.form.to_dict()
    print(b)
#查閱資料庫
    records=record_database()
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
        else:
            b['Balance']=b['Balance']

        #寫入資料庫
        insert_record(b['Date'],b['Money_Class'],int(b['Income']),int(b['Cost']),b['Balance'])

        # 更新balance
        update_balance(b['Balance'])
    
        return render_template("tables.html",num=num,records=records,b=b
    ,Date=b['Date'],Money_Class=b['Money_Class'],Income=int(b['Income']),Cost=int(b['Cost']),Balance=b['Balance'],account=loginaccount
    )

    #無新增資料
    else:
        records=record_database()
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
    a=request.args.get('id')
    print(f'id:{a}')
    print(type(a))
    #查閱刪除前資料庫
    records=record_database()
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
            update_balance(Balance)

            #資料庫刪除指令
            delete_cost(class_name,date_value,cost_value,cost_value)

            #刪除指令後，資料庫再查詢
            records=record_database()
            num=len(records)
            print(records)
            print(f'records after delete:{records}')
            return render_template("tables.html",num=num,records=records,Balance=Balance)
        
        #刪除項目為收入
        else:
            print(f'income is:{records[int(a)][2]}')

            #資料庫Balance更新
            Balance=records[int(a)][-1]+records[int(a)][-2]-records[int(a)][-3]
            print(f'original balance:{records[int(a)][-1]};new balance:{Balance}')
            update_balance(Balance)

            #資料庫刪除指令
            delete_income(class_name,date_value,income_value,income_value)

            #刪除指令後，資料庫再查詢
            records=record_database()
            num=len(records)
            print(records)
            return render_template("tables.html",num=num,records=records,Balance=Balance)
    
    #當前紀錄僅有一筆
    else:
        #資料庫刪除指令
        delete_sql="delete FROM `record` "
        cursor.execute(delete_sql)
        conn.commit()
        records=record_database()
        num=len(records)
        Balance=0
        print(records)

        return render_template("tables.html",num=0,records=records,Balance=Balance)

#至修改mode
@app.route('/editmode',methods = ['POST','GET'])
def edit_mode():
    a=request.args.get('id')
    #查閱資料庫
    records=record_database()
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
    update_balance(Balance)
  
    return render_template("editmode.html"
    ,num=num,records=records,Balance=Balance,a=int(a))

@app.route('/submit_update',methods =['POST','GET'])
def submit_update():
    e=request.args.get('id')
    print(f'id:{e}')

    #查閱資料庫
    records=record_database()
    print(records)
    num=len(records)
    print(num)

    #欲修改內容
    date_value=records[int(e)][0]
    class_name=records[int(e)][1]
    income_value=records[int(e)][2]
    cost_value=records[int(e)][3]
    print(f'editing content:{date_value},{class_name},{income_value},{cost_value}')


    #修改後內容
    update_date=request.form.get('edit_Date',records[int(e)][0])
    update_class=request.form.get('edit_Money_Class',records[int(e)][1])
    update_income=request.form.get('edit_Income',0)
    update_spent=request.form.get('edit_Cost',0)
    Balance= records[int(e)][-1]
    #收入&支出 → list → 處理空值 → 0才能運算。
    b=update_income.split()
    c=update_spent.split()
    print(f'original:{update_income};income:{b}')
    print(f'original:{update_spent};spent:{c}')

    if b==[]:
        b.insert(0,0)
    if c==[]:
        c.insert(0,0)

    # balance處理  
    if num>1: #當前紀錄超過一筆
        print('Aa')
        if cost_value==0: #cost=0→ 修改收入
            print(f'A++ update balance: {Balance}')
            #資料庫刪除修改舊內容
            delete_income(class_name,date_value,income_value,income_value)

        elif income_value==0: #income=0→ 修改支出
            print(f'B++ update balance: {Balance}')
            #資料庫刪除修改舊內容
            delete_cost(class_name,date_value,cost_value,cost_value)

        #Balance最後更新、資料庫新增修改內容
        Balance=Balance+int(b[0])-int(c[0])
        insert_record(update_date,update_class,b[0],c[0],Balance)
        # 更新資料庫balance
        update_balance(Balance)

    else:#當前紀錄僅有一筆
        print(f'bb++ update balance: {Balance}')
        #整個資料庫刪除
        delete_sql="delete FROM `record` "
        cursor.execute(delete_sql)
        conn.commit()

        #Balance最後更新、資料庫新增修改內容
        Balance=int(b[0])-int(c[0])
        insert_record(update_date,update_class,b[0],c[0],Balance)
        # 更新資料庫balance
        update_balance(Balance)

    records=record_database()
    print(records)
    num=len(records)

    return render_template("tables.html",num=num,records=records,Balance=Balance)

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
    select_income_sql="select `class`,sum(`income`) from `record` where `spent`= 0 group by class"
    cursor.execute(select_income_sql)
    income_records=cursor.fetchall()
    income_num=len(income_records)
    for i in range(income_num):
        income_money.append(int(income_records[i][1]))
        income_money_class.append(income_records[i][0])

    #spent圓餅圖
    select_spent_sql="select `class`,sum(`spent`) from `record` where `income`=0 group by class "
    cursor.execute(select_spent_sql)
    spent_records=cursor.fetchall()
    print(spent_records)
    spent_num=len(spent_records)
    for i in range(spent_num):
        spent_money.append(int(spent_records[i][1]))
        spent_money_class.append(spent_records[i][0])

    #每月開銷、收入線圖
    select_sql="select date_format(`Date`,'%y-%c') 'Year-Month',sum(`income`), sum(`spent`) from `record` group by 1  order by 1"
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
    select_total_sql="select date_format(`Date`,'%y-%c') 'Year-Month',`class`, `income`, `spent` from `record` order by 1"
    cursor.execute(select_total_sql)
    total_records=cursor.fetchall()
    for i in income_class:
        if i=='薪水':
            select_income_sql="select date_format(`Date`,'%y-%c') 'Year-Month',`class`, sum(`income`) from `record` where `income` in (select `income` from `record` where `class`= '薪水') group by 1 order by 1"      
            cursor.execute(select_income_sql)
            salary=cursor.fetchall()
            print(f'salary is {salary}')
        if i=='獎金':
            select_income_sql="select date_format(`Date`,'%y-%c') 'Year-Month',`class`, sum(`income`) from `record` where `income` in (select `income` from `record` where `class`= '獎金') group by 1 order by 1"      
            cursor.execute(select_income_sql)
            bonus=cursor.fetchall()
        if i=='股息':
            select_income_sql="select date_format(`Date`,'%y-%c') 'Year-Month',`class`, sum(`income`) from `record` where `income` in (select `income` from `record` where `class`= '股息') group by 1 order by 1"      
            cursor.execute(select_income_sql)
            interest=cursor.fetchall()
        if i=='意外財':
            select_income_sql="select date_format(`Date`,'%y-%c') 'Year-Month',`class`, sum(`income`) from `record` where `income` in (select `income` from `record` where `class`='意外財') group by 1 order by 1"      
            cursor.execute(select_income_sql)
            accident=cursor.fetchall()
            print(f'accident is {accident}')
        if i=='其他收入':
            select_income_sql="select date_format(`Date`,'%y-%c') 'Year-Month',`class`, sum(`income`) from `record` where `income` in (select `income` from `record` where `class`= '其他收入') group by 1 order by 1"  
            cursor.execute(select_income_sql)
            otherincome=cursor.fetchall()

    for i in spent_class:
        if i=='交通':
            select_spent_sql="select date_format(`Date`,'%y-%c') 'Year-Month',`class`, sum(`spent`) from `record` where `spent` in (select `spent` from `record` where `class`= '交通') group by 1 order by 1"      
            cursor.execute(select_spent_sql)
            trans=cursor.fetchall()
            print(f'trans is {trans}')
        if i=='飲食':
            select_spent_sql="select date_format(`Date`,'%y-%c') 'Year-Month',`class`, sum(`spent`) from `record` where `spent` in (select `spent` from `record` where `class`= '飲食') group by 1 order by 1"      
            cursor.execute(select_spent_sql)
            food=cursor.fetchall()
        if i=='生活':
            select_spent_sql="select date_format(`Date`,'%y-%c') 'Year-Month',`class`, sum(`spent`) from `record` where `spent` in (select `spent` from `record` where `class`= '生活') group by 1 order by 1"      
            cursor.execute(select_spent_sql)
            life=cursor.fetchall()
        if i=='娛樂':
            select_spent_sql="select date_format(`Date`,'%y-%c') 'Year-Month',`class`, sum(`spent`) from `record` where `spent` in (select `spent` from `record` where `class`= '娛樂') group by 1 order by 1"      
            cursor.execute(select_spent_sql)
            fun=cursor.fetchall()
        if i=='股票投資':
            select_spent_sql="select date_format(`Date`,'%y-%c') 'Year-Month',`class`, sum(`spent`) from `record` where `spent` in (select `spent` from `record` where `class`= '股票投資') group by 1 order by 1"      
            cursor.execute(select_spent_sql)
            invest=cursor.fetchall()
        if i=='其他支出':
            select_spent_sql="select date_format(`Date`,'%y-%c') 'Year-Month',`class`, sum(`spent`) from `record` where `spent` in (select `spent` from `record` where `class`= '其他支出') group by 1 order by 1"      
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
    select_sql="select `Date`,`class`,`income`,`spent`,`balance` from `record`"
    cursor.execute(select_sql)
    records=cursor.fetchall()
    balance=records[0][-1]
    select_income_sql="select sum(`income`) from `record` where `spent`= 0"
    cursor.execute(select_income_sql)
    income_records=cursor.fetchall()
    income_int=int(income_records[0][0])

    select_spent_sql="select sum(`spent`) from `record` where `income`= 0"
    cursor.execute(select_spent_sql)
    spent_records=cursor.fetchall()
    spent_int=int(spent_records[0][0])

    def easy_read_amount(inputmoney):
        total_money_length=len(str(inputmoney)) 
        initial_value_qty=total_money_length%3 #1(餘數)
        comma_qty=total_money_length//3  #無條件捨去
        final_length=initial_value_qty+comma_qty+1
        result=str(inputmoney)[0:initial_value_qty]+","
        for i in range(1,comma_qty+1):
            if i!=comma_qty:
                result=result+str(inputmoney)[initial_value_qty+3*(i-1):initial_value_qty+3*i]+","
                print(f'{i}:{result}')
            else:
                result=result+str(inputmoney)[initial_value_qty+3*(i-1):initial_value_qty+3*i]
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