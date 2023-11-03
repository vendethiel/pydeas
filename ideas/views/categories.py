from django.views import generic
from ideas.models import Category
from . import validated_filter


class ListCategoriesView(generic.ListView):
    model = Category
    template_name = "categories/index.html"
    context_object_name = "categories"


class ShowCategoryView(generic.DetailView):
    model = Category
    template_name = "categories/show.html"

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)  # This populates 'category'
        kwargs['ideas'] = self.ideas_for_category(kwargs['category'])
        return kwargs

    def ideas_for_category(self, category: Category):
        user = self.request.user
        return validated_filter(category.idea_set, user).prefetch_related('author')
