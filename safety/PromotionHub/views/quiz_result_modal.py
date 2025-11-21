from django.shortcuts import render
from ..models import Quiz, QuizResult

def quiz_result_modal(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    results = QuizResult.objects.filter(quiz_id=quiz_id).select_related("user")
    return render(request, "PromotionHub/Quiz/components/quiz_result_modal.html", {
        "quiz": quiz,
        "results": results
    })
