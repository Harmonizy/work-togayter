# evaluate/templatetags/evaluate_tags.py
from django import template

from ..models import QuestionSet

register = template.Library()

@register.inclusion_tag('evaluate/includes/select_questionset.html', takes_context=True)
def select_questionset_for_evaluation(context, report_id):
    question_sets = QuestionSet.objects.select_related('start_question').all()
    return {
        'question_sets': question_sets,
        'report_id': report_id,
    }
