from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect

from ideas.helpers.user import auto_approve
from ideas.models import Category, Idea
from . import validated_filter


class ShowIdeaView(generic.DetailView):
    model = Idea
    template_name = "ideas/show.html"

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)  # This populates 'idea'
        # TODO show reports associated?
        kwargs['implementations'] = self.implementations_for_idea(kwargs['idea'])
        return kwargs

    def implementations_for_idea(self, idea: Idea):
        user = self.request.user
        return validated_filter(idea.implementation_set, user).prefetch_related('author')


# TODO perms.idea_new
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
        # TODO is_valid(): make sure user has no idea in that category pending
        form.instance.category = self.category
        form.instance.author = self.request.user
        form.instance.validated = self.auto_approve()
        return super().form_valid(form)

    def get_success_url(self):
        if self.auto_approve():
            return reverse_lazy('ideas:idea', kwargs={'pk': self.object.id})
        else:
            return reverse_lazy('ideas:category', kwargs={'pk': self.category.id})

    def auto_approve(self):
        return auto_approve(self.request.user)


class RecentIdeasView(generic.ListView):
    model = Idea
    template_name = "ideas/recent.html"
    context_object_name = "ideas"

    ordering = [("approved", "ASC")]  # TODO


class PendingIdeaQueueView(generic.ListView, PermissionRequiredMixin):
    model = Idea
    template_name = "ideas/queue.html"
    context_object_name = "ideas"

    permission_required = "validate_idea"

    def get_queryset(self):
        return self.get_queryset().filter(validated=False).prefetch_related('author')


class ValidateIdea(generic.View, PermissionRequiredMixin):
    permission_required = "validate_idea"

    def get(self, request, *args, **kwargs):
        # TODO handle async submit, just return OK/NOT OK
        idea_id = kwargs['pk']
        idea = get_object_or_404(Idea, pk=idea_id)
        idea.validated = True
        idea.save()
        return HttpResponseRedirect(reverse_lazy("ideas:idea", kwargs={'pk': idea_id}))
