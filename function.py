import main.conDB
cost=['交通','飲食','生活','娛樂','其他支出','投資']
earning=['薪水','獎金','獲利','意外財','其他收入']
class data:
  def __init__(self,asset):
    self.__asset=asset
    self.balance=asset

  def change(self,j,money):
    if j in cost:
      print(f'original asset: {self.balance}')
      if self.balance <money:
          self.balance=self.balance-money
          print("餘額不足!!!!")
      else:
        self.balance=self.balance-money
        print(f'新增紀錄: {j}, ${money},餘額:{self.balance}')
    elif j in earning:
      self.balance=self.balance+money
      print(f'新增紀錄: {j}, ${money},餘額:{self.balance}')
    else:
      print('error')
#實作
original_asset=int(input('請輸入資產: '))
I=data(original_asset)
print(I.balance)

while True:
  try:
    m_class=input('請輸入金錢用途/來源: ')
    m=int(input('請輸入金額: '))
    I.change(m_class,m)
    conn=main.conDB.connection('Money Management')
    cursor=conn.cursor()
    
    if m_class in cost :
      if m<=I.balance:
        sql="INSERT INTO `record` (`class`,`income`,`spent`,`balance`) VALUES(%s,%s,%s,%s)"
        val=(m_class,0,m,I.balance)
        cursor.execute(sql, val)
        conn.commit()
        print('成功插入表格一筆')
      else:
        conn.rollback()
        print('餘額不足，無法插入表格')
    elif m_class in earning:
      sql="INSERT INTO `record` (`class`,`income`,`spent`,`balance`) VALUES(%s,%s,%s,%s)"
      val=(m_class,m,0,I.balance)
      cursor.execute(sql, val)
      conn.commit()
      print('成功插入表格一筆')
            
  except: 
    break
