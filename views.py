
from django.shortcuts import render,redirect

from django.http import HttpResponse
import mysql.connector as mcdb
from django.contrib  import messages
from django.core.mail import send_mail
from django.conf import settings
import datetime
import random
import uuid



conn = mcdb.connect(host="localhost",user = "root",password = "",database='mydb')
print('successfully connected to database')

cur = conn.cursor()

# home

def home(request):
     return render(request,'user/home.html')

def userhome(request):
    if 'user_email' in request.COOKIES and request.seesion.has_key('user_email'):
        admin_emails = request.session['user_email']
        admin_emailc = request.COOKIES['user_email']
        print("session Email is" + admin_emails)
        print("COOKIE Email is " + admin_emailc)
        return render(request,'user/home.html')
    else:
        return redirect(login)
    


# logout

def logout(request):
    del request.session['user_email']
    del request.session['user_id']
    response = redirect(login)
    response.delete_cookie('user_id')
    response.delete_cookie('user_email')
    return response

# about

def about(request):
    return render(request,'user/about.html')

# contact

def contact(request):
    return render(request,'user/contact.html')



# cart

def cart(request):
    return render(request,'user/cart.html')

# login

def login(request):
    return render(request,'user/login.html')

def login_process(request):
    email=request.POST["email"]
    password=request.POST["password"]
    cur.execute("select * from `tbl_user` where `user_email` = '{}' and `user_password` = '{}'".format(email,password))
    data = cur.fetchone()
    if data is not None:
        if len(data) > 0:
            # Fetch data
            user_id =data[0]     #fetch id of user
            user_email=data[4]    #fetch email of user

            # store user information in session
            request.session['user_id']=user_id
            request.session['user_email']=user_email

            # store user information in Cookie
            response = redirect(home)
            response.set_cookie('user_id',user_id)
            response.set_cookie('user_email',user_email)
            return response
        else:
                messages.success(request,'Login Failed')
                return render(request,'user/login.html')
    messages.success(request,'Login Failed!')
    return render(request,'user/login.html')



# change password

def change_password(request):
    return render(request,'user/change_password.html')

def change_passwordprocess(request):
    if 'user_id' in request.COOKIES and request.session.has_key('user_id'):
        user_id = request.session['user_id']
        opassword = request.POST['old_password']
        npassword = request.POST['new_password']
        cpassword = request.POST['confirm_password']

        # fetch old password from database
        cur.execute("select * from `tbl_user` where `user_id` = '{}'".format(user_id))
        db_data = cur.fetchone()
        if db_data is not None:
            if len(db_data) > 0:

                # compare old password with db old password
                old_password_db = db_data[5]
                if opassword == old_password_db:

                    # compare new and comfirm password
                    if npassword != cpassword:
                        messages.success(request,'New and confirmed password not matched')
                        return render(request,'user/change_password.html')
                    else:
                        cur.execute("update `tbl_user` set `user_password` = '{}' where `user_id` ='{}'".format(npassword,user_id))
                        conn.commit()
                        messages.success(request,'Password Changed successfully')
                        return render(request,'user/change_password.html')
                else:
                    messages.success(request, 'Old password not matched')
                    return render(request,'user/change_password.html')
            else:
                redirect(login)
        else:
            redirect(login)
    else:
        return redirect(login)




# signup


def signup(request):
    return render(request,'user/signup.html')

def signupprocess(request):
    name= request.POST["name"]
    gender= request.POST["gender"]
    phone=  request.POST["phone"]
    email= request.POST["email"]
    password= request.POST["password"]
    address= request.POST["address"]

    cur.execute("INSERT INTO `tbl_user` (`user_name`,`user_gender`,`user_mobile`,`user_email`,`user_password`,`user_address`) VALUES ('{}','{}','{}','{}','{}','{}')".format (name,gender,phone,email,password,address) ) 
    conn.commit()
    messages.success(request,'Account Created Successfully!')
    return redirect(signup)



# product


