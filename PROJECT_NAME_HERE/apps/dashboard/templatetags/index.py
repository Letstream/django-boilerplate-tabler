from django import template
import math
register = template.Library()

@register.simple_tag
def get_key_from_list(List, index, key=None):
    if key is None:
        return List[int(index)]
    else:
        return List[int(index)].get(str(key), None)

@register.filter(name="range_year")
def range_year(start,end):
    return range(start,end)

@register.filter(name="num_of_pages")
def num_of_pages(total_entries, page_size):
    return math.ceil(total_entries/page_size)

@register.filter(name="page_range")
def page_range(num_pages):
    return range(1,num_pages+1)

@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    # if 'page' in updated.keys():
    for key in kwargs.keys():
        updated[key] = kwargs[key]
    return updated.urlencode()
