# flask version
from wtforms.widgets import HTMLString, html_params
from flask_wtf import Form
from wtforms import *
import main.conDB


class RecordForm(Form):
    Date = DateField("日期'")
    Money_Class=RadioField('金錢類別', choices = ['交通','飲食','生活','娛樂','其他支出','投資','薪水','獎金','獲利','意外財','其他收入'])
    Income=IntegerField("收入")
    Cost=IntegerField("支出")
    Balance=IntegerField("淨額")
    submit = SubmitField("提交")

