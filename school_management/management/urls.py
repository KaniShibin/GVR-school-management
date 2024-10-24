from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'management'
urlpatterns = [
    path('admin-create/',views.AdminCreateView.as_view(),name="AdminCreateView"),
    path('admin-delete/<int:pk>/',views.AdminDeleteView.as_view(),name="AdminDeleteView"),
    path('admin-list/',views.AdminListView.as_view(),name="AdminListView"),
    path('admin-update/<int:pk>/',views.AdminUpdateView.as_view(),name="AdminUpdateView"),   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)