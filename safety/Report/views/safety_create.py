from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from ..forms.reports import BaseReportForm, GroundReportForm, AviationReportForm
from ..forms.attachments import ImageFormSet, RecommendationFormSet, FileFormSet
from ..services.safety_create import perform_create_all
from common.RTAFUser.models import Affiliation

def _get_priority(request):
    if "priority-H" in request.POST: return "H"
    if "priority-M" in request.POST: return "M"
    return "L"


@login_required
def new_report(request):
    if request.method == "GET":
        affiliation = Affiliation.objects.get(id=request.GET.get("affiliation")) if request.GET.get("affiliation") else None
        initial = {
            "affiliation": affiliation,
            "report_type": request.GET.get("report_type", ""),
            "content": affiliation.airviation_content if affiliation and affiliation.airviation_content else "",
        }
        return render(request, "Report/safety-reports/safety-create.new-report.html", {
            "base_form": BaseReportForm(prefix="base_form", initial=initial),
            "image_formset": ImageFormSet(prefix="images"),
            "recommendation_formset": RecommendationFormSet(prefix="recommendations"),
            "file_formset": FileFormSet(prefix="files"),
        })

    base_form = BaseReportForm(request.POST, prefix="base_form")
    image_fs  = ImageFormSet(request.POST, request.FILES, prefix="images")
    rec_fs    = RecommendationFormSet(request.POST, prefix="recommendations")
    file_fs   = FileFormSet(request.POST, request.FILES, prefix="files")

    report_type = request.POST.get("base_form-report_type", "")
    ground_form   = GroundReportForm(request.POST, prefix="ground")    if "G" in report_type else None
    aviation_form = AviationReportForm(request.POST, prefix="aviation") if "A" in report_type else None

    form_valid = (
        base_form.is_valid() and
        image_fs.is_valid() and
        rec_fs.is_valid() and
        file_fs.is_valid() and
        (ground_form.is_valid() if ground_form else True) and
        (aviation_form.is_valid() if aviation_form else True)
    )

    if form_valid and "A" in report_type and not base_form.cleaned_data.get("content"):
        default_airv = getattr(getattr(request.user, "affiliation", None), "airviation_content", None)
    else: # if not form_valid
        messages.error(request, "กรุณาตรวจสอบข้อมูลให้ถูกต้อง")
        return render(request, "Report/safety-reports/safety-create.new-report.html", {
            "base_form": base_form,
            "image_formset": image_fs,
            "recommendation_formset": rec_fs,
            "file_formset": file_fs,
        })
    
    base_form.instance.report_type = report_type

    base_report = perform_create_all(
        base_form, image_fs, rec_fs, file_fs,
        ground_form, aviation_form,
        request, _get_priority(request)
    )

    messages.success(request, f"บันทึกเหตุการณ์ {base_report} เรียบร้อยแล้ว")
    return redirect("report:safety-report.list")


# @login_required
# def create_report(request, mission_type, report_type, affiliation):
#     base_form = BaseReportForm(request.POST, prefix="base_form")
#     ground_form = GroundReportForm(request.post, prefix="ground_form")
#     aviation_form = AviationReportForm(request.post, prefix="aviation_form")

#     image_formset = ImageFormSet(request.POST, request.FILES, prefix='images')
#     recommendation_formset = RecommendationFormSet(request.POST, prefix='recommendations')
#     file_formset = FileFormSet(request.POST, request.FILES, prefix='files')


#     if request.method == 'POST':
#         base_form = BaseReportForm(request.POST, prefix="base_form")
#         image_formset = ImageFormSet(request.POST, request.FILES, prefix='images')
#         recommendation_formset = RecommendationFormSet(request.POST, prefix='recommendations')
#         file_formset = FileFormSet(request.POST, request.FILES, prefix='files')
        
#         if "priority-H" in request.POST:
#             priority = "H"
#         elif "priority-M" in request.POST:
#             priority = "M"
#         else:
#             priority = "L"

#         forms_validate = [base_form.is_valid(), image_formset.is_valid(), recommendation_formset.is_valid(), file_formset.is_valid()]
#         if all(forms_validate):        
#             success, forms, base_report = create_new_report(base_form, image_formset, recommendation_formset, file_formset, request.user, priority)
#             base_form, image_formset, recommendation_formset, file_formset = forms
#         if success:
            
#             messages.info(request, f"บันทึกข้อมูลเหตุการณ์ {base_report} เรียบร้อยแล้ว")
#             return redirect('report:safety-report.list')

#     else:  # GET
#         initial_data = {'affiliation': request.user.affiliation}
#         if request.user.affiliation.airviation_content:
#             initial_data['content'] = request.user.affiliation.airviation_content

#         base_form = BaseReportForm(prefix="base_form", initial=initial_data)
#         image_formset = ImageFormSet(prefix='images')
#         recommendation_formset = RecommendationFormSet(prefix='recommendations')
#         file_formset = FileFormSet(prefix='files')

#     return render(request, 'Report/safety-reports/safety-create.new-report.html', {
#         'base_form': base_form,
#         'image_formset': image_formset,
#         'recommendation_formset': recommendation_formset,
#         'file_formset': file_formset,
#     })