from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from core.models import EventCategory
from core.forms import EventCategoryForm


class EventCategoryList(ListView):
    model = EventCategory
    template_name= 'admin/events/event_category_list.html'
    context_object_name = 'categories_list'


class EventCategoryCreate(CreateView):
    model = EventCategory
    form_class = EventCategoryForm
    template_name= 'admin/events/event_category_form.html'
    success_url = reverse_lazy('admin:event_category_list')


class EventCategoryUpdate(UpdateView):
    model = EventCategory
    form_class = EventCategoryForm
    template_name= 'admin/events/event_category_form.html'
    success_url = reverse_lazy('admin:event_category_list')


class EventCategoryDelete(DeleteView):
    model = EventCategory
    success_url = reverse_lazy('admin:event_category_list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)