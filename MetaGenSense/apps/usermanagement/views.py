from django.http import HttpResponseRedirect
from django.shortcuts import render

from forms import UserCreateForm


def create_account(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/success/')
    else:
        form = UserCreateForm()
    return render(request,'create.html',{'form':form})

