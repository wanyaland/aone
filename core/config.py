# CATEGORY
BUSINESS = 'B'
EVENT = 'E'
CATEGORY_TYPES = {
        (BUSINESS, 'Business'),
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

# File upload path
FILE_UPLOAD_PATH = (
    ('businesses/banner/%Y/%m/%d', 'BUSINESS_BANNER'),
    ('businesses/%Y/%m/%d', 'BUSINESS_PHOTO'),
    ('avatars/%Y/%m/%d', 'AVATARS'),
    ('news/%Y/%m/%d', 'NEWS'),
    ('event/%Y/%m/%d', 'EVENT')
)

#  COST TYPES
COST_TYPE = (
    # cost_type: cost_type_icon
    (25, 'Inexpensive', '$'),
    (50, 'Moderate', '$$'),
    (75, 'Pricey', '$$$'),
    (100, 'Ultra High End', '$$$$')
)


# WEEKDAYS
WEEKDAYS_MAP = {
    0: ('Monday', 'Monday'),
    1: ('Tuesday', 'Tuesday'),
    2: ('Wednesday', 'Wednesday'),
    3: ('Thursday', 'Thursday'),
    4: ('Friday', 'Friday'),
    5: ('Saturday', 'Saturday'),
    6: ('Sunday', 'Sunday'),
}
WEEKDAYS = WEEKDAYS_MAP.values()
# PRICE_MIN_MAX
