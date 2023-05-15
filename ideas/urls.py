from django.urls import path
from . import views

app_name = 'ideas'
urlpatterns = [
    path('', views.ListCategoriesView.as_view(), name='index'),
    path('categories/<int:pk>', views.ShowCategoryView.as_view(), name='category'),
    path('ideas/<int:pk>', views.ShowIdeaView.as_view(), name='idea'),
    path('ideas/new', views.NewIdeaView.as_view(), name='idea_new'),
    path('implementations/<int:pk>', views.ShowImplementationView.as_view(), name='implementation'),
    path('implementations/new', views.NewImplementationView.as_view(), name='implementation_new')
]
