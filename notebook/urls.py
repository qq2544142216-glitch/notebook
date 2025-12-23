from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

def redirect_to_notes(request):
    return redirect('note_list')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_notes, name='home'),
    path('notes/', include('notes.urls')),
    path('accounts/', include('accounts.urls')),
    # 修复退出URL - 使用GET方法
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]