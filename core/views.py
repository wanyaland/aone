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
from hitcount.models import HitCount
from hitcount.views import HitCountMixin,HitCountDetailView
from .ranking import Ranking
from actstream import action
from actstream.models import Action
from geopy.geocoders import Nominatim
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.template import loader
from africa_one.settings import DEFAULT_FROM_EMAIL

def index(request):
    rank = Ranking()
    parent_categories = ParentCategory.objects.all()
    recent_activities = Action.objects.all()[:6]
    events =list(Event.objects.all())
    popular_events = rank.rank_events(events)[:3]
    reviews = list(Review.objects.all())
    review_of_the_day = rank.rank_reviews(reviews)[:1]
    return render(request,'core/index.html',{
        'review_of_the_day':review_of_the_day,
        'categories':parent_categories,
        'popular_events':popular_events,
        'recent_activities':recent_activities,
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

def upload_business_photos(request,pk):
    if request.method=='POST':
        business = get_object_or_404(Business,pk=pk)
        photos = request.FILES.getlist('photos')
        for photo in photos:
            BusinessPhoto.objects.create(business=business,photo=photo,photo_type='BusinessPhoto')
    return render(request,'core/businesses/business_detail.html')

def mark_photo(request,pk):
    if request.method=='POST':
        business_photo = get_object_or_404(BusinessPhoto,pk=pk)
        tag = request.POST.get('tag')
        business_photo.tag = tag
    return render(request,'core/businesses/business_detail.html')

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
            action.send(request.user,verb='tagged',target=review,action_object=review_tag)
            data = {'success':'false'}
    return HttpResponse(json.dumps(data))

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

def claim_business_find_page(request):
    return render(request,'core/claim-business/find.html')

class CategoryLandingPageView(DetailView):
    model= Category
    template_name = 'core/business-category/landing-page.html'
    def get_context_data(self, **kwargs):
        context = super(CategoryLandingPageView,self).get_context_data(**kwargs)
        businesses = Business.objects.filter(categories=self.object)
        categories = Category.objects.all()
        rank = Ranking()
        top_businesses = rank.rank_businesses(list(businesses))[:4]
        context['top_businesses']=top_businesses
        context['categories'] = categories
        return context

class CategoryListingPageView(ListView):
    model = Business
    template_name = 'core/business-category/listing-page.html'
    def get_queryset(self):
        query_set = super(CategoryListingPageView,self).get_queryset()
        return query_set
    def get_context_data(self, **kwargs):
        context = super(CategoryListingPageView,self).get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        return context

def claim_business(request,pk):
    msg="Claim Business"
    business = get_object_or_404(Business,pk=pk)
    if request.user:
        try:
            customer = Customer.objects.get(user=request.user)
            business.owner = customer
            business.save()
        except ObjectDoesNotExist:
            return redirect(reverse('core:sign_up_business'))
    return render(request,'core/claim-business/find.html',{'msg':msg})

def sign_up_business_view(request):
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        customer_form = CustomerForm(request.POST)
        if form.is_valid() and customer_form.is_valid():
            user = form.save()
            customer = customer_form.save(commit=False)
            customer.user = user
            customer.user_type = Customer.BUSINESS
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
            customer.user_type = Customer.MODERATOR
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
            customer.user_type = Customer.CUSTOMER
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
            action.send(request.user,verb='reviewed',target=business,action_object=review)
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
    login_required = True
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
            biz=business_form.save()
            if pk:
                action.send(request.user,verb='edited',target=biz)
            else:
                message = '%s was created '% biz
                EmailMessage('Business',message,to=['info@africaone.com'])
                action.send(request.user,verb='added business',target=biz)
            return redirect('core:add_business_success')
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
        action.send(request.user,verb='created event',target=event)
        return redirect(reverse('core:events_landing'))
    return render(request, 'core/events/create.html', {})

class ReviewListView(ListView):
    model = Business
    template_name = 'core/review_list.html'
    paginate_by = 10


class ReviewDetail(HitCountDetailView):
    model = Review
    count_hit=True

class EventDetail(HitCountDetailView):
    model=Event
    count_hit = True


def event_comment(request,pk):
    event = get_object_or_404(Event,pk=pk)
    if request.method=='POST':
        comment = request.POST.get('comment')
        event.comment = comment
        event.save()
    action.send(request.user,verb='commented',target=event)
    return reverse('core:events_full_view',event.id)

class BusinessDetail(HitCountDetailView):
    template_name = 'core/businesses/business_detail.html'
    model = Business
    count_hit = True
    '''
    def get(self,request,*args,**kwargs):
        sort = request.GET.get('sort')
        if sort=='date':
            self.reviews = self.get_object().review_set.all().order_by('-create_date')
        elif sort=='rating':
            self.reviews = self.get_object().review_set.all().order_by('rating_score')
        else:
            self.reviews = self.get_object().review_set.all()
        context = self.get_context_data(reviews=self.reviews)
        return self.render_to_response(context)
    '''
    def get_context_data(self, **kwargs):
        context = super(BusinessDetail,self).get_context_data(**kwargs)
        self.business =self.get_object()
        context['avg_rating']=self.business.get_avg_rating()
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
        context['business_photos']=self.business.businessphoto_set.all()[:10]
        context['reviews_number']=self.business.get_no_reviews()
        return context

class UserDetail(DetailView):
    template_name = 'core/user/user_detail.html'
    model=Customer

class UserList(ListView):
    template_name = 'core/user_list.html'
    model = Customer

class ClaimBusinessList(ListView):
    model=Business
    template_name='core/claim-business/find.html'

def search_business(request):
    '''
    view that returns list of nearest businesses
    :param request:
    :return:
    '''
    query = request.GET.get('business_name','')
    location = request.GET.get('location','')
    businesses = Business.objects.all()
    if query:
        businesses = Business.objects.filter(name__icontains=query)
    if location:
        geolocator = Nominatim()
        place = geolocator.geocode(location)
        businesses = list(businesses.distance(place.latitude,place.longitude))
    return reverse('core:category_name_listing',businesses=businesses)



def find_business(request):
    if request.is_ajax():
        name = request.GET.get('name')
        location = request.GET.get('location')
        businesses=[]
        if location:
            qs = Business.objects.distance(location)
        if name:
            if qs:
                qs = qs.filter(name=name)
            else:
                qs = Business.objects.filter(name=name)
        if qs:
            businesses=list(qs)
        data={}
        list=[]
        for business in businesses:
            biz_data={}
            biz_data['id']=business.id
            biz_data['name']=business.name
            list.append(biz_data)
        data['businesses']=list
    return HttpResponse(json.dumps(data),content_type='application/json')

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
            BusinessPhoto.objects.create(photo=file,photo_type=BusinessPhoto.REVIEWPHOTO,business=form.instance.business)
        action.send(self.request,verb='created review',target=self.object)
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
        rank = Ranking()
        ranked_listings = rank.rank_businesses(listings)
        for business in ranked_listings:
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
        if latitude  and longitude :
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
                '''
                if business.photo:
                 business_data['logo']=business.photo.url
                '''
                if business.banner_photo:
                 business_data['Banner Image']=business.banner_photo.url
                business_data['Business ID']=business.pk
                business_data['Business Name']=business.name
                business_data['Business URL']=business.web_address
                businesses.append(business_data)
        #sort businesses by ranking
        rank = Ranking()
        ranked_businesses=rank.rank_businesses(businesses)
        data={'businesses':ranked_businesses[:6]}
        return HttpResponse(json.dumps(data))

class ResetPasswordRequestView(FormView):
    template_name='core/auth-user/forgot_password.html'
    success_url = '/login/'
    form_class = PasswordResetRequestForm

    @staticmethod
    def validate_email_address(email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self,request,*args,**kwargs):
        '''
        A normal post request which takes input from field 'email'

        '''
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email"]
        if self.validate_email_address(data) is True:
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    c={
                            'email':user.email,
                            'domain':request.META['HTTP_HOST'],
                            'site_name':'africaone.com',
                            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                            'user':user,
                            'token':default_token_generator.make_token(user),
                            'protocol':'http',

                            }
                    subject_template_name='registration/password_reset_subject.txt'
                    email_template_name = 'core/auth-user/password_reset_email.html'
                    subject = loader.render_to_string(subject_template_name,c)
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name,c)
                    email=EmailMessage(subject,email,to=[user.email])
                    email.send()
                    messages.success(request,'An email has been sent to '+data)
                    result = self.form_valid(form)
                    return result
        result=self.form_invalid(form)
        messages.error(request,'No user is associated with this email address')
        return result

class PasswordResetConfirmView(FormView):
    template_name = ''