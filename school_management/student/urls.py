from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'student'
urlpatterns = [
    path('student-create/',views.StudentCreateView.as_view(),name="StudentCreateView"),
    path('student-list/',views.StudentListView.as_view(),name="StudentListView"),
    path('student-update/<int:pk>/',views.StudentUpdateView.as_view(),name="StudentUpdateView"),
    path('student-delete/<int:pk>/',views.StudentDeleteView.as_view(),name="StudentDeleteView"),
    path('fee-create/',views.FeeCreateView.as_view(),name="FeeCreateView"),
    path('fee-list/',views.FeeDetailsListView.as_view(),name="FeeDetailsListView"),
    path('fee-update/<int:pk>/',views.FeeDetailsUpdateView.as_view(),name="FeeDetailsUpdateView"),
    path('fees-history/',views.FeeHistoryListView.as_view(),name="FeeHistoryListView"),
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)