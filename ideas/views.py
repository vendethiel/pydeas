from django.views import generic
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .helpers.user import auto_approve, can_see_unvalidated
from .models import Category, Idea


def validated_filter(qs, user):
    if can_see_unvalidated(user):
        return qs.all()
    else:
        return qs.filter(validated=True)


class ListCategoriesView(generic.ListView):
    model = Category
    template_name = "categories/index.html"
    context_object_name = "categories"


class ShowCategoryView(generic.DetailView):
    model = Category
    template_name = "categories/show.html"

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs) # This populates 'category'
        kwargs['ideas'] = self.validated_filter(kwargs['category'].idea_set)
        return kwargs

    def validated_filter(self, qs):
        return validated_filter(qs, self.request.user)


class ShowIdeaView(generic.DetailView):
    model = Idea
    template_name = "ideas/show.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class NewIdeaView(generic.CreateView, LoginRequiredMixin):
    template_name = "ideas/new.html"
    model = Idea
    fields = ("name", "description")

    def dispatch(self, request, *args, **kwargs):
        category_id = request.GET['category_id']
        self.category = get_object_or_404(Category, pk=category_id)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['category'] = self.category
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.category = self.category
        form.instance.validated = self.auto_approve()
        return super().form_valid(form)

    def get_success_url(self):
        category_id = self.category.id
        if self.auto_approve():
            return reverse_lazy('ideas:idea', kwargs={'category_id': category_id, 'pk': self.object.id})
        else:
            return reverse_lazy('ideas:category', kwargs={'category_id': category_id})

    def auto_approve(self):
        return auto_approve(self.request.user)


class PendingIdeaQueueView(generic.ListView, PermissionRequiredMixin):
    permission_required = "see_queue"


class SignupView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"
