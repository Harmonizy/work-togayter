from django.contrib.admin.models import LogEntry, CHANGE, ADDITION, DELETION
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from django.http import HttpResponse


def create_log_entry(user, model_instance, action_type):
    content_type = ContentType.objects.get_for_model(model_instance)
    
    LogEntry.objects.create(
        user=user,
        content_type=content_type,
        object_id=model_instance.pk,
        object_repr=str(model_instance),
        action_flag=action_type,
        change_message=f'{action_type} action on {model_instance.__class__.__name__}',
    )

# Example usage:
# def my_view(request):
#     # Example of an action
#     if request.method == "POST":
#         # Assuming you want to create a new instance of YourModel
#         instance = YourModel.objects.create(name="New Item")
        
#         # Log the creation of the new object
#         create_log_entry(request.user, instance, ADDITION)
        
#         return HttpResponse("Created successfully.")
#     return HttpResponse("Something went wrong.")


def log_model_changes(model_instance, original_instance):    
    changes = []
    for field in model_instance._meta.fields:
        field_name = field.name
        old_value = getattr(original_instance, field_name)
        new_value = getattr(model_instance, field_name)

        if old_value != new_value:
            changes.append(f"{field_name.capitalize()} changed from '{old_value}' to '{new_value}'")

    return ", ".join(changes)

# Example usage:
# change_message = log_model_changes(instance, original_instance)

# # Log the changes in the admin log
# create_log_entry(request.user, instance, CHANGE, change_message)