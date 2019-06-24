from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from guestbook.models import Guestbook


def list(request):
    guestbook = Guestbook.objects.all().order_by('-id')
    data = {
        'guestbook': guestbook
    }

    return render(request, 'guestbook/list.html', data)



def add(request):
    result = auth(request)

    if result == True:
        return HttpResponseRedirect("/")

    guestbook = Guestbook()
    guestbook.name = request.POST['name']
    guestbook.password = request.POST['password']
    guestbook.contents = request.POST['contents']
    guestbook.save()
    return HttpResponseRedirect('/guestbook/list')


def deleteform(request, id=0):
    result = auth(request)

    if result == True:
        return HttpResponseRedirect("/")

    data = {'id': id}
    return render(request, 'guestbook/deleteform.html', data)


def delete(request, id=0):
    result = auth(request)

    if result == True:
        return HttpResponseRedirect("/")

    password = request.POST['password']
    guestbook = Guestbook.objects.filter(id=id).filter(password=password)
    guestbook.delete()
    return HttpResponseRedirect('/guestbook/list')


def auth(request):
    if not request.session._session:
        return True