from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('mailsendprocess/',views.mailsendprocess,name='mailsendprocess'),
    
    path('cart/',views.cart,name='cart'),

    path('userhome/',views.userhome,name='userhome'),
    path('login/',views.login,name='login'),
    path('login_process/',views.login_process,name='login_process'),

    path('logout/',views.userlogout,name='logout'),

    path('change_password/',views.change_password,name='change_password'),
    path('change_passwordprocess/',views.change_passwordprocess,name='change_passwordprocess'),

    path('signup/',views.signup,name='signup'),
    path('signupprocess',views.signupprocess,name='signupprocess'),

    path('product/',views.product,name='product'),
    path("listing/<int:id>",views.productlistingbycategory),
    path("search/",views.productsearch),
    path('product_details/<int:id>',views.product_details,name='product_details'),
    
      
    path('addtocart/<int:id>', views.addtocart, name="addtocart"),
    path('cartview', views.cartview, name='cartview'),
    path('cartremove/<int:id>', views.cartremove, name="cartremove"),
    path('thanks', views.thanks, name='cartview'),
    path('checkout', views.checkout, name='checkout'),
    path('placeorder', views.placeorder, name='cartview'),
     path('orderview', views.orderview, name='cartview'),
    path('orderdetails/<int:id>', views.orderdetailsview, name='cartview'),
    
    path('checkout/', views.checkout, name='checkout'),  
   
   
    path('feedback', views.feedbackadd, name='feedbackadd'),
    path('feedbackprocess', views.feedbackaddprocess, name="feedbackaddprocess"),
    path('feedbackview', views.feedbackview, name='feedbackview'),

    path('userforgot',views.userforgot),
    path('userforgotprocess',views.userforgotprocess),


    

    
     
]