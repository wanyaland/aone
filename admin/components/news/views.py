from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from core.models import News
from core.forms import NewsForm


class NewsList(ListView):
    model = News
    template_name= 'admin/news/news_list.html'


class NewsCreate(CreateView):
    model = News
    form_class = NewsForm
    template_name= 'admin/news/news_form.html'
    success_url = reverse_lazy('admin:news_list')


class NewsUpdate(UpdateView):
    model = News
    form_class = NewsForm
    template_name= 'admin/news/news_form.html'
    success_url = reverse_lazy('admin:news_list')


class NewsDelete(DeleteView):
    model = News
    success_url = reverse_lazy('admin:news_list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)