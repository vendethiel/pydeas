from django.shortcuts import render, get_object_or_404
from .models import Category, Idea


def list_categories(request):
    categories = Category.objects.all()
    return render(request, "categories/index.html", {"categories": categories})


def show_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    return render(request, "categories/show.html", {"category": category})


def show_idea(request, idea_id):
    idea = get_object_or_404(Idea, pk=idea_id)
    return render(request, "ideas/show.html", {"idea": idea})