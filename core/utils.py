import datetime
import time

from django.utils.text import slugify

from core.config import COST_TYPE, WEEKDAYS_MAP
import time

def get_slug(value, unique=True, allow_unicode=False):
    value = slugify(value, allow_unicode)
    if unique:
        time_stamp = str(int(round(time.time() * 1000)))
        value += "_"+time_stamp
    return value


def update_dict(dict1, dict2):
    """
    TODO: use dict.update
    Can not use dict.update due to behavior of request.GET and request.POST
    :param dict1:
    :param dict2:
    :return: return dict1
    """
    if isinstance(dict1, dict) and isinstance(dict2, dict):
        for key in dict2:
            dict1[key] = dict2[key]
        return dict1
    return None


def remove_dups_by_key(result_set, by_key=None, identity_key='id'):
    """

    :param result_set: list of dict
    :param identity_key: unique by column
    :param by_key: combine these filed
    :return:
    """
    final_result_set = []
    identity_traversed = {}
    by_key = by_key or []
    for row in result_set:
        identity_value = row[identity_key]
        if identity_value not in identity_traversed:
            for key in by_key:
                row[key] = [row[key]]
            final_result_set.append(row)
            identity_traversed[identity_value] = len(final_result_set)-1
        else:
            result_set_index = identity_traversed[identity_value]
            obj = final_result_set[result_set_index]
            for key in by_key:
                if isinstance(obj[key], list):
                    if row[key] not in obj[key]: # or key.split("_")[0] in ("faq", "categories", 'question'):
                        obj[key].append(row[key])
                else:
                    obj[key] = list(set([obj[key], row[key]]))
    return final_result_set, list(identity_traversed.keys())


def calculate_price_category(price_min, price_max):
    """
    :param price_min:
    :param price_max:
    :return:
    """
    default_cost_type = {'label': COST_TYPE[0][1], 'icon': COST_TYPE[0][2], 'reminder': '$', 'form_id': COST_TYPE[0][3]}
    for cost_map in COST_TYPE[::-1]:
        cost_cap = cost_map[0]
        if price_max >= cost_cap:
            return {'label': cost_map[1], 'icon': cost_map[2], 'form_id': cost_map[3], 'reminder': '$$$$'[len(cost_map[2]):]}

    return default_cost_type  # else it is Ultra high expensive


def business_working_status(business_hours):
    """

    :param business_hours: [['Monday', starttime, endtime], ['Monday', starttime, endtime], ]
    :return:
    """
    now = datetime.datetime.now()
    current_day = now.weekday()
    current_time = now.time()
    working_status = {'status': False, 'label': 'Closed Now', 'form_id': 'close_now'}
    for hour in business_hours:
         if WEEKDAYS_MAP[current_day][0] == hour[0] and (hour[1] <= current_time <= hour[2]):
            return {'status': True, 'label': 'Open Now', 'start_time': hour[1], 'end_time': hour[2], 'form_id': 'open_now'}
    return working_status


def random_unique_string(prefix="GAP"):
    cur_time = str(time.time()).split(".")
    return "{}{}{}".format(prefix, cur_time[0], cur_time[1])

