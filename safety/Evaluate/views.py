import json
from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction


from .models import EvaluationQuestion, EvaluationAnswer, BaseReportEvaluation, QuestionSet
from safety.Report.models.reports import BaseReport


def evaluate_main(request, report_id, question_id=1):
    report = BaseReport.objects.get(id=report_id)
    question_set = QuestionSet.objects.get(id=question_id)  # Assuming a default question set for simplicity
    context = {"report": report, "question_set": question_set}
    return render(request, 'Evaluate/evaluate-main.html', context)


@require_POST
def get_current_question(request):
    try:
        data = json.loads(request.body)
        question_id = data['question_id'] 
    except (KeyError, json.JSONDecodeError):
        return JsonResponse({'error': 'Invalid request'}, status=400)

    try:
        question = EvaluationQuestion.objects.get(id=question_id)
    except EvaluationQuestion.DoesNotExist:
        raise Http404

    return JsonResponse({
        'type': 'question',
        'id': question.id,
        'text': question.text,
    })


@require_POST
def get_next_question(request):
    try:
        data = json.loads(request.body)
        question_id = data['question_id']
        answer = data['answer'] 
        print("===> answer:"*10, answer)   
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


@require_POST
def submit_evaluation(request):

    data = json.loads(request.body)
    answers = data.get('answers', [])
    result_id = data.get('result_id')
    question_set_id = data.get('question_set_id')
    report_id = data.get('report_id') 
    print("===> report_id:"*10, report_id)
    print(data)
    with transaction.atomic():
        report_evaluation = BaseReportEvaluation.objects.create(
            question_set_id=question_set_id,
            final_result_id=result_id,
            report_id=report_id,
            evaluator_id=request.user.id
        )

        for idx, entry in enumerate(answers):
            question_id = entry['questionID']
            answer_value = entry['answer']

            try:
                question = EvaluationQuestion.objects.get(id = question_id)
            except EvaluationQuestion.DoesNotExist:
                continue  # Skip bad data

            EvaluationAnswer.objects.create(
                evaluation=report_evaluation,
                question=question,
                answer=answer_value,
                order=idx + 1
            )

        return JsonResponse({'status': 'ok'})
    
    return JsonResponse({'status': 'error'}, status=400)

# path('api/submit-evaluation/', views.submit_evaluation, name='submit_evaluation')

