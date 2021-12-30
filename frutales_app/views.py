import re
from django.http import request
from django.shortcuts import redirect, render
from .forms import LoginForm, UserForm
from .models import User
import bcrypt
from django.contrib import messages
from .models import *

def home (request):
    return render(request, 'home.html')

def homeUser(request):
    return render (request, 'home-user.html')

def logout(request):
    request.session.clear()
    return redirect('/login')

def login(request):
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            formPassword = loginForm['password'].value()
            loginEmail = loginForm['email'].value()
            logged_user = User.objects.filter(email=loginEmail)[0]

            if bcrypt.checkpw(formPassword.encode(), logged_user.password.encode()):
                print('password is correct')
                request.session['user_id'] = logged_user.id
                request.session['name'] = logged_user.first_name
                return redirect('/home-user')
            else:
                print('password is incorrect')
                return redirect('/login')
    else:
        context = {
            # 'userForm': UserForm(),
            'loginForm': LoginForm()
        }
        return render(request, 'login.html', context)


def createUser(request):
    # POST 
    if request.method == 'POST':
        # formResults = UserForm(request.POST)
        # validResults = formResults.is_valid()
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
            print('errors exist')
        # si el diccionario de errores contiene algo, recorra cada par clave-valor y cree un mensaje flash
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/home-user')
        else:
            user_exist = User.objects.filter(email=request.POST['email'])
            print(user_exist)
            if not user_exist:     
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                email = request.POST['email']
                password = request.POST['password']
                pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                logged_user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)
                request.session['user_id'] = logged_user.id
                request.session['name'] = logged_user.first_name
                # User.objects.create(...)
                print('no errors found')
                # registerEmail = formResults['email'].value()
                # user_exist = User.objects.filter(email=registerEmail)
                # print(user_exist)
                # if not user_exist: 
                #     print('not user exist with that email')
                #     logged_user = formResults.save()
                #     request.session['user_id'] = logged_user.id
                # else:
                #     print('user alread exist')
                # return redirect('/register')
                return render(request, 'register.html')
            else: 
                messages.error(request, 'Email is already being used')
                return redirect('/home-user')
        # print(validResults)
        print('form is FALSE')
        # context = {
        #      # 'userForm': formResults,
        #     # 'formErrors': UserForm().errors
        # }
    # return render(request, 'login.html')
    return render(request, 'register.html')

def carrusel(request):
    return render(request,'carrusel.html')

def producto(request,nombre):
    context = {}
    tamaño = "pequeño,mediano,grande"
    tamaño = tamaño.split(',')
    if nombre == "ramos":
        producto= Producto.objects.get(id=1)
        print(producto)
        producto.tamaño=producto.tamaño.split(',')
        producto.precio=producto.precio.split(',')
        row=[]
        for i in range (len(producto.tamaño)):
            row.append({"tamaño":producto.tamaño[i],"precio":producto.precio[i]})
        context={
            "producto":producto,
            "row":row,
        }

    elif nombre == "corazon":
        producto= Producto.objects.get(id=2)
        print(producto)
        producto.tamaño=producto.tamaño.split(',')
        producto.precio=producto.precio.split(',')
        row=[]
        for i in range (len(producto.tamaño)):
            row.append({"tamaño":producto.tamaño[i],"precio":producto.precio[i]})
        context={
            "producto":producto,
            "row":row,
        }
    
    elif nombre == "bandeja":
        producto= Producto.objects.get(id=3)
        print(producto)
        producto.tamaño=producto.tamaño.split(',')
        producto.precio=producto.precio.split(',')
        row=[]
        for i in range (len(producto.tamaño)):
            row.append({"tamaño":producto.tamaño[i],"precio":producto.precio[i]})
        context={
            "producto":producto,
            "row":row,
        }

    elif nombre == "basico":
        producto= Producto.objects.get(id=4)
        print(producto)
        producto.tamaño=producto.tamaño.split(',')
        producto.precio=producto.precio.split(',')
        row=[]
        for i in range (len(producto.tamaño)):
            row.append({"tamaño":producto.tamaño[i],"precio":producto.precio[i]})
        context={
            "producto":producto,
            "row":row,
        }
    print (nombre)
    return render(request, 'producto.html',context)

def addtocart(request):
    pedido = request.POST["pedido"]
    p=Producto.objects.filter(nombre = pedido)
    print("encontrado")
    print(p)
    
    tamañoproducto = request.POST["tamañoproducto"]
    rosaadicional = request.POST["rosaadicional"]
    rosaadicional = int(rosaadicional)
    if rosaadicional >0:
        adicional = Adicional.objects.filter(nombre = "Rosas")
        rosas_adicional = AdicionalOrden.objects.create(nombre_adicional = adicional[0], cantidad = rosaadicional )
    
    
    globoadicional = request.POST["globoadicional"]
   
    if globoadicional == "globopequeño":
        adicional = Adicional.objects.filter(nombre = "Globo pequeño")
        globo_adicional = AdicionalOrden.objects.create(nombre_adicional = adicional[0], cantidad = 1 )
    
    elif globoadicional == "globogrande":
        adicional = Adicional.objects.filter(nombre = "Globo grande")
        globo_adicional = AdicionalOrden.objects.create(nombre_adicional = adicional[0], cantidad = 1 )

    especificaciones = request.POST["especificaciones"]
    entrega = request.POST["entrega"]
    ciudad = request.POST["ciudad"]
    Orden.objects.create(producto = p[0], tamañoproducto = tamañoproducto, rosaadicional = rosas_adicional, globoadicional = globo_adicional, especificaciones = especificaciones, entrega = entrega, ciudad = ciudad)
    # print(pedido)
    # print(request.POST)
    return redirect('/')