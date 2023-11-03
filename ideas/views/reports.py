from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import generic

from models import Report, Idea, Implementation


class ListReportView(generic.ListView, PermissionRequiredMixin):
    model = Report
    template_name = "report/index.html"

    permission_required = "see_report"

    # TODO query associated object

    def get_queryset(self):
        # Only show unresolved reports
        return self.get_queryset().filter(resolved_by=None)


class ShowReportView(generic.DetailView, PermissionRequiredMixin):
    model = Report
    template_name = "report/show.html"

    permission_required = "see_report"


class ActionReportView(generic.View, PermissionRequiredMixin):
    permission_required = "action_report"

    def post(self, request, *args, **kwargs):
        # TODO kwargs? really?
        object_model_name = kwargs['object_model_name']
        if not Report.is_reportable(object_model_name):
            pass # TODO error
        object_id = kwargs['object_id']
        report = Report.objects.filter(object_model_name=object_model_name, object_id=object_id).first()
        if report.resolved_by is not None:
            pass # TODO error
        report.resolved_by = request.user
        report.resolved_at = datetime.now()

        # TODO ?
        # except queryset.model.DoesNotExist:
        # raise Http404(
        #     "No report matches the given query."
        # )



class NewReportView(generic.CreateView, LoginRequiredMixin):
    model = Report
    template_name = "report/new.html"
    fields = ("model_id", "comment")
    object_model = None
    object_model_name = None

    def dispatch(self, request, *args, **kwargs):
        object_id = request.GET['object_id']
        self.object = get_object_or_404(self.object_model, pk=object_id)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['object'] = self.object
        kwargs['model_name'] = self.object_model_name
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        # TODO is_valid(): make sure user has no report of that idea/impl pending
        form.instance.author = self.request.user
        form.instance.model_name = self.object_model_name
        return super().form_valid(form)


class NewIdeaReportView(NewReportView):
    object_model = Idea
    object_model_name = 'idea'


class NewImplementationReportView(NewReportView):
    object_model = Implementation
    object_model_name = 'idea'
