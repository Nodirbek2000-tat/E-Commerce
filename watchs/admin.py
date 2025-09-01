from django.contrib import admin
from .models import Users,Category,Payment_type,Comment_type,Comments,Product,Order,Contact,Advertisement,PublishedManager


admin.site.register(Users)
admin.site.register(Category)
admin.site.register(Payment_type)
admin.site.register(Comment_type)
admin.site.register(Comments)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Contact)
admin.site.register(Advertisement)
# admin.site.register(PublishedManager)
