#連接資料庫、表格建立、欄位新增/修改
import pymysql
import pymysql.cursors

# Connect to the database
# MySQL需先創建Momey Management資料庫
# def connection(db)
def connection(db):
    connection = pymysql.connect(host='localhost',
                            user='root',
                            password='987654321',
                            database=db,
                            )   
    return connection

# create table 'member'
mycursor = connection('Money Management').cursor()
# mycursor.execute('CREATE TABLE IF NOT EXISTS `sign-in-member`( \
#             `member_account` VARCHAR(20) NOT NULL primary key, \
#             `member_pwd` VARCHAR(20) NOT NULL \
#             )')
# print("create table successfully")


# mycursor.execute('CREATE TABLE IF NOT EXISTS `record`( \
#                 `class` VARCHAR(20) NOT NULL, \
#                 `money` int(20) NOT NULL \
#                 )')

# 新增/修改欄位
# mycursor.execute('ALTER TABLE `record` ADD balance int(20)')
# mycursor.execute('ALTER TABLE `record` CHANGE COLUMN money income int(20)')
# mycursor.execute('ALTER TABLE `record` ADD COLUMN spent int(20) AFTER income ')
print("connect DB successfully")

