import json
from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import EvaluationQuestion


def evaluate_main(request, report_id):
    return render(request, 'Evaluate/evaluate-main.html', {"report_id": report_id})


@require_POST
@csrf_exempt
def get_next_question(request):
    try:
        data = json.loads(request.body)
        question_id = data['question_id']
        answer = data['answer'] 
    except (KeyError, json.JSONDecodeError):
        return JsonResponse({'error': 'Invalid request'}, status=400)

    try:
        question = EvaluationQuestion.objects.get(id=question_id)
    except EvaluationQuestion.DoesNotExist:
        raise Http404

    if answer.upper() == "Y":
        next_question = question.next_if_yes
        result = question.result_if_yes
    else:
        next_question = question.next_if_no
        result = question.result_if_no

    if next_question:
        return JsonResponse({
            'type': 'question',
            'id': next_question.id,
            'text': next_question.text,
        })

    elif result:
        return JsonResponse({
            'type': 'result',
            'id': result.id,
            'result_type': result.type.name     ,                # from ResultTypeChoices
            'name': result.name,
            'english_name': result.english_name,
            'description': result.description,
        })
    else:
        return JsonResponse({'type': 'end', 'message': 'No next question or result.'})


from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import EvaluationQuestion, EvaluationAnswer, BaseReportEvaluation, EvaluationResult, QuestionSet

@csrf_exempt
def submit_evaluation(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    data = json.loads(request.body)
    answers = data.get('answers', [])
    result_id = data.get('result_id')
    question_set_id = data.get('question_set_id')
    report_id = request.GET.get('report_id') 

    # Dummy report association for now
    report_evaluation = BaseReportEvaluation.objects.create(
        question_set_id=question_set_id,
        final_result_id=result_id,
        report_id=report_id,
    )

    for idx, entry in enumerate(answers):
        question_text = entry['question']
        answer_value = entry['answer']

        # Look up question by text (or add question ID to front-end for more precise match)
        try:
            question = EvaluationQuestion.objects.get(text=question_text, question_set_id=question_set_id)
        except EvaluationQuestion.DoesNotExist:
            continue  # Skip bad data

        EvaluationAnswer.objects.create(
            evaluation=report_evaluation,
            question=question,
            answer=answer_value,
            order=idx + 1
        )

    return JsonResponse({'status': 'ok'})

# path('api/submit-evaluation/', views.submit_evaluation, name='submit_evaluation')