def product(request):
    cur.execute("SELECT * FROM `tbl_product` ")
    data = cur.fetchall()
    print(list(data))
    cur.execute("SELECT * FROM `tbl_category` ")
    data1 = cur.fetchall()
    print(list(data1))
    return render(request , 'user/product.html' , {"mydata":data,"cdata":data1})

def productlistingbycategory(request,id):
    print(id)
    cur.execute("""
    select * from `tbl_product` where `category_id`  = '{}'
      """.format(id))
    data = cur.fetchall()
    #return list(data)
    print(list(data))
    cur.execute("SELECT     * from tbl_category")
    data1 = cur.fetchall()
    #return list(data)
    print(list(data1))
    return render(request, 'user/product.html', {'mydata': data,'cdata': data1})

def productsearch(request):
    search = request.GET['search']
    cur.execute("""select * from `tbl_product` where `product_name`  like '%{}%'""".format(search))
    data = cur.fetchall()
    #return list(data)
    print(list(data))
    cur.execute("SELECT * from `tbl_category`")
    data1 = cur.fetchall()
    #return list(data)
    print(list(data1))
    return render(request, 'user/product.html', {'mydata': data,'cdata': data1})



#  product details 


def product_details(request,id):
    cur.execute("SELECT * FROM `tbl_product` where  `product_id` = '{}'".format(id) )
    data = cur.fetchone()
    print(list(data)) 
    return render(request,'user/product_details.html',{'mydata': data})



# checkout

def checkout(request):
    return render(request,'user/checkout.html')





# mail send

def mailsendprocess(request):
    body = "Name is " + request.POST['txt1'] + "\n Message is " + request.POST['txt2'] + "\n Phone " + request.POST['txt3']
    email_form = settings.EMAIL_HOST_USER
    recipient_list = ['agrimarketofficial@gmail.com']
    subject = "Contact Form Website"
    send_mail(subject,body,email_form,recipient_list)

    cur.execute("INSERT INTO tbl_contact (user_name, contact_details, user_mobile) VALUES (%s, %s, %s)", (request.POST['txt1'], request.POST['txt2'], request.POST['txt3']))
    conn.commit()

    # Redirect to contact page
    return redirect(contact)
    



# def addtocart(request,id):
#     if 'user_id' in request.COOKIES and request.session.has_key('user_id'):
#         userid = request.session['user_id']
#         db_data = cur.fetchone()
#         pid = id
#         qty = request.POST['qty']
#         cur.execute("select * from `tbl_cart` where `user_id` = {} and `product_id` = {}".format(userid,pid))
#         db_data = cur.fetchone()
#         if db_data == None:
#             cur.execute("INSERT INTO `tbl_cart`(`user_id`,`product_id`,`product_qty`) VALUES ('{}','{}','{}')".format(userid,pid,qty))
#             conn.commit()
#             messages.success(request, 'Product Added to Cart')
#             return redirect(cartview)
#         else:
#             oldqty = db_data[3]
#             newqty = int(oldqty) + int(qty)
#             cartid = db_data[0]
#             cur.execute("update `tbl_cart` set `product_qty` = '{}' where `cart_id` = '{}'".format(newqty,cartid))
#             conn.commit()
#             messages.success(request, 'Cart Updated')
#             return redirect(cartview)
#     else:
#         return redirect(login)


