from django import template

register = template.Library()

@register.inclusion_tag('core/components/paginator.html', takes_context=True)
def paginator(context, page_shift=2):
    page_obj = context['page_obj']
    paginator = context['paginator']
    page_number = page_obj.number
    total_pages = paginator.num_pages

    start_range = page_number - page_shift
    end_range = page_number + page_shift
    if start_range <= 0:
        end_range += 1 - start_range
        start_range = 1
    if end_range > total_pages:
        start_range -= (end_range - total_pages)
        end_range = total_pages
        if start_range <= 0: start_range = 1
    page_numbers = [n for n in range(start_range, end_range+1)]
    show_dots = end_range <= (total_pages - 2)
    show_last = end_range <= (total_pages - 1)
    prev_item = max(page_number-1, 1)
    next_item = min(page_number+1, total_pages)

    return {
        'page_number': page_number,
        'total_pages': total_pages,
        'page_numbers': page_numbers,
        'next_item': next_item,
        'prev_item': prev_item,
        'previous_page_number': page_obj.previous_page_number,
        'next_page_number': page_obj.next_page_number,
        'show_dots': show_dots,
        'show_last': show_last
    }