from django.shortcuts import render, redirect
from core.models import Business,Category,ParentCategory,BusinessPhoto,Review,Event,Country,BusinessHours
from django.contrib.auth.models import User
from django.views.generic import *
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.core import serializers
import json
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse,reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404,render_to_response
from geoposition.fields import Geoposition
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate,login,logout
import operator
from django.db.models import Q
import datetime

from django.template import RequestContext

# Create your views here.

def login_user(request):
  state="Please login below"
  username=password=''
  next_url=''
  if request.GET:
     next_url=request.GET.get('next')
  if request.POST:
     username = request.POST.get('username')
     password = request.POST.get('password')
     next_url= request.POST.get('next')
     user = authenticate(username=username,password=password)
     if user is not None:
       if user.is_active:
         login(request,user)
         return HttpResponseRedirect(next_url)
       else:
         state="Your account is not active"
     else:
        state="Your username and/or password were incorrect"
  return render(request,'admin/auth.html',{'state':state,'username':username,'password':password,'next':next_url})

def logout(request):
    logout(request)
    return redirect('core:home')
         

class BusinessList(ListView):
    model = Business
    queryset = Business.objects.all()
    template_name = 'admin/index.html'
    paginate_by = 50
    @method_decorator(login_required(login_url='/manager/login/'))
    def dispatch(self,*args,**kwargs):
      return super(BusinessList,self).dispatch(*args,**kwargs)

    def get_queryset(self):
        result =super(BusinessList,self).get_queryset()
        name = self.request.GET.get('name')
        location = self.request.GET.get('location')
        categories = self.request.GET.getlist('categories')
        claimed = self.request.GET.get('claim-status')
        query_list=[]
        if name:
            query_list.append(Q(name__icontains=name))
        if location:
            query_list.append(Q(city__icontains=location))
        if claimed:
            if claimed=='claimed':
                query_list.append(Q(claimed=True))
            elif claimed=='unclaimed':
                query_list.append(Q(claimed=False))
        if categories:
            queries=[Q(categories__pk=category) for category in categories]
            result = result.filter(reduce(operator.or_,queries))
        if query_list:
            result=result.filter(reduce(operator.and_,query_list))
        return result

    def get_context_data(self, **kwargs):
        context = super(BusinessList,self).get_context_data(**kwargs)
        context['no_of_businesses']=Business.objects.all().count()
        context['no_of_events']=Event.objects.all().count()
        context['no_of_reviews']=Review.objects.all().count()
        context['no_of_users']=User.objects.all().count()
        context['no_of_business_owners']=0
        return context


class ParentCategoryCreate(CreateView):
    def post(self,request,*args,**kwargs):
        name = request.POST['name']
        icon = request.POST['icon']
        parent_category = ParentCategory(name=name,icon=icon)
        parent_category.save()
        data = {'name':parent_category.name,'id':parent_category.pk,'icon':parent_category.icon}
        return HttpResponse(json.dumps(data))

class ParentCategoryUpdate(UpdateView):
    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        icon = request.POST['icon']
        pk = request.POST['id']
        parent_category = get_object_or_404(ParentCategory,pk=pk)
        parent_category.name = name
        parent_category.icon = icon
        parent_category.save()
        data = {'name':parent_category.name,'id':parent_category.pk,'icon':parent_category.icon}
        return HttpResponse(json.dumps(data))

class ParentCategoryDelete(View):
    def post(self, request, *args, **kwargs):
        pk = request.GET.get('id')
        parent_category = get_object_or_404(ParentCategory,pk=pk)
        parent_category.delete()
        data = {'success':'true'}
        return HttpResponse(json.dumps(data))

def delete_parent_category(request,*args,**kwargs):
    pk= request.GET.get('id')
    parent_category = get_object_or_404(ParentCategory,pk=pk)
    parent_category.delete()
    data = {'success':'true'}
    return HttpResponse(json.dumps(data),content_type="application/json")

class CategoryCreate(View):
    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        parent_id = request.POST.get('super-category-id')
        parent_category = get_object_or_404(ParentCategory,pk=parent_id)
        category = Category.objects.create(name=name,parent_category=parent_category)
        data = {'name':category.name,'super-category-id':parent_category.pk,'id':category.pk}
        return HttpResponse(json.dumps(data))