def addtocart(request, id):
    if 'user_id' in request.COOKIES and 'user_id' in request.session:
        
        pid = id
        qty = request.POST['qty']
        # pprice = request.POST['price']
        userid = request.session['user_id']


        
        # Assuming you have established a connection and cursor before this point
        cur.execute("SELECT * FROM `tbl_cart` WHERE `user_id` = %s AND `product_id` = %s", (userid, pid))
        db_data = cur.fetchone()
        
        if db_data is None:
            cur.execute("INSERT INTO `tbl_cart` (`product_id`, `product_qty`,`user_id`) VALUES (%s, %s, %s)", (pid, qty, userid))
            conn.commit()
            messages.success(request, 'Product Added to Cart')
            return redirect(cartview)
        else:
            oldqty = db_data[2]  # Assuming the index of product_qty in db_data is 2, adjust as necessary
            newqty = int(oldqty) + int(qty)
            cartid = db_data[0]  # Assuming the index of cart_id in db_data is 0, adjust as necessary
            cur.execute("UPDATE `tbl_cart` SET `product_qty` = %s WHERE `cart_id` = %s", (newqty, cartid))
            conn.commit()
            messages.success(request, 'Cart Updated')
            return redirect(cartview)
    else:
        return redirect(login)

def cartview(request):
    if 'user_id' in request.COOKIES and request.session.has_key('user_id'):
        uid = request.session['user_id']
        cur.execute('''SELECT
            `tbl_cart`.`cart_id`
            , `tbl_product`.`product_name`
            , `tbl_product`.`product_price`
            , `tbl_product`.`product_image`
            , `tbl_cart`.`product_qty`
            , `tbl_cart`.`product_id`
            , `tbl_product`.`product_price` * `tbl_cart`.`product_qty` AS tot_price_times_qty
        FROM
            `tbl_product`
            INNER JOIN `tbl_cart` 
                ON (`tbl_product`.`product_id` = `tbl_cart`.`product_id`) WHERE `tbl_cart`.`user_id` = {}'''.format(uid))
        data = cur.fetchall()
        #return list(data)
        print(list(data))
        countevalue = len(data)
        res = sum(i[6] for i in data)  # Output: 15
        return render(request, 'user/cart.html', {'product': data,'total':res})
    else:
        return redirect(login)
        
def checkout(request):
    return  render(request,'user/checkout.html')



def cartremove(request,id):
    print("------------------------------")
    print(id)
    cur.execute("delete from tbl_cart where `cart_id` = {}".format(id))
    conn.commit()
    #return list(data)
    messages.success(request, 'Product Removed from Cart')
    return redirect(cartview)   

