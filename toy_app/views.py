from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.template.response import TemplateResponse
from django.views.generic import TemplateView, ListView, DetailView
from pure_pagination.mixins import PaginationMixin
from .models import Item, Tag


class IndexView(TemplateView):

    template_name = 'toy_app/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['object_list'] = Item.get_items_each_for_tags()
        return context


class ItemDetailView(DetailView):

    template_name = 'toy_app/item_detail.html'
    model = Item


def item_list(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    items = get_list_or_404(Item.objects.all().order_by('-release_date'), tag=tag)
    context = {
        'object_list': items,
        'tag': tag,
    }
    return TemplateResponse(request,
                            'toy_app/item_list.html',
                            context=context,
                            )


'''
class ItemByTagListView(TemplateView):

    template_name = 'toy_app/item_list.html'

    def get_context_data(self, **kwargs):
        tag = Tag.objects.filter(pk=tag_id)
        context = super(ItemByTagListView, self).get_context_data(**kwargs)
        context['object_list'] = Item.objects.prefetch_related('tag').objects.filter(tag=tag)
        return context
'''

'''
    model = Item
    tag = Tag.objects.filter(pk=tag_pk)
    queryset = Item.objects.prefetch_related('tag').objects.filter(tag=tag)
    paginate_by = 10
'''

'''
    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        item_list = Item.objects.prefetch_related('tag')
        context['object_list'] = item_list
        return context
'''