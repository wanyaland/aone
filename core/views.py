from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from forms import *
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from core.models import *
from django.views.generic import *
from django.core.urlresolvers import reverse
from djangoratings.views import AddRatingView,AddRatingFromModel
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import HttpResponse,HttpResponseRedirect
import json
from geopy.distance import vincenty
from django.views.decorators.csrf import csrf_exempt
from tag_manager import TagManager
from django.core.exceptions import ObjectDoesNotExist
import datetime

def index(request):
    parent_categories = ParentCategory.objects.all()
    businesses= Business.objects.all()[:5]
    events = Event.objects.all()
    return render(request,'core/index.html',{
        'categories':parent_categories,
        'businesses':businesses,
        'events':events,
    })

def logout_view(request):
    logout(request)
    return redirect('core:home')

def login_view(request):
    next_url=''
    state = None
    if request.GET:
        next_url = request.GET.get('next')
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.POST.get('next')
        user = authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request,user)
                if  next_url:
                    return HttpResponseRedirect(next_url)
                else:
                    return HttpResponseRedirect(reverse('core:home'))
            else:
                state="Your account is not active"
        else:
            state="Your username and password do not match"
    return render(request,'core/auth-user/login.html',{'next':next_url,'state':state,'request':request})

def tag_review(request):
    review_id = request.POST.get('review_id')
    tagged = request.POST.get('tag')
    if review_id:
        tag_manager = TagManager()
        review = get_object_or_404(Review,pk=review_id)
        ip_address = request.META['REMOTE_ADDR']
        review_tag=tag_manager.add_tag(review,tagged,request.user,ip_address)
        if review_tag:
            data ={'success':'true'}
        else:
            data = {'success':'false'}
    return HttpResponse(json.dumps(data))

def forgot_password_view(request):
    return render(request,'core/auth-user/forgot_password.html', {})

def about(request):
    return render(request,'core/static-info/about.html', {})

def StaticPrivacyPolicyView(request):
    return render(request,'core/static-info/privacy-policy.html', {})

def StaticAdvertisingView(request):
    return render(request,'core/static-info/advertising.html', {})

def StaticTermsConditionsView(request):
    return render(request,'core/static-info/terms-conditions.html', {})

def AddBusinessSuccessView(request):
    return render(request,'core/businesses/add_business_success.html', {})

def CategoryLandingPageView(request):
    return render(request,'core/business-category/landing-page.html', {})

def CategoryListingPageView(request):
    return render(request,'core/business-category/listing-page.html', {})

def claim_business_find_page(request):
    return render(request,'core/claim-business/find.html')

def sign_up_business_view(request):
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        customer_form = CustomerForm(request.POST)
        if form.is_valid() and customer_form.is_valid():
            user = form.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.user_type = 'B'
            user.save()
            customer.save()
    else:
        form = RegistrationForm()
        customer_form = CustomerForm()
    return render(request,'core/auth-user/sign_up_business.html',{
        'form':form,'customer_form':customer_form
    })

def sign_up_moderator(request):
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        customer_form = CustomerForm(request.POST)
        if form.is_valid() and customer_form.is_valid():
            user = form.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.user_type = 'M'
            user.save()
            customer.save()
    else:
        form = RegistrationForm()
        customer_form = CustomerForm()
    return render(request,'core/auth-user/sign_up.html',{
        'form':form,'customer_form':customer_form
    })

def sign_up(request):
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        customer_form = CustomerForm(request.POST,request.FILES)
        if  form.is_valid() and customer_form.is_valid() :
            user = form.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.user_type = 'C'
            user.save()
            customer.save()
            return redirect('core:home')
    else:
        form = RegistrationForm()
        customer_form = CustomerForm()
    return render(request,'core/auth-user/sign_up.html',{
        'form':form,'customer_form':customer_form
    })


class BusinessListView(ListView):
    model = Business
    def get_queryset(self):
        return Business.objects.filter(Business,name=self.args[0])


