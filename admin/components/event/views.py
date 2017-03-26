from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from core.models import Event
from core.forms import EventForm
from core.views import combineEventDateAndTime


class EventList(ListView):
    model = Event
    template_name= 'admin/event/event_list.html'


class EventCreate(CreateView):
    model = Event
    form_class = EventForm
    template_name= 'admin/event/event_form.html'

    def get_success_url(self):
        return reverse_lazy('admin:event_list')

    def form_valid(self, form):
        form = combineEventDateAndTime(form)

        event_obj = form.save(commit=False)
        event_obj.owner = self.request.user.customer
        event_obj.save()
        form.save_m2m()

        return HttpResponseRedirect(self.get_success_url())


class EventUpdate(UpdateView):
    model = Event
    form_class = EventForm
    template_name= 'admin/event/event_form.html'

    def get_success_url(self):
        return reverse_lazy('admin:event_list')

    def get_initial(self):
        # Set initial values for date and time in the form
        initial = self.initial.copy()
        initial['start_date'] = self.object.event_date.strftime("%d/%m/%Y")
        initial['start_time'] = self.object.event_date.strftime("%I:%M %p")
        if self.object.end_date:
            initial['finish_date'] = self.object.end_date.strftime("%d/%m/%Y")
            initial['finish_time'] = self.object.end_date.strftime("%I:%M %p")
        
        return initial

    def form_valid(self, form):
        form = combineEventDateAndTime(form)

        return super(EventUpdate, self).form_valid(form)


class EventDelete(DeleteView):
    model = Event
    success_url = reverse_lazy('admin:event_list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)