from django.views import generic
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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


class NewIdeaView(generic.CreateView, LoginRequiredMixin):
    template_name = "ideas/new.html"
    model = Idea
    fields = ("name", "description")

    def form_valid(self, form):
        form.instance.category = get_object_or_404(Category, pk=self.kwargs['category_id'])
        form.instance.validated = self.auto_approve()
        return super().form_valid(form)

    def get_success_url(self):
        category_id = self.kwargs['category_id']
        if self.auto_approve():
            return reverse('ideas:idea', category_id, self.object.id)
        else:
            return reverse('ideas:category', category_id)

    def auto_approve(self):
        # TODO move this somewhere else?
        # TODO perm or something?
        return self.request.user.is_staff


class PendingIdeaQueueView(generic.ListView, PermissionRequiredMixin):
    permission_required = "see_queue"


class SignupView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"
