from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import generic

from ideas.models import Report, Idea, Implementation


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
    template_name = "reports/show.html"

    permission_required = "see_report"


class ActionReportView(generic.View, PermissionRequiredMixin):
    permission_required = "action_report"

    def post(self, request, *args, **kwargs):
        # TODO kwargs? really?
        object_model_name = kwargs['object_model_name']
        if not Report.is_reportable(object_model_name):
            pass  # TODO error
        object_id = kwargs['object_id']
        report = Report.objects.filter(object_model_name=object_model_name, object_id=object_id).first()
        if report.resolved_by is not None:
            pass  # TODO error
        report.resolved_by = request.user
        report.resolved_at = datetime.now()

        # TODO ?
        # except queryset.model.DoesNotExist:
        # raise Http404(
        #     "No report matches the given query."
        # )


class NewReportView(generic.CreateView, LoginRequiredMixin):
    model = Report
    template_name = "reports/new.html"
    fields = ("comment",)
    object_model = None
    object_model_name = None

    def dispatch(self, request, *args, **kwargs):
        pk = request.GET['pk']
        self.instance = get_object_or_404(self.object_model, pk=pk)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        print(self.instance)
        kwargs['instance'] = self.instance
        kwargs['model_name'] = self.object_model_name
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        if not self._can_be_reported():
            return super().form_invalid(form)

        form.instance.reporter = self.request.user
        form.instance.model_id = self.instance.id
        form.instance.model_name = self.object_model_name
        return super().form_valid(form)

    # XXX should this be an override on the Form object itself?
    def _can_be_reported(self):
        report = Report.report(self.object_model_name, self.instance.id)
        if report is None:
            return True
        # Already reported this instance (whether closed or not)
        return report.reporter is not self.request.user


class NewIdeaReportView(NewReportView):
    object_model = Idea
    object_model_name = 'idea'


class NewImplementationReportView(NewReportView):
    object_model = Implementation
    object_model_name = 'implementation'
