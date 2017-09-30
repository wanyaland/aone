# CATEGORY
BUSINESS = 'B'
EVENT = 'E'
CATEGORY_TYPES = {
        (BUSINESS, 'Event'),
        (EVENT, 'Event')
}

# USERS
CUSTOMER = 'C'
MODERATOR = 'M'
USER_TYPES = {
    (BUSINESS, 'Business'),
    (CUSTOMER, 'Customer'),
    (MODERATOR, 'Moderator'),
}


# TAGS
REVIEW_TAG_CHOICES = {
        ('C', 'COOL'),
        ('H', 'HELPFUL'),
        ('F', 'FUNNY'),
    }

# PHOTOS
BUSINESS_PHOTO = 'BP'
REVIEW_PHOTO = 'RP'
USER_PHOTO = 'UP'
PHOTO_TYPE = (
    (BUSINESS_PHOTO, 'BusinessPhoto'),
    (REVIEW_PHOTO, 'ReviewPhoto'),
    (USER_PHOTO, 'UserPhoto')
)
PHOTO_TAG_HELPFUL = 'H'
PHOTO_TAG_INAPPROPRIATE = 'I'
PHOTO_TAG = (
    (PHOTO_TAG_HELPFUL, 'Helpful'),
    (PHOTO_TAG_INAPPROPRIATE, 'Inappropriate'),
)