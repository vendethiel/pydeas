from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    class Meta:
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Idea(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    validated = models.BooleanField()

    def __str__(self):
        return self.name


class Implementation(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    repo_url = models.CharField(max_length=200)
    demo_url = models.CharField(max_length=200)
    # TODO more info, like notes/comment/language maybe?
    validated = models.BooleanField()

    def __str__(self):
        return f"{self.author.username}'s {self.idea.name}"


class Report(models.Model):
    model_name = models.CharField(max_length=200)
    model_id = models.IntegerField() # Cannot make it a FK because of polymorphism
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")
    comment = models.TextField()
    resolved_at = models.DateTimeField(null=True)
    resolved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="resolved_reports")

    # TODO validate model_name
    # TODO composite PK (model_name, model_id)

    @staticmethod
    def is_reportable(name):
        return name == 'idea' or name == 'implementation'

    @staticmethod
    def idea_report(idea_id):
        return Report.report('idea', idea_id)

    @staticmethod
    def implementation_report(implementation_id):
        return Report.report('implementation', implementation_id)

    @staticmethod
    def report(model_name, model_id):
        return Report.objects.filter(model_name=model_name, model_id=model_id).first()

    def is_resolved(self):
        return self.resolved_by is not None

    def __str__(self):
        return f"Report on {self.model_name} #{self.model_id} by {self.reporter.username}"

# TODO comments (with rating?)
# TODO screenshots
