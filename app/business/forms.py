from django import forms
from django.contrib.auth.models import User
from .models import Review, Customer, Business
from core.utils import random_unique_string


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
