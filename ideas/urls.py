from django.urls import path
from .views import categories, ideas, implementations, accounts

app_name = 'ideas'
urlpatterns = [
    path('', categories.ListCategoriesView.as_view(), name='index'),
    path('categories/<int:pk>', categories.ShowCategoryView.as_view(), name='category'),

    path('ideas/<int:pk>', ideas.ShowIdeaView.as_view(), name='idea'),
    path('ideas/<int:pk>/validate', ideas.ValidateIdea.as_view(), name='idea_queue'),
    path('ideas/new', ideas.NewIdeaView.as_view(), name='idea_new'),
    path('ideas/queue', ideas.PendingIdeaQueueView.as_view(), name='idea_queue'),

    path('implementations/<int:pk>', implementations.ShowImplementationView.as_view(), name='implementation'),
    path('implementations/new', implementations.NewImplementationView.as_view(), name='implementation_new'),

    path('signup', accounts.SignupView.as_view(), name='signup')
]
