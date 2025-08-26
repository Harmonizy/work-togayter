from safety.Report.forms.reports import AviationReportForm, GroundReportForm, SafetyReportForm

detail_form_dict = {
    'G': (GroundReportForm, "รายงานภาคพื้น"),
    'A': (AviationReportForm, "รายงานภาคอากาศ"),
    'S': (SafetyReportForm, "รายงานนิรภัยอุบัติการณ์")
}
