from django.shortcuts import redirect, render
from django.contrib import messages
from .models import *
import bcrypt
# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.basic_validator(request.POST)
    
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    this_user = User.objects.create(first_name= request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
    request.session['user_id'] = this_user.id
    return redirect('/quotes')


def success(request):
    if "user_id" not in request.session:
        return redirect('/')
    context = {
        "user" : User.objects.get(id=request.session['user_id']),
        "quotes" : Quotes.objects.all()
    }
    return render(request, 'home.html', context)

def logout(request):
    del request.session['user_id']
    return redirect('/')

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            return redirect('/quotes')
    
    return redirect('/')

def addQuote(request):
    errors = Quotes.objects.quote_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    new_quote = Quotes.objects.create(author=request.POST['author'], quote=request.POST['quote'], uploaded_by=User.objects.get(id=request.session['user_id']))
    new_quote.likes.add(User.objects.get(id=request.session['user_id']))
    return redirect('/quotes')
def displayQuote(request, id):
    context ={
        "quote" : Quotes.objects.get(id=id)
    }
    return render(request, 'singleQuotePage.html', context)

def deleteQuote(request, id):
    quote = Quotes.objects.get(id=id)
    quote.delete()
    return redirect('/quotes')

def likeQuote(request, id):
    user = User.objects.get(id=request.session['user_id'])
    liked_quote = Quotes.objects.get(id=id)
    liked_quote.likes.add(user)
    return redirect('/quotes')
def displayUserPage(request, id):
    context = {
        "user" : User.objects.get(id=id),
        "logged_user" : User.objects.get(id=request.session['user_id']),
    }
    # if context['user'] == context['logged_user']:
    #     return redirect('/myaccount/'+str(request.session['user_id']))
    return render(request, 'user_page.html', context)
    
def displayMyAccount(request, id):
    if id == request.session['user_id']:
        context = {
            "user": User.objects.get(id=request.session['user_id'])
        }
    else:
        return redirect('/quotes')
    return render(request, 'edit_user.html', context)

def updateAccount(request, id):
    errors = User.objects.update_validator(request.POST)
    user = User.objects.get(id=request.session['user_id'])
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/myaccount/'+str(id))
    else:
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        return redirect('/myaccount/'+str(id))
