from django.db.models import Max, F
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from board.models import Board
from user.models import User


def list(request, page_no=1, kwd=''):

    # 페이징적용
    page_unit = 5
    count = Board.objects.filter(title__contains=kwd).count()
    page_count = count//page_unit
    if count % page_unit > 0:
        page_count = page_count + 1
    if page_no > page_count or page_no < 1:
        return HttpResponseRedirect("/")

    rpage_count = page_count - page_no

    limit = page_no * page_unit
    offset = limit-5
    board = Board.objects.filter(title__contains=kwd).order_by('-groupno', 'orderno')[offset:limit]
    data = {
        'board': board,
        'page_count': page_count,
        'rpage_count': rpage_count,
        'page_no': page_no,
        'kwd': kwd
    }
    return render(request, 'board/list.html', data)


def write(request):
    result = auth(request)

    if result == True:
        return HttpResponseRedirect("/")

    if request.method == 'GET':
        return render(request, 'board/write.html')

    else:
        board = Board()
        board.title = request.POST['title']
        board.content = request.POST['content']
        board.hit = 0
        groupno = Board.objects.aggregate(max_groupno=Max('groupno')+1)

        if groupno['max_groupno'] is None:
            groupno['max_groupno'] = 1
        board.groupno = groupno['max_groupno']
        board.orderno = 1
        board.depth = 0
        board.user_id = request.session['authuser']['id']
        board.save()
        return HttpResponseRedirect('/board/list/')


def view(request, id):

    board = Board.objects.get(id=id)
    data = {
        'board': board
    }
    board.hit = board.hit + 1
    board.save()
    return render(request, 'board/view.html', data)


def update(request, id):
    result = auth(request)

    if result == True:
        return HttpResponseRedirect("/")

    if request.method == 'GET':
        writer_id = Board.objects.get(id=id)
        if writer_id.user.id == request.session['authuser']['id']:
            board = Board.objects.get(id=id)
            data = {
                'board': board
            }
            return render(request, 'board/modify.html', data)
        else:
            return HttpResponseRedirect("/")

    else:
        board = {
            'title': request.POST['title'],
            'content': request.POST['content']
        }

        Board.objects.filter(id=id).update(**board)
        return HttpResponseRedirect('/board/view/'+str(id))


def delete(request, id):
    result = auth(request)

    if result == True:
        return HttpResponseRedirect("/")

    writer_id = Board.objects.get(id=id)
    if writer_id.user.id == request.session['authuser']['id']:
        Board.objects.filter(id=id).delete()

    return HttpResponseRedirect('/board/list/')


def reply(request, id):
    result = auth(request)

    if result == True:
        return HttpResponseRedirect("/")

    if request.method == 'GET':
        data = {
            'id': id
        }
        return render(request, 'board/replyform.html', data)

    else:
        board = Board()
        board.title = request.POST['title']
        board.content = request.POST['content']
        board.hit = 0
        parent_board = Board.objects.get(id=id)
        board.groupno = parent_board.groupno
        board.orderno = parent_board.orderno + 1
        board.depth = parent_board.depth + 1
        board.user_id = request.session['authuser']['id']
        Board.objects.filter(groupno=board.groupno).filter(orderno__gte=board.orderno).update(orderno=F('orderno')+1)
        board.save()
        return HttpResponseRedirect('/board/list/')


def search(request):

    kwd = request.POST['kwd']
    list = Board.objects.filter(title__contains=kwd)

    return HttpResponseRedirect('/board/list/1/'+kwd)


def auth(request):
    if not request.session._session:
        return True