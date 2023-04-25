from django.urls import path
from . import views

app_name = 'ideas'
urlpatterns = [
    path('', views.list_categories, name='index'),
    path('/category/<int:category_id>', views.show_category, name='category'),
    path('/idea/<int:idea_id>', views.show_idea, name='idea'),
]