class BusinessUserView(View):
    template_name = 'core/business_user.html'

    def get(self,request,*args,**kwargs):
        customer = Customer.objects.filter(user=request.user)
        pk = self.kwargs.get('pk')
        if pk is None:
            business_form = BusinessForm()
            review_form = ReviewForm()
        else:
            review = get_object_or_404(Review,pk=pk)
            business = Review.objects.filter(review=review,customer=customer)
            review_form = ReviewForm(instance=review)
            business_form = BusinessForm(instance=business)
        return render(
            request,
            self.template_name,{
               'review_form':review_form,
                'business_form':business_form,
                'action_url':reverse('core:business_user_edit',kwargs={'pk':pk}) if pk else reverse('core:business_user_add'),
            }
        )

    def post(self,request,*args,**kwargs):
        customer = Customer.objects.filter(user=request.user)
        pk = self.kwargs.get('pk')
        if pk is None:
            review_form = ReviewForm(request.POST)
            business_form = BusinessForm(request.POST,request.FILES)
        else:
            review = get_object_or_404(Review,pk=pk)
            business = Review.objects.filter(review=review,customer=customer)
            review_form = ReviewForm(instance=review,data=request.POST)
            business_form = BusinessForm(instance=business,data=request.POST,files=request.FILES)
        if business_form.is_valid() and review_form.is_valid():
            review = review_form.save(commit=False)
            business = business_form.save()
            review.business= business
            review.customer = Customer.objects.get(user=request.user)
            review.save()
            review_type = ContentType.objects.get_for_model(review)
            score = review.POST['rating']
            params = {
                'content_type_id':review_type.id,
                'object_id':review.id,
                'field_name': 'rating',
                'score':score,
            }
            AddRatingView()(request,**params)
            return redirect('core:review_list')
        else:
            return render(request,
                      self.template_name,{
                        'review_form':review_form,
                        'business_form':business_form,
                        'action_url':reverse('core:business_user_edit',kwargs={'pk':pk}) if pk else reverse('core:business_user_add'),
                      })


class BusinesView(View):

    template_name = 'core/business_create.html'

    def get(self,request,*args,**kwargs):
        pk = self.kwargs.get('pk')
        if pk is None:
            business_form= BusinessForm()
        else:
            business = get_object_or_404(Business,pk=pk)
            business_form = BusinessForm(instance=business,files=request.FILES)
        return render(
            request,
            self.template_name,
            {
                'form':business_form,
                'action_url':reverse('core:business_edit',
                                     kwargs={'pk':pk} ) if pk else reverse('core:business_add')

            }
        )

    def post(self,request,*args,**kwargs):
        pk=self.kwargs.get('pk')
        if pk is not None:
            business = get_object_or_404(Business,pk=pk)
            business_form = BusinessForm(instance=business,data=request.POST,files=request.FILES)
        else:
            business_form = BusinessForm(request.POST,request.FILES)
        if business_form.is_valid():
            business_form.save()
            return redirect('core:add_business_successful')
        else:
            return render(
                request,self.template_name,
                {
                    'form':business_form,
                    'action_url':reverse('core:business_edit',kwargs={'pk':pk}) if pk else reverse('core:business_add')
                }
            )

def add_business_successful(request):
    # return render(request,'core/business_successful.html')
    return render(request,'core/businesses/add_business_success.html', {})

def UserDetailTestPageView(request,pk):
    customer = get_object_or_404(Customer,pk=pk)
    return render(request, 'core/user/user_detail-temp.html', {'customer':customer,})

def events_landing(request):
    events = Event.objects.all()
    context = {'events':events}
    return render(request, 'core/events/landing.html',context)

def events_listing(request):
    return render(request, 'core/events/listing.html')

def events_detail(request,pk):
    event=get_object_or_404(Event,pk=pk)
    return render(request, 'core/events/full.html',{'event':event})

def create_event(request):
    if request.method=='POST':
        name = request.POST.get('event_name')
        where = request.POST.get('where')
        description = request.POST.get('description')
        price = request.POST.get('price')
        event = Event(name=name,description=description,where=where,price=price)
        event.save()
        return redirect(reverse('core:events_landing'))
    return render(request, 'core/events/create.html', {})

class ReviewListView(ListView):
    model = Business
    template_name = 'core/review_list.html'


class ReviewDetail(DetailView):

    model = Review

    def get_client_ip(self):
        ip = self.request.META.get('HTTP_X_FORWARDED_FOR',None)
        if ip:
            ip= ip.split(', ')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR','')
        return ip

    def tracking_hit_post(self):
        review = self.model.objects.get(pk=self.object.id)
        try:
            ReviewView.objects.get(review=review,ip=self.get_client_ip(),session=self.request.session.session_key)
        except ObjectDoesNotExist:
            import socket
            dns = str(socket.getfqdn(self.get_client_ip())).split('.')[-1]
            try:
                if int(dns):
                    view = ReviewView(review=review,
                                      ip=self.get_client_ip(),
                                      created=datetime.datetime.now(),
                                      session=self.request.session.session_key)
                    view.save()
                else: pass
            except ValueError:pass

    def get_context_data(self,**kwargs):
        context_data= super(ReviewDetail,self).get_context_data(**kwargs)
        context_data['get_client_ip']= self.get_client_ip()
        context_data['tracking_hit_post'] = self.tracking_hit_post()



def event_comment(request,pk):
    event = get_object_or_404(Event,pk=pk)
    if request.method=='POST':
        comment = request.POST.get('comment')
        event.comment = comment
        event.save()
    return reverse('core:events_full_view',event.id)

