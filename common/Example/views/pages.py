from random import randint

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from ..forms import FeedbackForm

feedback_data = {
    1: {
        "name": "Alice Thompson",
        "email": "alice.thompson@example.com",
        "message": "Great service! I really enjoyed the experience."
    },
    2: {
        "name": "Brian Lee",
        "email": "brian.lee@example.net",
        "message": "There was a minor issue with the form layout on mobile."
    },
    3: {
        "name": "Carla Mendes",
        "email": "carla.m@example.org",
        "message": "Everything went smoothly, thank you!"
    },
    4: {
        "name": "Daniel Wu",
        "email": "daniel.wu@example.com",
        "message": "I’d like to suggest adding a dark mode option."
    },
    5: {
        "name": "Emma Clark",
        "email": "emma.c@example.com",
        "message": "The support team was very helpful and fast."
    }
}


def feedback_view(request):
    
    if request.method == 'POST':
        if 'HX-Request' in request.headers:
            form = FeedbackForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                response = JsonResponse({"status" : "success", "message" : "Feedback received successfully!" })
                response["HX-Response-Target"] = "none"
                # response["HX-Response-Swap"] = "outerHTML"
                response["HX-Trigger"] = "dataReceived"
                # {"dataReceived" : {"level" : "info", "message" : "Here Is A Message"}}                
                return response
            else:
                return render(request, 'Example/feedback_form.html#feedback-form-modal', {'form': form})
    else:
        data = feedback_data.get(randint(1, 5))
        form = FeedbackForm(initial=data)
        info = feedback_data.get(randint(1, 5))
        if 'HX-Request' in request.headers:
            return render(request, 'Example/feedback_form.html#feedback-form-modal', {'form': form, 'info': info})
        return render(request, 'Example/feedback_form.html', {'form': form})