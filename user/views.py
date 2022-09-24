from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.utils import translation
import uuid
from django.conf import settings
from django.core.mail import send_mail
from home.models import FAQ
from order.models import Order, OrderProduct
from product.models import Category, Comment
from user.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from user.models import UserProfile
from django.contrib.auth.models import User

@login_required(login_url='/login') # Check login
def index(request):
    #category = Category.objects.all()
    current_user = request.user  # Access User Session information
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {#'category': category,
               'profile':profile}
    return render(request,'user_profile.html',context)

def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        user_obj = User.objects.filter(username = username).first()
        profile_obj = UserProfile.objects.filter(user = user_obj ).first()
        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return HttpResponseRedirect('/login')
        else:
            if user is not None:
                login(request, user)
                current_user =request.user
                userprofile=UserProfile.objects.get(user_id=current_user.id)
                request.session['userimage'] = userprofile.image.url
                #*** Multi Langugae
                request.session[translation.LANGUAGE_SESSION_KEY] = userprofile.language.code
                request.session['currency'] = userprofile.currency.code
                translation.activate(userprofile.language.code)

                # Redirect to a success page.
                return HttpResponseRedirect('/'+userprofile.language.code)
            else:
                messages.warning(request,"Login Error !! Username or Password is incorrect")
                return HttpResponseRedirect('/login')
    # Return an 'invalid login' error message.

    #category = Category.objects.all()
    context = {#'category': category
     }
    return render(request, 'login_form.html',context)

def logout_func(request):
    logout(request)
    if translation.LANGUAGE_SESSION_KEY in request.session:
        del request.session[translation.LANGUAGE_SESSION_KEY]
        del request.session['currency']
    return HttpResponseRedirect('/')


def signup_form(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get("email")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            

            try:
                if User.objects.filter(username = username).first():
                    messages.success(request, 'Username is taken.')
                    return HttpResponseRedirect('/signup')

                if User.objects.filter(email = email).first():
                    messages.success(request, 'Email is taken.')
                    return HttpResponseRedirect('/signup')

                auth_token = str(uuid.uuid4())
                send_mail_after_registration(email , auth_token)             
                user_obj = User(username = username , email = email, first_name=first_name, last_name=last_name)
                user_obj.set_password(password)
                user_obj.save()
                
                   
                profile_obj = UserProfile.objects.create(user = user_obj , auth_token = auth_token)
                profile_obj.save()
                
                messages.success(request, 'Mail has been sent for confirmation!')
                messages.success(request, 'Please check Spam Section of Mail as well!')
                
                
                return HttpResponseRedirect('/')
                

            except Exception as e:
                print(e)
           
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect('/signup')


    form = SignUpForm()
    #category = Category.objects.all()
    context = {#'category': category,
               'form': form,
               }
    return render(request, 'signup_form.html', context)




@login_required(login_url='/login') # Check login
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user) # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile) #"userprofile" model -> OneToOneField relatinon with user
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)

@login_required(login_url='/login') # Check login
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>'+ str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        #category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'user_password.html', {'form': form,#'category': category
                       })

@login_required(login_url='/login') # Check login
def user_orders(request):
    #category = Category.objects.all()
    current_user = request.user
    orders=Order.objects.filter(user_id=current_user.id)
    context = {#'category': category,
               'orders': orders,
               }
    return render(request, 'user_orders.html', context)

@login_required(login_url='/login') # Check login
def user_orderdetail(request,id):
    #category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id=id)
    context = {
        #'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)

@login_required(login_url='/login') # Check login
def user_order_product(request):
    #category = Category.objects.all()
    current_user = request.user
    order_product = OrderProduct.objects.filter(user_id=current_user.id).order_by('-id')
    context = {#'category': category,
               'order_product': order_product,
               }
    return render(request, 'user_order_products.html', context)

@login_required(login_url='/login') # Check login
def user_order_product_detail(request,id,oid):
    #category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=oid)
    orderitems = OrderProduct.objects.filter(id=id,user_id=current_user.id)
    context = {
        #'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)


def user_comments(request):
    #category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        #'category': category,
        'comments': comments,
    }
    return render(request, 'user_comments.html', context)

@login_required(login_url='/login') # Check login
def user_deletecomment(request,id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Comment deleted..')
    return HttpResponseRedirect('/user/comments')

def user_verify(request , auth_token):
    try:
        profile_obj = UserProfile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return HttpResponseRedirect('/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return HttpResponseRedirect('/login')
        else:
            messages.success(request, 'Please Contact Support. Your verification code doesn`t match.')
            return HttpResponseRedirect('/')
    except Exception as e:
        print(e)
        return HttpResponseRedirect('/')


def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )