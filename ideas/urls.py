from django.urls import path
from . import views

app_name = 'ideas'
urlpatterns = [
    path('', views.ListCategoriesView.as_view(), name='index'),
    path('categories/<int:pk>', views.ShowCategoryView.as_view(), name='category'),
    path('categories/<int:category_id>/ideas/<int:pk>', views.ShowIdeaView.as_view(), name='idea'),
    path('categories/<int:category_id>/ideas/new', views.NewIdeaView.as_view(), name='idea_new')
]
