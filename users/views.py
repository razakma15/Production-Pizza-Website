import stripe
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import *
from django.db import IntegrityError

# When the context dictionary has a key called data this is for succes/error messages displayed at redirect.html
# Function which is called on main webpage and displays the amount of items in the user's basket.
def index(request):
    if request.user.is_authenticated == True:
        return render(request, "users/index.html",{"basket_quantity":request.user.basket_quantity})
    else:
        return render(request, "users/index.html",{"basket_quantity":0})
# Simple authentication function which is called when login modal is submitted, uses post for extra security.
def login_view(request):
    logout(request)
    username = request.POST["username"]
    email = request.POST["email"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password, email=email)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        context={"data":"Invalid Credentials"}
        return render(request,"users/redirect.html",context)
# Uses the django included logout function
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
# Creates new user and catches Integrity / Unique exeption error's then redirect's to error page.
def register(request):
    try:
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        user = CustomUser.objects.create_user(username, email, password)
        user.save()
        return HttpResponseRedirect(reverse("index"))
    except IntegrityError:
        context={"data":"Email already in use!"}
        return render(request,"users/redirect.html",context)
# The meat of the website, created for maximum flexibility by checking if all types of food are present so on the menu.html page only
# necessary subtitles are displayed.
def menu(request):
    x = 0
    if request.user.is_authenticated:
        x = request.user.basket_quantity
    context = {
    "Meal":Meal.objects.all(),
    "basket_quantity":x,
    "Main": Meal.objects.filter(type__iexact='Main').exists(),
    "Premium": Meal.objects.filter(type__iexact='Premium').exists(),
    "Side": Meal.objects.filter(type__iexact='Side').exists(),
    "Dessert": Meal.objects.filter(type__iexact='Dessert').exists(),
    }
    return render(request,"users/menu.html",context)
# Process ajax request to check if menu items are already in basket before adding to user model to prevent data error's.
# Uses in-built django ORM to make queries.
def ajax_basket(request):
    if request.user.is_authenticated:
        req_data = request.GET.get('food_title', None)
        filter_data = Meal.objects.get(title__iexact=req_data)
        if  request.user.meal.filter(title__iexact=req_data).exists():
            data = {'is_taken': "Copy"}
        else:
            request.user.meal.add(filter_data)
            request.user.basket_quantity += 1
            request.user.save()
            data = {"is_taken" : "Not Copy"}
        return JsonResponse(data)
    else:
        data = {"is_taken" : "No_Login"}
        return JsonResponse(data)
# Redirects to checkout if the user is authenticated and has at least one food item.
# Sends Stripe_key though the context notation to be used by the checkout button.
def basket(request):
    if request.user.is_authenticated:
        if request.user.meal.count() == 0:
            context={"data":"No Pizza's Added!"}
            return render(request,"users/redirect.html",context)
        else:
            context = {
            "user_meals":request.user.meal.all(),
            "basket_quantity":request.user.basket_quantity,
            "key":settings.STRIPE_PUBLISHABLE_KEY,
            }
            return render(request,"users/checkout.html",context)
    else:
        context = {"data":"Please Login First"}
        return render(request,"users/redirect.html",context)
# Ajax request which finds a Meal object with a matching name then removes food object from user object.
def ajax_checkout(request):
    req_data = request.GET.get('food_title', None)
    filter_data = Meal.objects.get(title__iexact=req_data)
    request.user.meal.remove(filter_data)
    request.user.basket_quantity -= 1
    request.user.save()
    data = {"request":req_data}
    return JsonResponse(data)
# Process payment of food objects by sending a request to stripe payment servers using their api, then clearing all food objects relating to the user
# Setting the basket to 0 and redirecting the user back to the main page.
def charge(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        total_cost = str(request.POST["total_cost"]) + str("00")
        charge = stripe.Charge.create(
            amount=total_cost,
            currency='gbp',
            description='A Pizza Payment',
            source=request.POST['stripeToken']
        )
        request.user.meal.clear()
        request.user.basket_quantity = 0
        request.user.save()
        context={"data":"Payment Succesfully Processed"}
        return render(request,'users/redirect.html',context)
