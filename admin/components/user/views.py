from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from core.models import Customer
from core.forms import CustomerForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User


class UserList(ListView):
    model = User
    template_name= 'admin/user/user_list.html'


class UserCreate(CreateView):
    model = User
    form_class = CustomerForm
    template_name= 'admin/user/user_form.html'

    def get_success_url(self):
        return reverse_lazy('admin:user_list')

    def form_valid(self, form):
        user_obj = form.save()
        user_obj.customer.photo = self.request.FILES.get('photo')

        return HttpResponseRedirect(self.get_success_url())


class UserUpdate(UpdateView):
    model = User
    form_class = CustomerForm
    template_name= 'admin/user/user_form.html'
    success_url = reverse_lazy('admin:user_list')

    def get_initial(self):
        return {
            'photo': self.object.customer.photo
        }

    def form_valid(self, form):
        customer = form.instance.customer
        customer.photo = self.request.FILES.get('photo')
        customer.save()

        return super(UserUpdate, self).form_valid(form)


class UserDelete(DeleteView):
    model = User
    success_url = reverse_lazy('admin:user_list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)