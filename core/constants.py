"""
This hosts all messages related to AfricaOne

1. 2000 <= code < 3000 are considered OK

2. 4000 <= code < 5000 are considered NOT found or validation failed

3. 5000 <= code are considered erre
"""

INACTIVE = 0
ACTIVE = 1
DRAFT = 2


MIN_SUCCESS_CODE = 2000
MAX_SUCCESS_CODE = 2999

SUCCESS_OK = 2000
