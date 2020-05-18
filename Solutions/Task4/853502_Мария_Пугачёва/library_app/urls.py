from django.urls import path
from library_app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('books/', views.BooksView.as_view(), name='books'),
    path('books/<int:id>/', views.BookDetail.as_view(), name='book-detail'),
    path('visitors/', views.VisitorsView.as_view(), name='visitors'),
    path('visitors/<int:id>/', views.VisitorDetail.as_view(), name='visitor-detail'),
    path('registrations/', views.RegistrationsView.as_view(), name='registrations'),
    path('registrations/add/', views.RegistrationCreate.as_view(), name='registration-add'),
    path('registrations/del/<int:id>/', views.RegistrationDelete.as_view(), name='registration-del'),
    path('registrations/upd/<int:id>/', views.RegistrationUpdate.as_view(), name='registration-upd'),
    path('registrations/<int:id>/', views.RegistrationDetail.as_view(), name='registration-detail'),
]
