from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from ideas.helpers.user import auto_approve
from ideas.models import Idea, Implementation


class ShowImplementationView(generic.DetailView):
    model = Implementation
    template_name = "implementations/show.html"


# TODO perms.implementation_new
class NewImplementationView(generic.CreateView, LoginRequiredMixin):
    template_name = "implementations/new.html"
    model = Implementation
    fields = ("repo_url", "demo_url")  # TODO name/comment?

    def dispatch(self, request, *args, **kwargs):
        idea_id = request.GET['idea_id']
        self.idea = get_object_or_404(Idea, pk=idea_id)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['idea'] = self.idea
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # TODO is_valid(): make sure user has no impl in that idea pending
        form.instance.idea = self.idea
        form.instance.author = self.request.user
        form.instance.validated = self.auto_approve()
        return super().form_valid(form)

    def get_success_url(self):
        if self.auto_approve():
            return reverse_lazy('ideas:implementation', kwargs={'pk': self.object.id})
        else:
            return reverse_lazy('ideas:idea', kwargs={'pk': self.idea.id})

    def auto_approve(self):
        return auto_approve(self.request.user)