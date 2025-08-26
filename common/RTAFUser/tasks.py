from celery import shared_task

@shared_task
def user_task(username):
    print(f"User task for {username}")
    return f"User task for {username}"
