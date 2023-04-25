from django.views import generic
from .models import Category, Idea


class ListCategoriesView(generic.ListView):
    model = Category
    template_name = "categories/index.html"
    context_object_name = "categories"


class ShowCategoryView(generic.DetailView):
    model = Category
    template_name = "categories/show.html"


class ShowIdeaView(generic.DetailView):
    model = Idea
    template_name = "ideas/show.html"