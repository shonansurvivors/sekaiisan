from django.db.models import Count
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import View, ListView
from django.views.generic.edit import FormView

from .models import Article, Heritage, Country, SiteMaster
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

        country_list = Country.objects.filter(area=area).filter(heritage__article__word_count_per_image__gt=0).\
            annotate(article_count=Count('formal_name')).order_by('id')

        return render(request, 'trip_app/country_list.html', {'country_list': country_list})


class CountryHeritageListView(View):
    def get(self, request, name):

        heritage_list = Heritage.objects.filter(country__formal_name=name).\
            filter(article__word_count_per_image__gt=0).annotate(article_count=Count('formal_name')).order_by('id')

        context = {
            'country_name': name,
            'heritage_list': heritage_list,
        }

        return render(request, 'trip_app/heritage_list.html', context)


class HeritageListView(View):
    def get(self, request):

        heritage_list = Heritage.objects.\
            filter(article__word_count_per_image__gt=0).annotate(article_count=Count('formal_name')).order_by('id')

        return render(request, 'trip_app/heritage_list.html', {'heritage_list': heritage_list})


class HeritageArticleListView(View):
    def get(self, request, name):

        article_list = Article.objects.filter(heritage__formal_name=name).filter(word_count_per_image__gt=0)

        context = {
            'heritage_name': name,
            'article_list': article_list,
        }

        return render(request, 'trip_app/article_list.html', context)


class ArticleListView(ListView):

    model = Article
    queryset = Article.objects.filter(heritage__isnull=False).filter(word_count_per_image__gt=0).distinct()
    paginate_by = 20
    template_name = 'trip_app/article_list.html'