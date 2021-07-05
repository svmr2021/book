from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('person/list/', PersonListView.as_view()),
    path('person/staff/list/', StaffListView.as_view()),
    path('person/reader/list/', ReaderListView.as_view()),
    path('person/create/', PersonCreateView.as_view()),
    path('person/update/<int:pk>', PersonUpdateView.as_view()),
    path('registrate/', UserRegisterView.as_view()),
    path('users/', UserListView.as_view()),
    path('book/list/', BookListView.as_view()),
    path('book/detail/<int:pk>', BookDetailView.as_view()),
    path('book/create/', BookCreateView.as_view()),
    path('book/update/<int:pk>/', BookUpdateView.as_view()),
    path('book/delete/<int:pk>/', BookDeleteView.as_view()),
    path('comment/create/', CommentCreateView.as_view()),
    path('comment/update/<int:pk>/', CommentUpdateView.as_view()),
    path('like/create/', LikeCreateView.as_view()),
    path('like/delete/<int:pk>', LikeDeleteView.as_view()),
    path('category/list/', CategoryListView.as_view()),
]
