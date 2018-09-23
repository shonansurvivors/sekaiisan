from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from .models import Item


class IndexView(TemplateView):

    template_name = 'toy/index.html'


class ItemListView(ListView):

    model = Item
    queryset = Item.objects.prefetch_related('tag')
