from django.urls import path
from .views import comment_list, add_comment,upload_file_view

urlpatterns = [
    path('', comment_list, name='comment_list'),
    path('add/', add_comment, name='add_comment'),
    path('add/<int:parent_comment_id>/', add_comment, name='add_reply'),
    path('upload/', upload_file_view, name='upload_file'),
]
