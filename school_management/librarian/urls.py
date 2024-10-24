from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'librarian'
urlpatterns = [
    path('book-create/',views.BookCreateView.as_view(),name="BookCreateView"),
    path('book-list/',views.BookListView.as_view(),name="BookListView"),
    path('books/<int:pk>/delete/',views.BookDeleteView.as_view(),name="BookDeleteView"),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='BookUpdateView'),
    path('books/search/', views.BookSearchAutocompleteView.as_view(), name='BookSearchAutocompleteView'),  
    path('library-record-create/',views.LibraryRecordCreateView.as_view(),name="LibraryRecordCreateView"),
    path('library-record-list/',views.LibraryRecordListView.as_view(),name="LibraryRecordListView"),
    path('get_division/',views.get_division,name="get_division"),
    path('get_student/',views.get_student,name="get_student"),
    path('library-record-autocomplete/',views.LibraryRecordSearchAutocompleteView.as_view(),name="LibraryRecordSearchAutocompleteView"),
    path('library-record-delete/<int:pk>/',views.LibraryRecordDeleteView.as_view(),name="LibraryRecordDeleteView"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)