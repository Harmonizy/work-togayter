from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import inlineformset_factory

from safety.Report.models.sixA import SixA, Answer, Question
from safety.Report.forms.sixA import SixAForm, AnswerForm, AnswerInlineFormSet


@login_required
def sixA_create_view(request, report_id):
    from safety.Report.models import BaseReport
    report = get_object_or_404(BaseReport, pk=report_id)
    sixa = SixA(report=report, user=request.user)

    # 1. ย้าย query questions มาไว้ตรงนี้ (เพื่อให้รู้นับจำนวนข้อก่อน)
    questions = list(Question.objects.all().order_by("category", "code"))

    # 2. กำหนด extra=len(questions) เพื่อสร้างฟอร์มให้ครบทุกข้อ
    AnswerFormSet = inlineformset_factory(
        SixA,
        Answer,
        form=AnswerForm,
        formset=AnswerInlineFormSet,
        extra=len(questions),
        can_delete=False
    )

    if request.method == "POST":
        # ใน POST ไม่ต้องห่วงเรื่อง extra เพราะมันจะอ่านจากข้อมูลที่ส่งมา
        form = SixAForm(request.POST, request=request, instance=sixa)
        formset = AnswerFormSet(request.POST, instance=sixa)

        if form.is_valid() and formset.is_valid():
            sixa = form.save()
            formset.instance = sixa
            formset.save()
            messages.success(request, "บันทึกแบบประเมิน 6A สำเร็จ")
            return redirect("report:safety-report.detail", pk=report.id)

    else:
        form = SixAForm(instance=sixa, request=request)
        
        initial_data = [{"question": q} for q in questions]

        formset = AnswerFormSet(
            instance=sixa,
            queryset=Answer.objects.none(),
            initial=initial_data
        )

    # สร้าง mapping: question.id -> form
    form_by_qid = {}
    for f in formset.forms:
        # ใช้ logic ที่แก้ไปรอบที่แล้ว (ดึง object แล้วเอา .id)
        q_obj = f.initial.get("question")
        if q_obj:
            form_by_qid[q_obj.id] = f

    grouped_data = []
    current_cat = None
    current_group = None

    for q in questions:
        if q.category != current_cat:
            if current_group:
                grouped_data.append(current_group)

            current_cat = q.category
            current_group = {
                "category_value": q.category,
                "category_label": q.get_category_display(),
                "entries": []
            }

        current_group["entries"].append((q, form_by_qid.get(q.id)))

    if current_group:
        grouped_data.append(current_group)

    return render(
        request,
        "SixA/safety-reports/sixA.html",
        {
            "report": report,
            "form": form,
            "formset": formset,
            "grouped_data": grouped_data,
        },
    )
