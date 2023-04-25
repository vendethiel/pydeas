from django.urls import path
from . import views

app_name = 'ideas'
urlpatterns = [
    path('', views.ListCategoriesView.as_view(), name='index'),
    path('/category/<int:pk>', views.ShowCategoryView.as_view(), name='category'),
    path('/idea/<int:pk>', views.ShowIdeaView.as_view(), name='idea'),
]