def placeorder(request):
        if 'user_id' in request.COOKIES and request.session.has_key('user_id'):
            order_date = datetime.datetime.now().strftime("%Y-%m-%d")
            order_status = "Confirmed"
            userid = request.session['user_id']
            shipping_name = request.POST['sname']
            user_mobile = request.POST['smobile']
            user_address = request.POST['saddress']
            paymentoption = request.POST['paymentoption']
            cur.execute("INSERT INTO `tbl_order_master`(`order_date`,`order_status`,`user_id`,`shipping_name`,`user_mobile`,`user_address`,`payment_mode`) VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(order_date,order_status,userid,shipping_name,user_mobile,user_address,paymentoption))
            conn.commit()

            orderid = cur.lastrowid
            #Order details

            uid = request.session['user_id']
            cur.execute(''' SELECT
                `tbl_cart`.`product_id`
                , `tbl_product`.`product_price`
                , `tbl_cart`.`product_qty`
            FROM
                `tbl_product`
                INNER JOIN `tbl_cart` 
                    ON (`tbl_product`.`product_id` = `tbl_cart`.`product_id`) WHERE `tbl_cart`.`user_id` = {}'''.format(uid))
            data = cur.fetchall()
            for i in data:
                oid = orderid
                pid = i[0]
                pqty = i[2]
                pprice = i[1]
                cur.execute("INSERT INTO `tbl_order_details`(`order_id`, `product_id`, `product_qty`, `product_price`) VALUES (%s, %s, %s, %s)", (oid, pid, pqty, pprice,))


                conn.commit()
            cur.execute("delete from `tbl_cart` where `user_id` = '{}' ".format(uid))
            conn.commit()
            return redirect(thanks)
        else:
            return redirect(login)

def thanks(request):
    return render(request,'user/thanks.html')



def orderview(request):
    if 'user_id' in request.COOKIES and request.session.has_key('user_id'):
        user_id = request.session['user_id']
        #cur.execute("Select * from tb_feedback")
        cur.execute('''select * from tbl_order_master 
         where user_id   = '{}'
        '''.format(user_id))
        data = cur.fetchall()
        print(list(data))
        return render(request, 'user/orderview.html', {'mydata': data})
    else:
        return redirect(login)

def orderdetailsview(request,id):
    if 'user_id' in request.COOKIES and request.session.has_key('user_id'):
        #cur.execute("Select * from tb_feedback")
        cur.execute('''SELECT
    `tbl_order_details`.`details_id`
    , `tbl_order_details`.`order_id`
    , `tbl_product`.`product_name`
    , `tbl_order_details`.`product_qty`
    , `tbl_order_details`.`product_price`
    
FROM
    `tbl_product`
    INNER JOIN `tbl_order_details` 
        ON (`tbl_product`.`product_id` = `tbl_order_details`.`product_id`) WHERE `tbl_order_details`.`order_id` =  '{}'
        '''.format(id))
        data = cur.fetchall()
        print(list(data))
        return render(request, 'user/orderdetails.html', {'mydata': data})
    else:
        return redirect(login)



def feedbackadd(request):
    if 'user_id' in request.COOKIES and request.session.has_key('user_id'):
        return render(request,'user/add_feedback.html')
    else:
        return redirect(login)
    
def feedbackaddprocess(request):
    print("Feedback added")
    if request.method == 'POST':
        print(request.POST)
        user_id = request.session['user_id']
        feedbackdetails = request.POST['txt1']
        feedbackdate = datetime.datetime.now().strftime("%Y-%m-%d")
        cur.execute("INSERT INTO `tbl_feedback`(`feedback_description`,`feedback_date`,`user_id`) VALUES ('{}','{}','{}')".format(feedbackdetails,feedbackdate,user_id))
        conn.commit()
        messages.success(request, 'Thank you for Sharing feedback')
        return redirect(feedbackadd) 
    else:
        return redirect(feedbackadd)
    
def feedbackview(request):
    if 'user_id' in request.COOKIES and request.session.has_key('user_id'):
      #cur.execute("Select * from tb_feedback")
        cur.execute('''SELECT
    `tbl_feedback`.`feedback_id`
    , `tbl_feedback`.`feedback_date`
    , `tbl_feedback`.`feedback_description`
    , `tbl_user`.`user_name`
FROM
    `tbl_user`
    INNER JOIN `tbl_feedback` 
        ON (`tbl_user`.`user_id` = `tbl_feedback`.`user_id`);''')
        data = cur.fetchall()
        print(list(data))
        return render(request, 'user/viewfeedback.html', {'mydata': data})
    else:
        return redirect(login)

# def userlogout(request):
#     del request.session['user_email']
#     del request.session['user_id']
#     response = redirect(login)
#     response.delete_cookie('user_id')
#     response.delete_cookie('user_email')
#     return response

def userlogout(request):
  
        del request.session['user_email']
        del request.session['user_id']

        response = redirect('login')  
        response.delete_cookie('user_id')
        response.delete_cookie('user_email')
        return response


def userforgot(request):
    return render(request,'user/userforgot.html')

def userforgotprocess(request):
    print(request.POST)
    txt1 = request.POST['txt1']
    cur.execute("select * from `tbl_user` where `user_email` = '{}' ".format(txt1))
    db_data = cur.fetchone()
        
    if db_data is not None:
        if len(db_data) > 0:
            #Fetch Data
            db_password = db_data[5]
            subject = 'Forgot Password'
            message = ' Your Password is  ' + db_password
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [txt1,]
            send_mail( subject, message, email_from, recipient_list )
            messages.success(request, 'Password Sent on Email ID')
            return redirect(login)
            #Cookie Code
        else:
            messages.success(request, 'User Not Found')
            return render(request, 'user/userforgot.html') 
    messages.success(request, 'User Not Found')    
    return render(request,'user/userforgot.html')