class BusinessDetail(DetailView):

    template_name = 'core/businesses/business_detail.html'
    model = Business

    def get_context_data(self, **kwargs):
        context = super(BusinessDetail,self).get_context_data(**kwargs)
        self.business =self.get_object()
        sort = self.request.GET.get('sort')
        if sort=='date':
         self.reviews = self.business.review_set.all().order_by('-create_date')
        elif sort=='rating':
         self.reviews = self.business.review_set.all().order_by('rating_score')
        else:
         self.reviews = self.business.review_set.all()
        self.categories = self.business.categories
        paginator = Paginator(self.reviews,5)
        page = self.request.GET.get('page')
        try:
            review_list = paginator.page(page)
        except PageNotAnInteger:
            review_list = paginator.page(1)
        except EmptyPage:
            review_list = paginator.page(paginator.num_pages)
        context['reviews'] = review_list
        business_set = []
        review_photos = []
        categories = self.categories.all()
        context['categories'] = categories
        for category in categories:
            for business in category.business_set.all():
                if business!= self.business:
                    business_set.append(business)
        context['business_set']= business_set[:3]
        for review in self.reviews:
            for photo in review.businessphoto_set.all():
                review_photos.append(photo)
        context['review_photos']=review_photos[:5]
        return context

class UserDetail(DetailView):
    template_name = 'core/user/user_detail.html'
    model=Customer

class UserList(ListView):
    template_name = 'core/user_list.html'
    model = Customer

class ClaimBusinessList(ListView):
    model=Business

def search_business(request):
    query = request.GET.get('business_name','')
    location = request.GET.get('location','')
    if query:
        qset = (
            Q(name__icontains=query)
        )
        results = Business.objects.filter(qset).distinct()
    else:
        results = []
    return render(request,'core/business-category/listing-page.html',{
        'results':results,
        'query':query,
    })

def get_listings_parent(request):
    if request.method=='GET':
        jsonData = {}
        parent_id = request.GET.get('parent_id')
        parent_category = get_object_or_404(ParentCategory,parent_id)
        return HttpResponse(json.dumps(jsonData),content_type="application/json")

class BusinessList(ListView):
    model = Business
    paginate_by = 30


class ReviewCreate(CreateView):
    form_class = ReviewForm
    template_name = 'core/review_form.html'

    def get_success_url(self):
        return reverse('core:review_list')

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('business_pk')
        business = get_object_or_404(Business,pk=pk)
        review_list = Review.objects.filter(business=business)
        context = super(CreateView,self).get_context_data(**kwargs)
        context['business']=business
        context['reviews']=review_list
        return context

    def form_valid(self,form):

        context = self.get_context_data()
        form.instance.business = context['business']
        #form.instance.rating.add(score=self.request.POST['rating'],user=self.request.user,ip_address=self.request.META['REMOTE_ADDR'])
        image_list =    self.request.FILES.getlist('files')
        response=super(ReviewCreate,self).form_valid(form)
        review_type = ContentType.objects.get_for_model(self.object)
        score = self.request.POST['rating']
        params = {
                'content_type_id':review_type.id,
                'object_id':self.object.id,
                'field_name': 'rating',
                'score':score,
         }
        AddRatingView()(self.request,**params)
        for file in image_list:
            BusinessPhoto.objects.create(photo=file,review=self.object)
        return response


class ReviewEdit(UpdateView):
    form_class=ReviewForm
    template_name = 'core/review_form.html'

class ReviewDelete(DeleteView):
    model = Review

class GetHomePageBusinesses(View):
    def get(self,request,*args,**kwargs):
        parent_id = request.GET.get('parent_id')
        parent_cat = get_object_or_404(ParentCategory,id=parent_id)
        categories = parent_cat.category_set.all()
        businesses = []
        listings=[]
        data={}
        listings = list(Business.objects.filter(categories=categories).all())
        listings.sort(key=lambda x:x.get_avg_rating(),reverse=True)
        for business in listings:
             business_data={}
             business_data['id']=business.pk
             business_data['name']=business.name
             businesses.append(business_data)
        data={'businesses':businesses[:10]}
        return HttpResponse(json.dumps(data))

class GetNearestBusinesses(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(GetNearestBusinesses, self).dispatch(request, *args, **kwargs)

    def post(self,request,*args,**kwargs):
        longitude = request.POST.get('longitude')
        latitude = request.POST.get('latitude')
        businesses = []
        listings = list(Business.objects.all())
        if latitude == 0 and longitude == 0:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

        for business in listings:
              user_location = (latitude,longitude)
              business_location=(business.latitude,business.longitude)
              print str(vincenty(user_location,business_location).miles) + " " + business.name
              if vincenty(user_location,business_location).miles <= 5:
                business_data={}
                if business.photo:
                 business_data['logo']=business.photo.url
                if business.banner_photo:
                 business_data['banner']=business.banner_photo.url
                business_data['name']=business.name
                businesses.append(business_data)
        data={'businesses':businesses[:6]}
        return HttpResponse(json.dumps(data))


