from django.core.paginator import Paginator

def paginate_queryset(queryset, request, items_per_page=10):
    """
    Paginate the given queryset based on the request.

    Parameters:
    - queryset: The list or queryset to paginate.
    - request: The HTTP request containing the page number.
    - items_per_page: Number of items per page (default is 10).

    Returns:
    - page_obj: The Page object for the current page.
    """
    items_per_page = request.GET.get('limit', items_per_page)
    paginator = Paginator(queryset, items_per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return page_obj
