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
        ('LOVE', 'LOVE'),
        ('LOL', 'LOL'),
        ('INTERESTING', 'INTERESTING'),
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
    (25, 'Inexpensive', '$', 'inexpensive'),
    (50, 'Moderate', '$$', 'moderate'),
    (75, 'Pricey', '$$$', 'pricey'),
    (100, 'Ultra High End', '$$$$', 'ultra')
)

COST_TYPE_DICT = [{'price': i[0], 'label': i[1], 'icon':i[2], 'form_id': i[3]} for i in COST_TYPE]

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

CONTACTUS_REVIEW_STATUS = (
    ('OPEN', 'OPEN'),
    ('REVIEWED', 'REVIEWED'),
    ('PROCESSING', 'PROCESSING'),
    ('RESOLVED', 'RESOLVED'),
    ('CLOSED', 'CLOSED'),
)

