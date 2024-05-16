from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
#    path('login/', auth_views.LoginView.as_view(), name='login'),
#    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
#    views.mostrar, name='mostrar'
    path('', include('app01.urls')),
    path('accounts/', include('django.contrib.auth.urls'))
]