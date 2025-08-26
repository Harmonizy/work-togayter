from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps

def groups_required(*group_names):
    """
    Decorator to check if the user belongs to any of the required groups.
    Parameters:
        *group_names: Multiple group names that the user must belong to.
    Usage:
        @groups_required('Group1', 'Group2')
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Check if the user is in any of the provided groups
            if not request.user.groups.filter(name__in=group_names).exists():
                return HttpResponseForbidden("You do not have permission to view this page.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def superuser_only(view_func):
    """
    Decorator to check if the user is a superuser.    
    Redirects to login page if the user is not a superuser.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('login')  # Redirect to the login page (or another page)
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view



def check_user_and_args(condition_func):
    """
    A decorator to check if the user passes the given condition.
    The condition is evaluated by calling the condition_func with 
    request.user and view parameters (*args, **kwargs).

    :param condition_func: A function that takes the user and URL parameters, 
                                 and returns True if the user meets the condition.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Check if the user meets the condition by passing request.user and other arguments
            if not condition_func(request.user, *args, **kwargs):
                return HttpResponseForbidden("You do not have permission to access this resource.")

            # If the condition is satisfied, proceed with the view
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


# ในตอนหลังสามารถกำหนดแบบนี้ก็ได้
# admin_or_self_object = check_user_and_args(condition_func=lambda user, obj: user.is_superuser or user == obj.owner)
# 