class CategoryUpdate(UpdateView):
    def post(self, request, *args, **kwargs):
        name= request.POST['name']
        cat_id = request.POST['id']
        parent_id = request.POST['super-category-id']
        category = get_object_or_404(Category, pk=cat_id)
        parent = get_object_or_404(ParentCategory,pk=parent_id)
        category.name = name
        category.parent_category = parent
        category.save()
        data = {'name':category.name,'super-category-id':parent.pk,
                'id':category.pk,}
        return HttpResponse(json.dumps(data))

def delete_category(request,*args,**kwargs):
    pk= request.GET.get('id')
    category = get_object_or_404(Category,pk=pk)
    category.delete()
    data = {'success':'true'}
    return HttpResponse(json.dumps(data),content_type="application/json")



class BusinessCreate(CreateView):
   model=Business
   template_name= 'admin/businesses/business_form.html'
   success_url = '/manager/manage_business_photos/'

   def get_context_data(self, **kwargs):
    context = super(BusinessCreate,self).get_context_data(**kwargs)
    countries={'UG':'UGANDA','KE':'KENYA',}
    context['countries']=countries
    context['action_url'] = reverse('admin:create_business')
    return context

   def post(self, request, *args, **kwargs):
       name = request.POST.get('name')
       country_string = request.POST.get('country')
       address = request.POST.get('address')
       city = request.POST.get('city')
       website = request.POST.get('website')
       categories = request.POST.getlist('categories[]')
       hours = request.POST.getlist('hours[]')
       popoularity = request.POST.get('popularity')
       latitude = request.POST.get('latitude')
       longitude = request.POST.get('longitude')
       if latitude == '':
           latitude=0
       if longitude=='':
           longitude=0
       country = Country.objects.get_or_create(name=country_string)[0]
       business = Business(name=name,country=country,address=address,web_address=website,latitude=float(latitude),
                           longitude=float(longitude),popularity_rating=popoularity,city=city)
       business.save()
       for period in hours:
           period_stamps = period.split()
           business_hour = BusinessHours.objects.get_or_create(day=period_stamps[0],opening_hours=period_stamps[1],closing_hours=period_stamps[2])[0]
           business.business_hours.add(business_hour)

       for category in categories:
           category = get_object_or_404(Category,id=category)
           business.categories.add(category)

       business.save()
       return render(request,'admin/businesses/business_manage_photos.html',{'pk':business.id})


class BusinessDelete(DeleteView):
    model = Business
    success_url = reverse_lazy('admin:home')


class BusinessUpdate(UpdateView):
    model = Business
    template_name = 'admin/businesses/business_form.html'
    success_url = '/manager/'


    def get_context_data(self, **kwargs):
        context = super(BusinessUpdate,self).get_context_data(**kwargs)
        categories_size = self.get_object().categories.all().count()
        categories = self.get_object().categories.all()
        countries={'UG':'UGANDA','KE':'KENYA',}
        context['action_url']= reverse('admin:update_business',kwargs= {'pk':self.get_object().id})
        context['categories_size']= categories_size
        context['categories']=categories
        context['countries']=countries
        return context

    def post(self, request, *args, **kwargs):
       name = request.POST.get('name')
       country_string = request.POST.get('country')
       address = request.POST.get('address')
       city = request.POST.get('city')
       website = request.POST.get('website')
       categories = request.POST.getlist('categories[]')
       hours = request.POST.getlist('hours[]')
       popoularity = request.POST.get('popularity')
       latitude = request.POST.get('latitude')
       longitude = request.POST.get('longitude')
       if latitude == '':
           latitude=0
       if longitude=='':
           longitude=0
       country = Country.objects.get_or_create(name=country_string)[0]
       business = Business(name=name,country=country,address=address,web_address=website,latitude=float(latitude),
                           longitude=float(longitude),popularity_rating=popoularity,city=city)
       business.save()
       for period in hours:
           period_stamps = period.split()
           business_hour = BusinessHours.objects.get_or_create(day=period_stamps[0],opening_hours=period_stamps[1],closing_hours=period_stamps[2])[0]
           business.business_hours.add(business_hour)

       for category in categories:
           category = get_object_or_404(Category,id=category)
           business.categories.add(category)

       business.save()
       return render(request,'admin/businesses/business_manage_photos.html',{'pk':business.id})



def manage_business_photos(request,pk):
    business = get_object_or_404(Business,pk=pk)
    business_photos = business.businessphoto_set.filter(business=business)
    return render(request,'admin/businesses/business_manage_photos.html',{'pk':pk,'business':business,'photos':business_photos})

