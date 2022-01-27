from multiprocessing import context
import re
from django.http import request
from django.shortcuts import redirect, render
from .forms import LoginForm, UserForm
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
            logged_user = Usuario.objects.filter(email=loginEmail)[0]

            if bcrypt.checkpw(formPassword.encode(), logged_user.password.encode()):
                print('password is correct')
                request.session['user_id'] = logged_user.id
                request.session['name'] = logged_user.first_name
                return redirect('/')
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
        errors = Usuario.objects.basic_validator(request.POST)
        if len(errors) > 0:
            print('errors exist')
        # si el diccionario de errores contiene algo, recorra cada par clave-valor y cree un mensaje flash
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')
        else:
            user_exist = Usuario.objects.filter(email=request.POST['email'])
            print(user_exist)
            if not user_exist:     
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                email = request.POST['email']
                number_phone = request.POST['number_phone']
                password = request.POST['password']
                pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                logged_user = Usuario.objects.create(first_name=first_name, last_name=last_name, email=email, number_phone = number_phone, password=pw_hash)
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
                return redirect('/')
            else: 
                messages.error(request, 'Email is already being used')
                return redirect('/login')
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
        row=[]
        precio = Precio.objects.filter(producto = producto)
        for i in precio:
            print(i, "Este es el i")
            row.append(i)
        context={
            "producto":producto,
            "row":row,
            "range":range(1,5),
        }

    elif nombre == "corazon":
        producto= Producto.objects.get(id=2)
        print(producto)
        row=[]
        precio = Precio.objects.filter(producto = producto)
        for i in precio:
            print(i, "Este es el i")
            row.append(i)
        context={
            "producto":producto,
            "row":row,
            "range":range(1,5),
        }
    
    elif nombre == "bandeja":
        producto= Producto.objects.get(id=3)
        print(producto)
        row=[]
        precio = Precio.objects.filter(producto = producto)
        for i in precio:
            print(i, "Este es el i")
            row.append(i)
        context={
            "producto":producto,
            "row":row,
            "range":range(1,5),
        }

    elif nombre == "basico":
        producto= Producto.objects.get(id=4)
        print(producto)
        row=[]
        precio = Precio.objects.filter(producto = producto)
        for i in precio:
            print(i, "Este es el i")
            row.append(i)
        context={
            "producto":producto,
            "row":row,
            "range":range(1,5),
        }
    print (nombre)
    
    return render(request, 'producto.html',context)

def addtocart(request):
    u = Usuario.objects.get(id = request.session['user_id']) 
    print ("funcion de addtocart")
    pedido = request.POST["pedido"]
    print(pedido)
    p=Producto.objects.filter(nombre = pedido)
    print("encontrado")
    print(p)
    notOrden = Orden.objects.filter(usuario = u, finalizado = False)
    if notOrden:
        print("entra al condiconal notorden")
        messages.info(request,"Por favor termina tu pedido pendiente")
        return redirect("/carrito")
    
    print("no entro al condicional notorden")
    
    tamañoproducto = request.POST["tamañoproducto"]

    rosaadicional = request.POST["rosaadicional"]
    print(rosaadicional)
    rosaadicional = int(rosaadicional)
    if rosaadicional >=0:
        adicional = Adicional.objects.filter(nombre = "Rosas")
        print(adicional)
        rosas_adicional = AdicionalOrden.objects.create(nombre_adicional = adicional[0], cantidad = rosaadicional )
        print(rosas_adicional.cantidad, 'rosas adicionales')
    
    
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
    print(p[0].nombre,u, tamañoproducto,rosas_adicional.cantidad,globo_adicional.nombre_adicional.nombre,especificaciones,entrega, ciudad)
    Orden.objects.create(producto = p[0], usuario = u ,tamañoproducto = tamañoproducto, rosaadicional = rosas_adicional, globoadicional = globo_adicional, especificaciones = especificaciones, entrega = entrega, ciudad = ciudad)
    # print(pedido)
    # print(request.POST)
    return redirect('/carrito')

def carrito(request):
    u = Usuario.objects.get(id = request.session['user_id']) 
    orden = Orden.objects.filter(usuario = u, finalizado = False)
    # print(orden[0].tamañoproducto)
    
    if orden :
        precio = Precio.objects.filter(producto =orden[0].producto, tamaño = orden[0].tamañoproducto)
        print(orden[0].rosaadicional)
        ra = orden[0].rosaadicional
        cantidad = int(ra.cantidad)
        p = float(ra.nombre_adicional.precio)
        print(ra, "RA")
        print(cantidad, "cantidad")
        print(p,"precio")
        p_total = p * cantidad
        print(p_total)
        ga = orden[0].globoadicional
        pg = float(ga.nombre_adicional.precio)
        total = p_total + pg + float(precio[0].precio)
        print(total)
        print(precio[0].precio, "este es el precio") 

        context = {
        "orden":orden[0],
        "precio":precio[0],
        "total_rosas":p_total,
        "total":total,
        }    

        return render(request,'carrito.html', context)
    else:
        print("No hay productos seleccionados")
        return render(request, 'carrito.html')

    return redirect ("/")

def finalizarOrden(request):
    ordenF_id = request.POST["orden-final"] 
    ordenF = Orden.objects.filter(id=ordenF_id)[0]
    ordenF.finalizado = True
    ordenF.save()
    return render(request, 'OrdenFinalizada.html')

def eliminarOrden(request):
    Eorden_id = request.POST["eliminar-orden"] 
    Eorden = Orden.objects.get(id=Eorden_id)
    Eorden.delete()
    return redirect('/')