from django.db.models import Count
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import View, ListView
from django.views.generic.edit import FormView

from .models import Article, Heritage, Country, Blog, SiteMaster
from .forms import ContactForm


class AboutUsView(View):
    def get(self, request):

        site_master = SiteMaster.objects.first()

        return render(request, 'trip_app/about_us.html', {'site_master': site_master})


class ContactView(FormView):
    template_name = 'trip_app/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('heritage_list')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super(ContactView, self).form_valid(form)


class AreaCountryListView(View):
    def get(self, request, area):

        country_list = Country.objects.\
            filter(area=area, heritage__article__word_count_per_image__gt=0, heritage__article__blog__hidden=False).\
            annotate(article_count=Count('heritage')).order_by('short_name')

        context = {
            'area_name': country_list[0].get_area_display,
            'country_list': country_list,
        }

        return render(request, 'trip_app/country_list.html', context)


class CountryHeritageListView(View):
    def get(self, request, name):

        heritage_list = Heritage.objects.\
            filter(country__formal_name=name, article__word_count_per_image__gt=0, article__blog__hidden=False).\
            annotate(article_count=Count('article', distinct=True)).order_by('formal_name')

        country_object = Country.objects.get(formal_name=name)

        context = {
            'country_object': country_object,
            'heritage_list': heritage_list,
        }

        return render(request, 'trip_app/heritage_list.html', context)


class HeritageArticleListView(View):
    def get(self, request, name):

        article_list = Article.objects.\
            filter(blog__hidden=False, heritage__formal_name=name, word_count_per_image__gt=0).\
            select_related('blog').prefetch_related('heritage').order_by('-created_at')

        heritage_object = Heritage.objects.get(formal_name=name)

        context = {
            'heritage_object': heritage_object,
            'article_list': article_list,
        }

        return render(request, 'trip_app/article_list.html', context)


class ArticleListView(ListView):

    model = Article
    queryset = Article.objects.filter(word_count_per_image__gt=0, heritage__isnull=False, blog__hidden=False). \
        select_related('blog').prefetch_related('heritage').distinct()
    ordering = ['-created_at']
    paginate_by = 40
    template_name = 'trip_app/article_list.html'


class HeritageListView(ListView):

    model = Heritage
    queryset = Heritage.objects.\
            filter(article__word_count_per_image__gt=0, article__blog__hidden=False).\
            annotate(article_count=Count('article', distinct=True))
    ordering = ['formal_name']
    paginate_by = 2000
    template_name = 'trip_app/heritage_list.html'


class NonArticleHeritageListView(ListView):

    model = Heritage
    queryset = Heritage.objects.filter(article__isnull=True).distinct()
    ordering = ['formal_name']
    paginate_by = 40
    template_name = 'trip_app/heritage_list.html'


class BlogListView(ListView):

    model = Blog
    queryset = Blog.objects.\
            filter(hidden=False, article__heritage__isnull=False, article__word_count_per_image__gt=0).\
            annotate(article_count=Count('article', distinct=True))
    ordering = ['-article_count']
    paginate_by = 40
    template_name = 'trip_app/blog_list.html'


class BlogArticleListView(View):

    def get(self, request, pk):

        article_list = Article.objects.\
            filter(blog__pk=pk, blog__hidden=False, heritage__isnull=False, word_count_per_image__gt=0). \
            prefetch_related('heritage').order_by('-created_at').distinct()

        context = {
            'blog_object': Blog.objects.get(pk=pk),
            'article_list': article_list,
        }

        return render(request, 'trip_app/article_list.html', context)
