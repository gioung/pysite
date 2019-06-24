"""pysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import(handler404, handler500)

import main.views as main_views
import user.views as user_views
import guestbook.views as guestbook_views
import board.views as board_views

handler404 = 'error.views.page_not_found'
handler500 = 'error.views.server_error'

urlpatterns = [
    path('', main_views.index),

    path('user/join/', user_views.join),
    path('user/login/', user_views.login),
    path('user/logout/', user_views.logout),
    path('user/update/', user_views.update),
    path('user/api/checkemail', user_views.checkemail),

    path('guestbook/list/', guestbook_views.list),
    path('guestbook/add/', guestbook_views.add),
    path('guestbook/deleteform/<int:id>', guestbook_views.deleteform),
    path('guestbook/delete/<int:id>', guestbook_views.delete),

    path('board/list/', board_views.list),
    path('board/list/<int:page_no>/', board_views.list),
    path('board/list/<int:page_no>/<str:kwd>', board_views.list),
    path('board/write', board_views.write),
    path('board/view/<int:id>', board_views.view),
    path('board/update/<int:id>', board_views.update),
    path('board/delete/<int:id>', board_views.delete),
    path('board/reply/<int:id>', board_views.reply),
    path('board/search', board_views.search),

    path('admin/', admin.site.urls),
]
