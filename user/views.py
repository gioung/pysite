from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from user.models import User


def join(request):
    if request.method == 'GET':
        return render(request, 'user/joinform.html')

    else:
        user = User()
        user.name = request.POST['name']
        user.email = request.POST['email']
        user.password = request.POST['password']
        user.gender = request.POST['gender']
        user.save()
        return render(request, 'user/joinsuccess.html')


def login(request):
    if request.method == 'GET':
        return render(request, 'user/loginform.html')

    else:
        results = User.objects.filter(email=request.POST['email']).filter(password=request.POST['password'])

        # 로그인 실패
        if len(results) == 0:
            return HttpResponseRedirect('/user/login?result=fail')

        # 로그인 처리
        authuser = results[0]
        request.session['authuser'] = model_to_dict(authuser)

        return HttpResponseRedirect('/')


def logout(request):
    del request.session['authuser']
    return HttpResponseRedirect('/')


def update(request):
    result = auth(request)

    if result == True:
        return HttpResponseRedirect("/")

    if request.method == 'GET':
        user = User.objects.get(id=request.session['authuser']['id'])
        data = {
            'user': user
        }
        return render(request, 'user/updateform.html', data)

    else:
        user = User.objects.get(id=request.session['authuser']['id'])
        user.name = request.POST['name']
        user.gender = request.POST['gender']
        if request.POST['password'] is not '':
            user.password = request.POST['password']
        user.save()
        request.session['authuser']['name'] = user.name

        return HttpResponseRedirect('/user/update?result=success')


def checkemail(request):
    email = request.GET['email']
    try:
        user = User.objects.get(email=email)
    except Exception as e:
        user = None

    result = {
        'result': 'success',
        'data': "not exist" if user is None else "exist"
    }
    return JsonResponse(result)


def auth(request):
    if not request.session._session:
        return True