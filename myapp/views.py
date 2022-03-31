import email
from email import message
from itertools import product
from urllib.request import Request
from django.shortcuts import render,redirect  #already exist
from. models import Contact, Product, Wishlist,Cart,Transaction # for contact ,product
from. models import User # for user 

from django.http import JsonResponse  #for validate_signup

#--------------------------PAYMENT-Library--------------------------------------------------------------------------------
from django.shortcuts import render
from django.conf import settings
from .models import Transaction
from .paytm import generate_checksum, verify_checksum

from django.views.decorators.csrf import csrf_exempt #callback



#-------------------------PAYMENT - DEF-----------------------------------------------------------------------------------------
def initiate_payment(request):
    user=User.objects.get(email=request.session['email'])
    try:
       
        amount = int(request.POST['amount'])
        
    except:
        return render(request, 'pay.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=user,amount=amount)
    transaction.save()
    carts= Cart.objects.filter(user=user)
    for i in carts:
        i.payment_status="paid"
        i.save()
        
    carts= Cart.objects.filter(user=user,payment_status="pending")
    request.session['cart_count']=len(carts) 
    
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://localhost:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)

#----------------def---callback---------------------------------------------------------------------------------------------------------

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        return render(request, 'callback.html', context=received_data)

#-------------------------PAYMENT_DEF- ENDS-------------------------------------------------------------------------------------

# Create your views here.
def index(request):
    try:
        user=User.objects.get(email=request.session['email'])
        if user.usertype=="user":
            return render (request,'index.html')
        else:
            return render (request,'seller_index.html')
    except:
        return render (request,'index.html')

def about (request):
    return render (request,'about.html')
#--------------------------------------------Shop.html-----------------------------------------------------
def shop (request):
    products=Product.objects. all()  #class Product ka all data fatch kiya = products me 
    all=len(products)   #all product ll count
    men=len(Product.objects.filter(product_collection="men")) # yha se ham len le jaynge and shop.html me (men) ki len fing hogi
    women=len(Product.objects.filter(product_collection="women"))
    kids=len(Product.objects.filter(product_collection="kids"))
    return render (request,'shop.html', {'all':all,'products':products,'men':men,'women':women,'kids':kids}) #products se for loop use kiya 

             #for collection-----------------

def collection_men(request):                 #all copy from def shop
    products=Product.objects. all()  #class Product ka all data fatch kiya = products me 
    all=len(products)   #all product ll count
    products=Product.objects.filter(product_collection="men")     #class Product ka men  data fatch(filter) kiya = products me 
    men=len(Product.objects.filter(product_collection="men"))           # yha se ham len le jaynge and shop.html me (men) ki len fing hogi
    women=len(Product.objects.filter(product_collection="women"))
    kids=len(Product.objects.filter(product_collection="kids"))
    return render (request,'shop.html', {'all':all, 'products':products,'men':men,'women':women,'kids':kids})         #products se for loop use kiya 
 
def collection_women(request):                 #all copy from def shop
    products=Product.objects. all()  #class Product ka all data fatch kiya = products me 
    all=len(products)   #all product ll count
    products=Product.objects.filter(product_collection="women")     #class Product ka men  data fatch(filter) kiya = products me 
    men=len(Product.objects.filter(product_collection="men"))           # yha se ham len le jaynge and shop.html me (men) ki len fing hogi
    women=len(Product.objects.filter(product_collection="women"))
    kids=len(Product.objects.filter(product_collection="kids"))
    return render (request,'shop.html', {'all':all,'products':products,'men':men,'women':women,'kids':kids})         #products se for loop use kiya 
 
def collection_kids(request):                 #all copy from def shop
    products=Product.objects. all()  #class Product ka all data fatch kiya = products me 
    all=len(products)   #all product ll count
    products=Product.objects.filter(product_collection="kids")     #class Product ka men  data fatch(filter) kiya = products me 
    men=len(Product.objects.filter(product_collection="men"))           # yha se ham len le jaynge and shop.html me (men) ki len fing hogi
    women=len(Product.objects.filter(product_collection="women"))
    kids=len(Product.objects.filter(product_collection="kids"))
    return render (request,'shop.html', {'all':all,'products':products,'men':men,'women':women,'kids':kids})         #products se for loop use kiya 
        
               #for category-----------------
               
               
def category_shirt (request):
    products=Product.objects. all()  #class Product ka all data fatch kiya = products me 
    all=len(products)   #all product ll count
    products=Product.objects.filter(product_category="shirt")     #class Product ka shirt  data fatch(filter) kiya = products me 
    shirt=len(Product.objects.filter(product_category="shirt")) # yha se ham len le jaynge and shop.html me (shirt) ki len fing hogi
    tshirt=len(Product.objects.filter(product_category="tshirt"))
    jeans=len(Product.objects.filter(product_category="jeans"))
    return render (request,'shop.html', {'all':all,'products':products,'shirt':shirt,'tshirt':tshirt,'jeans':jeans}) #products se for loop use kiya                

def category_tshirt (request):
    products=Product.objects. all()  #class Product ka all data fatch kiya = products me 
    all=len(products)   #all product ll count
    products=Product.objects.filter(product_category="tshirt")     #class Product ka tshirt  data fatch(filter) kiya = products me 
    shirt=len(Product.objects.filter(product_category="shirt")) # yha se ham len le jaynge and shop.html me (tshirt) ki len fing hogi
    tshirt=len(Product.objects.filter(product_category="tshirt"))
    jeans=len(Product.objects.filter(product_category="jeans"))
    return render (request,'shop.html', {'all':all,'products':products,'shirt':shirt,'tshirt':tshirt,'jeans':jeans}) #products se for loop use kiya                

def category_jeans (request):
    products=Product.objects. all()  #class Product ka all data fatch kiya = products me 
    all=len(products)   #all product ll count
    products=Product.objects.filter(product_category="jeans")     #class Product ka jeans  data fatch(filter) kiya = products me 
    shirt=len(Product.objects.filter(product_category="shirt")) # yha se ham len le jaynge and shop.html me (jeans) ki len fing hogi
    tshirt=len(Product.objects.filter(product_category="tshirt"))
    jeans=len(Product.objects.filter(product_category="jeans"))
    return render (request,'shop.html', {'all':all,'products':products,'shirt':shirt,'tshirt':tshirt,'jeans':jeans}) #products se for loop use kiya                

                #for size-----------------
                
                
                
def size_small (request):
    products=Product.objects. all()  #class Product ka all data fatch kiya = products me 
    all=len(products)   #all product ll count
    products=Product.objects.filter(product_size="s")     #class Product ka jeans  data fatch(filter) kiya = products me 
    small=len(Product.objects.filter(product_size="s")) # yha se ham len le jaynge and shop.html me (jeans) ki len fing hogi
    medium=len(Product.objects.filter(product_size="m"))
    large=len(Product.objects.filter(product_size="l"))
    return render (request,'shop.html', {'all':all,'products':products,'small':small,'medium':medium,'large':large}) #products se for loop use kiya                

def size_medium (request):
    products=Product.objects. all()  #class Product ka all data fatch kiya = products me 
    all=len(products)   #all product ll count
    products=Product.objects.filter(product_size="m")     #class Product ka jeans  data fatch(filter) kiya = products me 
    small=len(Product.objects.filter(product_size="s")) # yha se ham len le jaynge and shop.html me (jeans) ki len fing hogi
    medium=len(Product.objects.filter(product_size="m"))
    large=len(Product.objects.filter(product_size="l"))
    return render (request,'shop.html', {'all':all,'products':products,'small':small,'medium':medium,'large':large}) #products se for loop use kiya               

def size_large (request):
    products=Product.objects. all()  #class Product ka all data fatch kiya = products me 
    all=len(products)   #all product ll count
    products=Product.objects.filter(product_size="l")     #class Product ka jeans  data fatch(filter) kiya = products me 
    small=len(Product.objects.filter(product_size="s")) # yha se ham len le jaynge and shop.html me (jeans) ki len fing hogi
    medium=len(Product.objects.filter(product_size="m"))
    large=len(Product.objects.filter(product_size="l"))
    return render (request,'shop.html', {'all':all,'products':products,'small':small,'medium':medium,'large':large}) #products se for loop use kiya                             

                #for color-----------------
                
                
                
def color_blue (request):
    products=Product.objects. all()  #class Product ka all data fatch kiya = products me 
    all=len(products)   #all product ll count
    products=Product.objects.filter(product_color="blue")     #class Product ka jeans  data fatch(filter) kiya = products me 
    blue=len(Product.objects.filter(product_color="blue")) # yha se ham len le jaynge and shop.html me (jeans) ki len fing hogi
    black=len(Product.objects.filter(product_color="black"))
    white=len(Product.objects.filter(product_color="white"))
    pink=len(Product.objects.filter(product_color="pink")) # yha se ham len le jaynge and shop.html me (jeans) ki len fing hogi
    green=len(Product.objects.filter(product_color="green"))
    red=len(Product.objects.filter(product_color="red"))
    yellow=len(Product.objects.filter(product_color="yellow")) # yha se ham len le jaynge and shop.html me (jeans) ki len fing hogi
    return render (request,'shop.html', {'all':all,'products':products,'blue':blue,'black':black,'white':white,'pink':pink,'green':green,'red':red,'yellow':yellow}) #products se for loop use kiya                             

def color_black (request):
    products=Product.objects. all()  #class Product ka all data fatch kiya = products me 
    all=len(products)   #all product ll count
    products=Product.objects.filter(product_color="black")     #class Product ka jeans  data fatch(filter) kiya = products me 
    blue=len(Product.objects.filter(product_color="blue")) # yha se ham len le jaynge and shop.html me (jeans) ki len fing hogi
    black=len(Product.objects.filter(product_color="black"))
    white=len(Product.objects.filter(product_color="white"))
    pink=len(Product.objects.filter(product_color="pink")) # yha se ham len le jaynge and shop.html me (jeans) ki len fing hogi
    green=len(Product.objects.filter(product_color="green"))
    red=len(Product.objects.filter(product_color="red"))
    yellow=len(Product.objects.filter(product_color="yellow")) # yha se ham len le jaynge and shop.html me (jeans) ki len fing hogi
    return render (request,'shop.html', {'all':all,'products':products,'blue':blue,'black':black,'white':white,'pink':pink,'green':green,'red':red,'yellow':yellow}) #products se for loop use kiya                             

def color_white (request):
    products=Product.objects. all()  #class Product ka all data fatch kiya = products me 
    all=len(products)   #all product ll count
    products=Product.objects.filter(product_color="white")     #class Product ka jeans  data fatch(filter) kiya = products me 
    blue=len(Product.objects.filter(product_color="blue")) # yha se ham len le jaynge and shop.html me (jeans) ki len fing hogi
    black=len(Product.objects.filter(product_color="black"))
    white=len(Product.objects.filter(product_color="white"))
    pink=len(Product.objects.filter(product_color="pink")) # yha se ham len le jaynge and shop.html me (jeans) ki len fing hogi
    green=len(Product.objects.filter(product_color="green"))
    red=len(Product.objects.filter(product_color="red"))
    yellow=len(Product.objects.filter(product_color="yellow")) # yha se ham len le jaynge and shop.html me (jeans) ki len fing hogi
    return render (request,'shop.html', {'all':all,'products':products,'blue':blue,'black':black,'white':white,'pink':pink,'green':green,'red':red,'yellow':yellow}) #products se for loop use kiya                             

def color_pink (request):
    products=Product.objects. all()  #class Product ka all data fatch kiya = products me 
    all=len(products)   #all product ll count
    products=Product.objects.filter(product_color="pink")     #class Product ka jeans  data fatch(filter) kiya = products me 
    blue=len(Product.objects.filter(product_color="blue")) # yha se ham len le jaynge and shop.html me (jeans) ki len fing hogi
    black=len(Product.objects.filter(product_color="black"))
    white=len(Product.objects.filter(product_color="white"))
    pink=len(Product.objects.filter(product_color="pink")) # yha se ham len le jaynge and shop.html me (jeans) ki len fing hogi
    green=len(Product.objects.filter(product_color="green"))
    red=len(Product.objects.filter(product_color="red"))
    yellow=len(Product.objects.filter(product_color="yellow")) # yha se ham len le jaynge and shop.html me (jeans) ki len fing hogi
    return render (request,'shop.html', {'all':all,'products':products,'blue':blue,'black':black,'white':white,'pink':pink,'green':green,'red':red,'yellow':yellow}) #products se for loop use kiya                             

def color_green (request):
    products=Product.objects. all()  #class Product ka all data fatch kiya = products me 
    all=len(products)   #all product ll count
    products=Product.objects.filter(product_color="green")     #class Product ka jeans  data fatch(filter) kiya = products me 
    blue=len(Product.objects.filter(product_color="blue")) # yha se ham len le jaynge and shop.html me (jeans) ki len fing hogi
    black=len(Product.objects.filter(product_color="black"))
    white=len(Product.objects.filter(product_color="white"))
    pink=len(Product.objects.filter(product_color="pink")) # yha se ham len le jaynge and shop.html me (jeans) ki len fing hogi
    green=len(Product.objects.filter(product_color="green"))
    red=len(Product.objects.filter(product_color="red"))
    yellow=len(Product.objects.filter(product_color="yellow")) # yha se ham len le jaynge and shop.html me (jeans) ki len fing hogi
    return render (request,'shop.html', {'all':all,'products':products,'blue':blue,'black':black,'white':white,'pink':pink,'green':green,'red':red,'yellow':yellow}) #products se for loop use kiya                             

def color_red (request):
    products=Product.objects. all()  #class Product ka all data fatch kiya = products me 
    all=len(products)   #all product ll count
    products=Product.objects.filter(product_color="red")     #class Product ka jeans  data fatch(filter) kiya = products me 
    blue=len(Product.objects.filter(product_color="blue")) # yha se ham len le jaynge and shop.html me (jeans) ki len fing hogi
    black=len(Product.objects.filter(product_color="black"))
    white=len(Product.objects.filter(product_color="white"))
    pink=len(Product.objects.filter(product_color="pink")) # yha se ham len le jaynge and shop.html me (jeans) ki len fing hogi
    green=len(Product.objects.filter(product_color="green"))
    red=len(Product.objects.filter(product_color="red"))
    yellow=len(Product.objects.filter(product_color="yellow")) # yha se ham len le jaynge and shop.html me (jeans) ki len fing hogi
    return render (request,'shop.html', {'all':all,'products':products,'blue':blue,'black':black,'white':white,'pink':pink,'green':green,'red':red,'yellow':yellow}) #products se for loop use kiya                             
              
def color_yellow (request):
    products=Product.objects. all()  #class Product ka all data fatch kiya = products me 
    all=len(products)   #all product ll count
    products=Product.objects.filter(product_color="yellow")     #class Product ka jeans  data fatch(filter) kiya = products me 
    blue=len(Product.objects.filter(product_color="blue")) # yha se ham len le jaynge and shop.html me (jeans) ki len fing hogi
    black=len(Product.objects.filter(product_color="black"))
    white=len(Product.objects.filter(product_color="white"))
    pink=len(Product.objects.filter(product_color="pink")) # yha se ham len le jaynge and shop.html me (jeans) ki len fing hogi
    green=len(Product.objects.filter(product_color="green"))
    red=len(Product.objects.filter(product_color="red"))
    yellow=len(Product.objects.filter(product_color="yellow")) # yha se ham len le jaynge and shop.html me (jeans) ki len fing hogi
    return render (request,'shop.html', {'all':all,'products':products,'blue':blue,'black':black,'white':white,'pink':pink,'green':green,'red':red,'yellow':yellow}) #products se for loop use kiya                             



def cart (request):
    return render (request,'cart.html')

def blog (request):
    return render (request,'blog.html')
#--------------------------------------------Contact-----------------------------------------------------


def contact (request):
    if request.method=="POST":
        Contact.objects.create(
        fname=request.POST['fname'],
        lname=request.POST['lname'],
        email=request.POST['email'],
        subject=request.POST['subject'],
        message=request.POST['message'],
      )
        msg="Contact Saved Successfully."
        return render (request,'contact.html', {'msg':msg})
    else:
        return render (request,'contact.html',)
        
#--------------------Sign up-----------------------------------------------------------------------------

def signup(request):
    if request.method=="POST":
        try:
            User.objects.get(email=request.POST['email'])   #check the email is register or not 
            msg="That Email Is Already Registered. Try Another."
            return render(request,'signup.html', {'msg':msg})
            
        except:
            if request.POST['password']==request.POST['cpassword']:
                User.objects.create(
                    usertype=request.POST['usertype'],
                    fname=request.POST['fname'],
                    lname=request.POST['lname'],
                    email=request.POST['email'],
                    mobile=request.POST['mobile'],
                    address=request.POST['address'],
                    password=request.POST['password'],   
                )
                msg="User Sign Up Successfully 🎀🎗️"
                return render(request,'login.html',{'msg':msg})
            else:
                msg="Password & Confirm Password Do Not Matched 🚫"
                return render(request,'signup.html',{'msg':msg})
            
    else:
        return render(request,'signup.html')
    
    
#--------------------Log In-------------------------------------------------------------------------------------------


def login(request):
    if request.method=="POST":
        try:
            user=User.objects.get(
                email=request.POST['email'], # here we check the enter email in login with database
                password=request.POST['password']  #same check password in database 
              )
            if user.usertype=='user':  #if user select *user* then index.html ll open to buy product.
                request.session['email']=user.email  #login ke bad session banega user ka .  header.html me if else .
                request.session['fname']=user.fname
                
                wishlists=Wishlist.objects.filter(user=user) # in wishlist count  the number of product ll diplay when user login
                request.session['wishlist_count']=len(wishlists)
                
                carts= Cart.objects.filter(user=user) # in cart count  the number of product ll diplay when user login
                request.session[' cart_count']=len(carts)     #ll opn header.html ll make session
                
                
                
                return render(request,'index.html')  #email, pass.. match then go in home page !!
            
            else:  #if user select *seller* then seller_index.html ll open to *sell* product.
                request.session['email']=user.email  
                request.session['fname']=user.fname
                return render(request,'seller_index.html')  
                
        
        except:
            msg="Email & Pasword Is Incorrect 🚫"
            return render(request,'login.html', {'msg':msg})
           
    else:
        return render(request,'login.html')


def single_product(request):
    return render(request,'product-single.html')

def checkout(request):
    return render(request,'checkout.html')


#--------------------Log out---------------------------------------------------------------------------------


def logout(request):
    try:
        del request.session['email']
        del request.session['fname']
        return render(request,'login.html') 
    
    except:
        return render(request,'login.html')

#--------------------Change Password-----------------------------------------------------------------------------


def change_password (request):
    user=User.objects.get(email=request.session['email'])    #check email here with database
    if user.usertype=="user": #agar signup user ki side se hua to ye rule follow hoga:*****************
        if request.method=="POST":
            
            if user.password==request.POST['oldpassword']:  #current password match with database password.
                if request.POST['newpassword']==request.POST['cnewpassword']: #check pass & confirm pass match or not 
                    user.password=request.POST['newpassword']    #old pas remove new passsword ll save 
                    user.save()
                    return redirect ('logout')
                else:
                    msg="New Password and confirm Password Do Not Matched 🚫 "
                    return render(request,'change_password.html',{'msg':msg})
            else:
                msg="Current Password Do Not Matched 🚫 "
                return render(request,'change_password.html',{'msg':msg})
        else:
            return render(request,'change_password.html')
        
    else:  #this we did for ***seller*** side change passsword
        if request.method=="POST":
                
                if user.password==request.POST['oldpassword']:  #current password match with database password.
                    if request.POST['newpassword']==request.POST['cnewpassword']: #check pass & confirm pass match or not 
                        user.password=request.POST['newpassword']    #old pas remove new passsword ll save 
                        user.save()
                        return redirect ('logout')
                    else:
                        msg="New Password and confirm Password Do Not Matched 🚫 "
                        return render(request,'seller_change_password.html',{'msg':msg})
                else:
                    msg="Current Password Do Not Matched 🚫 "
                    return render(request,'seller_change_password.html',{'msg':msg})
        else:
            return render(request,'seller_change_password.html')
        
        
#--------------------------------------------------------------------------------------------------------------------- 
      
#--------------------Seller side HOME-PAGE-----------------------------------------------------------------------------              
def seller_index(request):
    return render(request,'seller_index.html')

#--------------------Seller side Add Product !!-----------------------------------------------------------------------------       

def seller_add_product(request):
    if request.method=="POST":
        product_seller=User.objects.get(email=request.session['email']) #['email]<--- ye email ko aage wale email se mathch krke Product_seller me rakhenge
        
        Product.objects.create(
            product_seller=product_seller,
            product_collection=request.POST['product_collection'],
            product_category=request.POST['product_category'],
            product_size=request.POST['product_size'],
            product_color=request.POST['product_color'],
            product_price=request.POST['product_price'],
            product_desc=request.POST['product_desc'],
            product_image=request.FILES['product_image'],
            
        )
        msg="Product Added Successfully 🎀🎗️"
        return render(request,'seller_add_product.html',{'msg':msg})
        
        
    else:
        return render(request,'seller_add_product.html')

#--------------------Seller side VIEW-PAGE----------------------------------------------------------------------------- 
      
def seller_view_product(request):
    product_seller=User.objects.get(email=request.session['email'])       #first we bring email of active user in product_seller
    product=Product.objects.filter(product_seller=product_seller)          #Product.objects.filter(product_seller=---) meaning is that Models ke Product me jo product_seller hai usme<--(---)ki value dal do
    return render(request,'seller_view_product.html',{'product':product})


#--------------------Seller side EDIT-PRODUCT-----------------------------------------------------------------------------    
def seller_edit_product(request,pk):
    product=Product.objects.get(pk=pk)
    if request.method=="POST":
        product.product_collection=request.POST['product_collection']
        product.product_category=request.POST['product_category']
        product.product_size=request.POST['product_size']
        product.product_color=request.POST['product_color']
        product.product_price=request.POST['product_price']
        product.product_desc=request.POST['product_desc']
        
        #we use try block for image may user change the image if not then use except :
        try:
            product.product_image=request.FILES['product_image']
            
        except:
            pass
               
        product.save()
        return render(request,'seller_edit_product.html',{'product':product})      
      
    else:
        return render(request,'seller_edit_product.html',{'product':product})
    
    
#--------------------Seller side DELETE-PRODUCT-----------------------------------------------------------------------------             
def seller_delete_product(request,pk):
    product=Product.objects.get(pk=pk)
    product.delete()
    return redirect(seller_view_product)

#-------------------WISHLIST-----------------------------------------------------------------------------

def product_detail(request,pk):
    wishlist_flag=False   #product is not in wishlist------------->
    cart_flag=False       #product is not in cart------------->
    product=Product.objects.get(pk=pk) #product fatch
    user=User.objects.get(email=request.session['email'])#User email fatch
    
    try:
        Wishlist.objects.get(user=user,product=product) #user and product leke aaye 
        wishlist_flag=True  #product is in wishlist------------->
    except:
        pass   #use if cond..in product_detail.html at add to widhlist button
    
    
#--------------------------for cart as same as wishlist---------------------------------------------------------------------
    try:
        Cart.objects.get(user=user,product=product,payment_status="pending") #user and product leke aaye 
        cart_flag=True  #product is incart------------->
    except:
        pass   #use if cond..in product_detail.html at add to widhlist button
    
    
    return render(request,'product_detail.html',{'product':product ,'wishlist_flag':wishlist_flag ,'cart_flag':cart_flag})

def add_to_wishlist(request,pk):
    product=Product.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    Wishlist.objects.create(
        # hamne wishlist ke models me 3 things add ki hai  user product and() date which is auto no need to put here )
        user=user,
        product=product 
    )
    return redirect('wishlist')

def wishlist(request):
    user=User.objects.get(email=request.session['email'])
    wishlists= Wishlist.objects.filter(user=user)
    
    #count then save in wishlist_count then--> print in header's heart(wishlist) span tag 
    request.session['wishlist_count']=len(wishlists)   #in wishlist count  the number of product ll diplay when user add / remove in wishlist
    
    return render(request,'wishlist.html',{'wishlists': wishlists})


def remove_from_wishlist(request,pk):
    product=Product.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    wishlist=Wishlist.objects.get(user=user,product=product)
    wishlist.delete()
    return redirect('wishlist')
    
#-------------------ADD_TO_CART-----------------------------------------------------------------------------

def add_to_cart(request,pk):
    product=Product.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    Cart.objects.create(
        # hamne wishlist ke models me 3 things add ki hai  user product and() date which is auto no need to put here )
        user=user,
        product=product,
        product_price=product.product_price,
        product_qty=1,
        total_price=product.product_price
    )
    return redirect('cart')

def cart(request):
    net_price=0  #for subtotal vt=19:13 v=12
    user=User.objects.get(email=request.session['email'])
    carts= Cart.objects.filter(user=user,payment_status="pending")
    
    for i in carts:  # subtotal in cart
        net_price=net_price+i.total_price
    
    #count then save in wishlist_count then--> print in header's heart(wishlist) span tag 
    request.session['cart_count']=len(carts)   #in wishlist count  the number of product ll diplay when user add / remove in wishlist
    
    return render(request,'cart.html',{'carts': carts ,'net_price': net_price})


def remove_from_cart(request,pk):
    product=Product.objects.get(pk=pk)
    user=User.objects.get(email=request.session['email'])
    cart=Cart.objects.get(user=user,product=product,payment_status="pending")
    cart.delete()
    return redirect('cart')

def change_qty(request):
    cart=Cart.objects.get(pk=request.POST['cid'])
    product_qty=int(request.POST['product_qty'])
    cart.product_qty=product_qty
    cart.total_price=cart.product_price*product_qty
    cart.save()
    return redirect('cart')

def myorders(request):
    user=User.objects.get(email=request.session['email'])
    carts= Cart.objects.filter(user=user,payment_status="paid")
    return render(request,'myorders.html',{'carts': carts })


def validate_signup(request):
	email=request.GET.get('email')
	data={
		'is_taken':User.objects.filter(email__iexact=email).exists()
	}
	return JsonResponse(data)
    