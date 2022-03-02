import random
import string
from datetime import datetime, timedelta, date
import sqlite3



def Coupon_code_genreator():
    str_size=12
    up_al="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    lo_al="abcdefghijklmnopqrstuvwxyz"
    num="1234567890"
    code="".join(random.choices(up_al+lo_al+num,k=str_size))
    discount=['Flat discount','Percentage discount']
    coupon_type="".join(random.choices(discount))
    minamt=random.randint(500,2500)
    if coupon_type=="Flat discount":
        value=random.randint(100,250)
        vtype="Rs"
    else:
        value=random.randint(2,50)
        vtype="%"
    print("Coupon type:",coupon_type)
    current_date = date.today()
    print("created date",current_date)
    exp_date = current_date + timedelta(days=random.randint(10,25))

    print("Ending date",exp_date)
    con=sqlite3.connect("database/shop.db")
    conn=con.cursor()
    conn.execute("insert into coupon values(?,?,?,?,?,?)",(code,coupon_type,value,exp_date,vtype,minamt))
    con.commit()
    return code