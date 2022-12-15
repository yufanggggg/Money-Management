from form import RecordForm
from flask import Flask, render_template, request, flash
import pymysql
import pymysql.cursors
app = Flask(__name__)
app.secret_key = 'development key'
conn=pymysql.connect(host='localhost',
                            user='root',
                            password='987654321',
                            database='Money Management',
                            )   
cursor=conn.cursor()

@app.route('/record', methods = ['POST'])
def record_create():
    form = RecordForm()
    Date=form.Date
    Money_Class=form.Money_Class
    Income=form.Income
    Cost=form.Cost
    Balance=form.Balance
    sql="INSERT INTO `record` (`Date`,`class`,`income`,`spent`,`balance`) VALUES(%d,%s,%s,%s,%s)" 
    val=(Date,Money_Class,Income,Cost,Balance)
    cursor.execute(sql, val)
    conn.commit()
    return render_template('tables.html',
                           Date=Date,
                           Money_Class=Money_Class,
                           Income=Income,
                           Cost=Cost,
                           Balance=Balance)
@app.route('/record', methods = ['GET'])
def record_read():
    form = RecordForm()
    Date=form.Date
    Money_Class=form.Money_Class
    Income=form.Income
    Cost=form.Cost
    Balance=form.Balance
    sql="SELECT * from `record`" 
    cursor.execute(sql)
    result=cursor.fetchall()
    return render_template('tables.html',
                           Date=Date,
                           Money_Class=Money_Class,
                           Income=Income,
                           Cost=Cost,
                           Balance=Balance)
if __name__ == '__main__':
    app.run(debug = True)