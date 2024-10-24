from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'staff'
urlpatterns = [
    path('staff-list/',views.StaffListView.as_view(),name="StaffListView"),
    path('staff-create/',views.StaffCreateView.as_view(),name="StaffCreateView"),
    path('staff-update/<int:pk>/',views.StaffUpdateView.as_view(),name="StaffUpdateView"),
    path('staff-delete/<int:pk>/',views.StaffDeleteView.as_view(),name="StaffDeleteView"),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)