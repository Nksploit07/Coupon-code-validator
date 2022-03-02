from flask import Flask, render_template, url_for, request 
import random
import string
from datetime import datetime, timedelta, date
import sqlite3
import coupon as cp

app=Flask(__name__)

@app.route("/")
def Home():
    return render_template('home.html')



@app.route("/coupon",methods=['GET','POST'])
def couponpage():
    con=sqlite3.connect("database/shop.db")
    conn=con.cursor()
    conn.execute("select * from coupon where 1=1")
    row=conn.fetchall()
    return render_template('coupon.html',rows=row)

@app.route("/createcoupon",methods=['GET','POST'])
def createcoupon():
    print('don')
    code=cp.Coupon_code_genreator()
    print(code)
    con=sqlite3.connect("database/shop.db")
    conn=con.cursor()
    conn.execute("select * from coupon where 1=1")
    row=conn.fetchall()
    return render_template('coupon.html',rows=row)




@app.route("/validate",methods=['POST','GET'])
def validate():
    if request.method=='POST':
        amount=int(request.form.get('amt'))
        coupen_code=request.form.get('ccode')
        print("Inserted Amount:",amount)
        print("Inserted Coupon code:",coupen_code)
        con=sqlite3.connect("database/shop.db")
        conn=con.cursor()
        conn.execute("select * from coupon where code==?",(coupen_code,))
        con.commit()
        data=conn.fetchall()
        
                    
        if len(data) == 0:
            return render_template('home.html',msg="Invalid coupon code")
        else:
            for row in data:
                v_exp=row[3]
                v_dis_type=row[1]
                v_dis=row[2]
                v_minamt=row[5]
                v_code=row[0]

        expdate=v_exp.split("-")
        datev=str(date.today())
        curdate=datev.split("-")
        print("date:",expdate,curdate)
        if curdate[2]>=expdate[2] and curdate[1]>=expdate[1] and curdate[0]>=expdate[0]:
            return render_template("home.html",msg="coupon expired.")
        else:
            if amount < v_minamt:
                return render_template('home.html',msg="coupon applicable on the purches of more than Rs ",amt=v_minamt)
            else:
                if v_dis_type=='Flat discount':
                    grand_total=amount-v_dis
                    print('Total amount:',amount)
                    print("discount:",v_dis)
                    print("grand total:",grand_total)
                    con=sqlite3.connect("database/shop.db")
                    conn=con.cursor()
                    conn.execute("delete from coupon where code=?",(v_code,))
                    con.commit()

                    return render_template('billreport.html',gtotal=grand_total,amt=amount,dis=v_dis)
                else:
                    v_dis=amount*v_dis/100
                    grand_total=amount-v_dis
                    print('Total amount:',amount)
                    print("discount:",v_dis)
                    print("grand total:",grand_total)
                    con=sqlite3.connect("database/shop.db")
                    conn=con.cursor()
                    conn.execute("delete from coupon where code=?",(v_code,))
                    con.commit()

                    return render_template('billreport.html',gtotal=grand_total,amt=amount,dis=v_dis)
def delexpcoupon():
    todaydate=str(date.today())
    con=sqlite3.connect("database/shop.db")
    conn=con.cursor()
    conn.execute("delete from coupon where expdate=?",(todaydate,))
    con.commit()

delexpcoupon()



if __name__=="__main__":
    app.run(debug=True)