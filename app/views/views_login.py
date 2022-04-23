from django.views.generic import View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


class LoginView(View):
    def post(self,request, *args, **kwargs):
        if request.method == "POST":
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.success(request, ('El correo o la contraseña es incorrecta, intenta nuevamente'))
                return redirect('app:login')
        else:
            pass
        context={
        }
        return render(request, 'authenticate/login.html', context)
    
    def get(self,request, *args, **kwargs):
        context={
        }
        #Comprobar si el usuario ya esta logeado
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return render(request, 'authenticate/login.html', context)

        

    def logout_user(request):
        logout(request)
        messages.success(request, ('Se ha cerrado sesión correctamente'))
        return redirect("app:login")
