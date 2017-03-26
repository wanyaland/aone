from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from core.models import NewsCategory
from core.forms import NewsCategoryForm


class NewsCategoryList(ListView):
    model = NewsCategory
    template_name= 'admin/news_category/news_category_list.html'
    context_object_name = 'categories_list'


class NewsCategoryCreate(CreateView):
    model = NewsCategory
    form_class = NewsCategoryForm
    template_name= 'admin/news_category/news_category_form.html'
    success_url = reverse_lazy('admin:news_category_list')


class NewsCategoryUpdate(UpdateView):
    model = NewsCategory
    form_class = NewsCategoryForm
    template_name= 'admin/news_category/news_category_form.html'
    success_url = reverse_lazy('admin:news_category_list')


class NewsCategoryDelete(DeleteView):
    model = NewsCategory
    success_url = reverse_lazy('admin:news_category_list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)