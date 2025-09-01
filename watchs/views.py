from http.client import responses
from itertools import product
from tkinter.messagebox import RETRY

from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from django.core.signals import request_started
from django.shortcuts import render, redirect
from unicodedata import category

from .models import Product, Contact, Category, Advertisement, Comments, Order
from .forms import Add_product,Update_new,Register_form,Login_form,Comments_form
import requests
from django.db.models import Q

def Home_page(request):
    advertisements=Advertisement.objects.filter(is_active=True)
    phones=Product.published.filter(category__name="Mobile Phones")[1:8]# .order_by('-id')
    watches=Product.published.filter(category__name="Smart Watches")[1:8]# .order_by('-id')

    context={
        "advertisements":advertisements,
        "phones":phones,
        "watches":watches,
    }
    return render(request,'index.html',context)




def add_news(request):
    if request.method == "POST":
        form=Add_product(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = Add_product()
    context = {
        "form": form
    }
    return render(request,"products_add.html",context)



def delete_new(request,pk):
    new =Product.objects.get(pk=pk)
    if new:
        new.delete()
        return redirect('home')

    else:
        return redirect('home')

def update_new(request,pk):
    new=Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = Update_new(request.POST, request.FILES, instance=new)
        if form.is_valid() :
            form.save()
            return redirect('home')
    else:
        form=Update_new(instance=new)
    context={
        'form':form
    }

    return render(request,"update_news.html",context)


# def comments_view(request):
#     if request.method == "POST":
#         form = Comments_form(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("coments")








def contact_view(request):

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")


        if not full_name or not email or not subject or not message:
            context = {
                "error" : "You should fill all sections"
            }

            return render(request,"contact.html",context)

        Contact.objects.create(
            full_name=full_name,
            email=email,
            subject=subject,
            message=message,
        )
        BOT_TOKEN="8070155781:AAF2ksinDJQKB5NRVfYRa5wF7ySSYlD2aqg"
        chat_id="6746520976"

        text=(
            "<b> YANGI MUROJAT !</b>\n\n"
            f"<b> Ismi: !</b>{full_name}\n"
            f"<b> Email: !</b>{email}\n"
            f"<b> Mavzu: !</b>{subject}\n"
            f"<b> Xabar: !</b>{message}\n"
        )

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={
            "chat_id" : chat_id,
            "text" : text,
            "parse_mode" : "HTML"
        })

        context = {
            'success' : 'Your message sent successfully'
        }

        return render(request,'contact.html',context)
    return render(request,"contact.html")




def order_number_view(request):
    if request.method=="POST":
        product= request.POST.get("product_id")
        phone_number = request.POST.get("phone_number")
        region = request.POST.get("region")
        city = request.POST.get("city")
        user = request.POST.get("name")
        payment_type = request.POST.get("payment_type")
        buying_counts = int(request.POST.get("buying_count", 1))

        if not product or not user or not region or not payment_type or not region or not city or not phone_number:
            context={
                "error":"You should fill all sections"
            }
            return render(request,"buy_now.html")

        Order.objects.create(
            product=product,
            user=user,
            payment_type=payment_type,
            delevering_point=region,
            buying_count=buying_counts,
        )

        BOT_TOKEN="8116151852:AAEE0nDf-lqfAHR8inJXk5LdxT-_aHl5EBQ"
        chat_id="6746520976"

        text=(
            "<b>🛒 YANGI BUYURTMA!</b>\n\n"
            f"<b>📦 Maxsulot nomi:</b> {product}\n"
            f"<b>📞 Buyurtmachi:</b> {user}\n"
            f"<b>💳 To'lov turi:</b> {payment_type}\n"
            f"<b>📍 Yetkazib berish manzili:</b> {region},{city}\n"
            f"<b>🔢 Maxsulot soni:</b> {buying_counts}\n"
        )

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={
            "chat_id" : chat_id,
            "text" : text,
            "parse_mode" : "HTML"
        })

        context = {
            'success' : 'Your product ordered successfully'
        }

        return render(request,"index.html",context)
    return render(request,"index.html")






# under the line I/ll write a register views

def Register_view(request):
    if request.method == "POST":
        form = Register_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = Register_form()
    context={
        "form" : form
    }
    return render(request,'register.html',context)

def Login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = Login_form(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user(   )
            login(request, user)
            return redirect("home")
    else:
        form = Login_form()
    context = {
        "form" : form
    }
    return render(request,'login.html',context)

def Logout(request):
    logout(request)
    return redirect('home')



# Detailed sections

def detailed_view(request,slug):
    products=Product.objects.get(slug=slug)

    related_products=Product.objects.filter(category=products.category)[1:8]


    if request.method=="POST":
        if not request.user.is_authenticated:
            return redirect("register_pro")
        return redirect("detail",slug=products.slug)


    context={
        "product":products,
        "related_products":related_products
    }
    return render(request,"single_page.html",context)

def buy_now_view(request,slug):
    product=Product.objects.get(slug=slug)
    stock=product.stock_count

    context={
        "products":product,
        "stock":stock,
    }

    return render(request,"buy_now.html",context)




def Aksesuar_view(request):
    aksessuar = Product.published.filter(category__name="Accessories")

    paginator=Paginator(aksessuar,20)
    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number)

    context={
        "aksessuars":aksessuar,
        "page_obj":page_obj
    }
    return render(request,"aksessuars.html",context)


def Headphones_view(request):
    head = Product.published.filter(category__name="Headphones")

    paginator=Paginator(head,20)
    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number)

    context={
        "headphone":head,
        "page_obj":page_obj

    }
    return render(request,"headphones.html",context)


def Mobile_phones_view(request):
    phone = Product.published.filter(category__name="Mobile Phones")

    paginator=Paginator(phone,20)
    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number)

    context={
        "phone":phone,
        "page_obj":page_obj
    }
    return render(request,"mobile_phones.html",context)


def Smart_watches_view(request):
    watches = Product.published.filter(category__name="Smart Watches")

    paginator=Paginator(watches,20)
    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number)

    context={
        "watches":watches,
        "page_obj":page_obj
    }
    return render(request,"smart_watches.html",context)


def Speakers_view(request):
    speaker = Product.published.filter(category__name="Speakers")

    paginator=Paginator(speaker,20)
    page_number=request.GET.get("page")
    page_obj=paginator.get_page(page_number)

    context={
        "speaker":speaker,
        "page_obj":page_obj
    }
    return render(request,"speakers.html",context)

# Search funtions
def search_view(request):
    query=request.GET.get('q')
    if query:
        response=Product.published.filter(Q(name__icontains=query))

    else:
        response=None
    paginator=Paginator(query,12)
    page_number =request.GET.get('page')
    page_obj=paginator.get_page(page_number)

    context={
        "response":response,
        "page_obj":page_obj,
    }

    return render(request,"search.html",context)


# def search_view(request):
#     query = request.GET.get('q')
#     if query:
#         response = New.published.filter(Q(title__icontains=query))
#
#     else:
#         response = None
#     paginator = Paginator(query,2)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     context = {
#         "response" : response,
#         "page_obj" : page_obj,
#     }
#     return render(request,"search.html",context)



# def detail(request):
#     return render(request,"single_page.html")


# About html
def about_view(request):
    return render(request,"about.html")

# Buy now view

def add_to_card_views(request):
    return render(request,"card.html")







