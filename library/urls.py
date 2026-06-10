from django.urls import path


from library.views import book_list_create
from library.class_views import (
    BookListCreateAPIView,
    BookRetrieveUpdateDestroyAPIView,
    CategoryListCreateGenericAPIView,
    CategoryRetrieveUpdateDestroyGenericView,
    AuthorListCreateGenericView,
    UserListGenericView,
    BookListGenericView
)

# api/v1/books/
urlpatterns = [
    # path('books/', book_list_create),
    # path('books/', BookListCreateAPIView.as_view()),
    path('books/', BookListGenericView.as_view()),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyAPIView.as_view()),
    path('categories/', CategoryListCreateGenericAPIView.as_view()),
    path('categories/<str:name>/', CategoryRetrieveUpdateDestroyGenericView.as_view()),
    path('authors/', AuthorListCreateGenericView.as_view()),
    path('users/', UserListGenericView.as_view()),
]
