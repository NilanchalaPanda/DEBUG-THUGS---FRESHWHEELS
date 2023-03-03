from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User, Product
from django.views.decorators.csrf import csrf_exempt

def verifyName(name):
    for char in name:
        if (char < 65 or char > 90) and (char < 97 and char > 122):
            return False
    return True

def verifyPassword(password):
    if len(password) != 8:
        return False
    lcount, hcount, dcount, scount = 0, 0, 0, 0
    for char in password:
        if char >= 65 and char <= 90:
            hcount += 1
        elif char >= 97 and char <= 122:
            lcount += 1
        elif char >= 48 and char <= 57:
            dcount += 1
        else:
            scount += 1
    if lcount != 0 and hcount != 0 and scount != 0 and dcount != 0:
        return True
    return False

def verifyEmail(email):
    return email.endswith('@gmail.com' | '@ves.ac.in')

def index(request):
    return render(request, 'login/main_index.html')

def aboutUs(request):
    return HttpResponse("About_US")

def testimonials(request):
    return HttpResponse("Testimonials")

def register(request):
    if request.GET.get('Login_btn') == ('Login'):
        user_email = request.GET.get('emailEditText', None)
        user_password = request.GET.get('passwordEditText', None)

        if user_email is not None and user_password is not None:
            try:
                currentUser = User.objects.get(user_email=user_email)
                if currentUser.get_user_password() == user_password:

                    request.session['data'] = {'id': currentUser.id, 
                                             'type': currentUser.user_type, 
                                             'name': currentUser.user_name, 
                                             'email': currentUser.user_email, 
                                             'address': currentUser.user_address, 
                                             'phone': currentUser.user_phone, 
                                             'password': currentUser.user_password}

                    if currentUser.get_user_type() == "Farmer":
                        return redirect(farmerPage)
                    
                    elif currentUser.get_user_type() == "Customer":
                        return redirect(customerPage)
                    
                    else:
                        return redirect(driverPage)
                    
            except Exception as e:
                print("Try Again", e.__class__.__name__)

    elif request.GET.get('SignUp_btn') == ('SignUp'):
        user_email = request.GET.get('emailEditText', '')
        user_password = request.GET.get('passwordEditText', '')
        confirm_password = request.GET.get('confirmPasswordEditText', '')

        if request.GET.get('users') != (''):
            user_type = request.GET.get('users')
            if user_password == confirm_password:
                try:
                    currentUser = User.objects.get(user_email=user_email)
                except:
                    try:
                        currentUser = User(user_email=user_email, user_password=user_password, user_type=user_type)
                        currentUser.save()

                        print("Saved", currentUser.__str__())

                        request.session['data'] = {'id':currentUser.id, 
                                             'type':currentUser.user_type, 
                                             'email':currentUser.user_email, 
                                             'password':currentUser.user_password}
                        
                        if currentUser.user_type == 'Driver':
                            return driverIndex(request)
                        elif currentUser.user_type == 'Customer':
                            return customerIndex(request)
                        elif currentUser.user_type == 'Farmer':
                            return farmerIndex(request)
                        
                    except Exception as e:
                        print('Try Again', e.__class__.__name__)

    elif request.GET.get('Submit_btn') == 'SubInfo':
        currentUserDets = request.session['data']
        print(currentUserDets)
        user_fname = request.GET.get('fNameEditText', '').strip()
        user_lname = request.GET.get('lNameEditText', '').strip()
        user_name = user_fname + " " + user_lname
        user_address = request.GET.get('addressEditText', '')
        user_phoneNumber = request.GET.get('phoneNumberEditText', '')

        if user_name != '' and user_address != '' and user_phoneNumber != '':
            try:
                currentUserDets.update({'name': user_name, 'address': user_address, 'phone': user_phoneNumber})
                currentUser = User.objects.get(user_email=currentUserDets['email'])
                print(currentUserDets)

                currentUser.user_name = user_name
                currentUser.user_address = user_address
                currentUser.user_phone = user_phoneNumber
                currentUser.save()

                print(currentUser.user_type)
                if currentUser.user_type == "Farmer":
                    return redirect(farmerPage)
                
                elif currentUser.user_type == "Driver":
                    return redirect(driverPage)
                
                else:
                    return redirect(customerPage)
                
            except Exception as e:
                print("Try again", e.__class__.__name__, str(e))

    return render(request, 'login/registration_page.html')

def farmerPage(request):
    return render(request, 'login/farmer.html')

def farmerIndex(request):
    return render(request, 'login/farmer_index.html')

@csrf_exempt
def farmerInventory(request):
    if request.method == 'POST' and request.accepts('json'):
        data = dict(request.POST)
        try:
            index = len(data) - 1
            farmer = User.objects.get(id=request.session['data']['id'])
            product = Product(product_type = data[f'itemJsonArray[{index}][]'][0], product_name = data[f'itemJsonArray[{index}][]'][1], product_description = data[f'itemJsonArray[{index}][]'][2], product_price = data[f'itemJsonArray[{index}][]'][3], product_quantity = data[f'itemJsonArray[{index}][]'][4], product_by = farmer)
            product.save()
            print("Inventory Received")
        except Exception as e:
            print(e.__class__.__name__, str(e))
        return HttpResponse('OK')
    return render(request, 'login/farmer_inventory.html')

def driverPage(request):
    return render(request, 'login/driver.html')

def driverIndex(request):
    return render(request, 'login/driver_index.html')

def customerIndex(request):
    return render(request, 'login/customer_index.html')

def customerPage(request):
    return render(request, 'login/customer.html')

def profilePage(request):
    return render(request, 'login/profile.html')

def cartPage(request):
    return render(request, 'login/cart.html')

def accountPage(request):
    return render(request, 'login/account.html')

def productPage(request):
    params = list(Product.objects.all())
    paramsForHtml = {}
    for index in range(len(params)):
        product = {'Name': params[index].product_name, 'Price': params[index].product_price, 'Type': params[index].product_type}
        paramsForHtml.update({f'Product{index + 1}': product})
    print(paramsForHtml)
    return render(request, 'login/product.html', {'paramsForHtml': paramsForHtml})

def ordersPage(request):
    return render(request, 'login/orders.html')

def requestsPage(request):
    return render(request, 'login/requests.html')