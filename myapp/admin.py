from django.contrib import admin
from. models import Contact,User,Product,Wishlist,Cart   # next step-----> **also need to import in views.py ****

# Register your models here.     
admin.site.register(Contact)
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Wishlist)
admin.site.register(Cart)