#sign in member db
import main.conDB

member_account=input('Please enter account: ')
member_pwd=input('Please enter password: ')
conn=main.conDB.connection('Money Management')
cursor=conn.cursor()
sql = "INSERT INTO `sign-in-member` (`member_account`, `member_pwd`) VALUES (%s, %s)"
cursor.execute(sql, (member_account, member_pwd))
conn.commit()



