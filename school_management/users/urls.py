from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'users'
urlpatterns = [
    path('admin-home/',views.HomeView.as_view(),name="HomeView"),
    path('login/',views.LoginView.as_view(),name="LoginView"),
    path('logout/',views.LogoutView.as_view(),name="LogoutView"),
    path('password-change/',views.UserChangePasswordView.as_view(),name="UserChangePasswordView"),
    path('admin-profile-edit/<int:pk>/',views.AdminProfileUpdateView.as_view(),name="AdminProfileUpdateView"),
    path('staff-profile-edit/<int:pk>/',views.StaffProfileUpdateView.as_view(),name="StaffProfileUpdateView"),
    path('admin-login/',views.AdminLoginView.as_view(),name="AdminLoginView"),
    path('staff-login/',views.StaffLoginView.as_view(),name="StaffLoginView"),
    path('librarian-login/',views.LibrarianLoginView.as_view(),name="LibrarianLoginView"),
    path('',views.IndexView.as_view(),name="IndexView"),
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)