def categories_json(request,*args ,**kwargs):
    jsonData = {}
    query = request.GET.get('query')
    categories = Category.objects.filter(name__icontains=query)
    jsonData['query'] = query
    suggestions = []
    for category in categories:
        category_data = {}
        category_data['value']=category.parent_category.name+">"+category.name
        category_data['data']=category.id
        suggestions.append(category_data)
    jsonData['suggestions'] = suggestions
    return HttpResponse(json.dumps(jsonData), content_type="application/json")


class BusinessManagePhotos(CreateView):
   model=Business
   template_name= 'admin/businesses/business_manage_photos.html'


class ManageCategories(CreateView):
   model=Business
   template_name= 'admin/categories/manage_categories.html'


class ManageReviews(CreateView):
    model=Review
    template_name= 'admin/reviews/manage_reviews.html'


class ManageUsers(CreateView):
    model = User
    template_name = 'admin/users/manage_users.html'


class CreateUser(View):
    model = User
    template_name = 'admin/users/create_user.html'


class UploadBusinessPhotos(View):
    def post(self,request,*args,**kwargs):
        photos = request.FILES.getlist('photos')
        business_id = request.POST.get('business_id')
        photo_type = request.POST.get('photo_type')
        business = get_object_or_404(Business,pk=business_id)
        photo_array=[]
        photo_id_array=[]
        for photo in photos:
            business_photo=BusinessPhoto.objects.create(photo=photo,photo_type=photo_type,business=business)
            photo_array.append(business_photo.photo.url)
            photo_id_array.append(business_photo.pk)
        data={'business_photos':photo_array,'photo_ids':photo_id_array,'business_id':business.pk}
        return HttpResponse(json.dumps(data))


class UploadBannerImage(View):
    def post(self,request,*args,**kwargs):
        banner = request.FILES.get('image')
        business_id = request.POST.get('business_id')
        business = get_object_or_404(Business,pk=business_id)
        business.banner_photo = banner
        business.save()
        data={'img_url': business.banner_photo.url, 'business_id':business.pk}
        return HttpResponse(json.dumps(data))


class UploadLogo(View):
    def post(self,request,*args,**kwargs):
        logo = request.FILES.get('image')
        business_id = request.POST.get('business_id')
        business = get_object_or_404(Business,pk=business_id)
        business.photo = logo
        business.save()
        data = {'img_url':business.photo.url,'business_id':business.pk}
        return HttpResponse(json.dumps(data))


class DeleteBusinessImage(View):
    def post(self,request,*arg,**kwargs):
        file_id = request.POST['file_id']
        photoType = request.POST['photoType']
        business_photo = get_object_or_404(BusinessPhoto,pk=file_id)
        business_photo.delete()
        success = True
        data={'success':success}
        return HttpResponse(json.dumps(data))

class EditCaption(View):
    def post(self,request,*args,**kwargs):
        file_id = request.POST['file_id']
        caption = request.POST['caption']
        photo_type = request.POST['photo_type']
        business_photo = get_object_or_404(BusinessPhoto,pk=file_id)
        business_photo.caption = caption
        business_photo.save()
        data ={'file_id':business_photo.pk,'caption':business_photo.caption,'photo_type':business_photo.photo_type}
        return HttpResponse(json.dumps(data))

class DeleteBannerImage(View):
    def post(self,request,*args,**kwargs):
        business_id = request.POST.get('business_id')
        business = get_object_or_404(Business,pk=business_id)
        business.banner_photo = None
        business.save()
        data={'success':True}
        return HttpResponse(json.dumps(data))

class DeleteLogoImage(View):
    def post(self,request,*args,**kwargs):
        business_id = request.POST.get('business_id')
        business = get_object_or_404(Business,pk=business_id)
        business.photo = None
        business.save()
        data = {'success':True}
        return HttpResponse(json.dumps(data))


class GetCategories(View):
    def get(self,request,*args,**kwargs):
        parent_categories = ParentCategory.objects.all()
        parent_cats=[]
        for parent_categ in parent_categories:
            parent_category={}
            parent_category['id']=parent_categ.id
            parent_category['name']=parent_categ.name
            parent_category['icon']=parent_categ.icon
            categories = parent_categ.category_set.all()
            cat_arrays=[]
            for category in categories:
                categories_array={}
                categories_array['id']=category.id
                categories_array['name']=category.name
                cat_arrays.append(categories_array)
            parent_category['categories']=cat_arrays
            parent_cats.append(parent_category)
        return HttpResponse(json.dumps(parent_cats),content_type="application/json")