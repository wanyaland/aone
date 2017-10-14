from django import forms
from django.contrib.auth.models import User
from .models import Review, Customer, Business, ReviewTag
from core.utils import random_unique_string
from django.contrib.auth.forms import UserCreationForm 


class ReviewForm(forms.ModelForm):
    listing_id = forms.IntegerField(required=True)
    email = forms.EmailField(required=False)

    def __init__(self, request, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self._request = request

    class Meta:
        model = Review
        fields = ['title', 'rating', 'review', 'attachment']

    def clean(self):
        cleaned_data = super(ReviewForm, self).clean()
        cleaned_data['customer'] = self.user_validate()
        cleaned_data['business'] = self.listing_validate()
        return cleaned_data

    def listing_validate(self):
        listing_id = self.cleaned_data['listing_id']
        business_listing = Business.objects.filter(status=True, id=listing_id)
        if business_listing.exists():
            return business_listing[0]
        else:
            raise Exception("no business found to review with this id")

    def user_validate(self):
        if self._request.user.is_authenticated():
            """
            use logged in user instance
            """
            user = self._request.user
            customer = Customer.objects.filter(user=user)
            if customer.exists():
                return customer[0]
            else:
                return Customer.objects.creare(user=user)
        else:
            # create new user and add this user as reviewer
            email = self.cleaned_data.get('email')
            if email:
                user = User.objects.create_user(random_unique_string(prefix="user"), email, random_unique_string(prefix="pass"))
                customer = Customer.objects.filter(user=user)
                if customer.exists():
                    return customer[0]
                return Customer.objects.creare(user=user)
            else:
                raise Exception("No Email found")


class ReviewTagForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(ReviewTagForm, self).__init__(*args, **kwargs)
        self._request = request

    class Meta:
        model = ReviewTag
        fields = ['review', 'tag']

    def review_validate(self):
        review_id = self.cleaned_data['review']
        review = Review.objects.filter(status=True, id=review_id)
        if review.exists():
            return review[0]
        else:
            raise Exception("no business found to review with this id")

    def clean(self):
        cleaned_data = super(ReviewTagForm, self).clean()
        # cleaned_data['review'] = self.review_validate()
        cleaned_data['user'] = self._request.user
        cleaned_data['cookie'] = self._request.META.get('HTTP_COOKIE')
        cleaned_data['ip_address'] = self._request.META.get('HTTP_X_FORWARDED_FOR') or self._request.META.get('REMOTE_ADDR')
        cleaned_data['user_agent'] = self._request.META.get('HTTP_USER_AGENT')
        return cleaned_data

class SignUpForm(UserCreationForm):
    class Meta:
       model = User
       fields = ('username','email')
