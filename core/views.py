from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin



class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context={

        }
        return render(request, 'index.html', context)