from django.db.models import Q
import rules

# --- define conditions as tuple (predicate, Q) ---
affiliation_condition = (
    lambda user, doc: user.affiliation == doc.recorder.affiliation,
    lambda user: Q(recorder__affiliation=user.affiliation),
)

rtaf_admin_condition = (
    lambda user, doc: True,
    lambda user: Q(),    
)

can_create_report = (
    lambda user, obj=None: user.has_perm("safety.add_report"),
    lambda user: Q(),  # สามารถดูทุก report ที่ตัวเองสร้าง
)

# 2. Can view risk register
can_view_hazard_log = (
    lambda user, obj=None: user.has_perm("safety.view_hazardlog"),
    lambda user: Q(type="hazard"),  # filter เฉพาะ hazard
)

# 3. Can perform risk assessment
can_risk_assess = (
    lambda user, obj=None: user.has_perm("safety.assess_risk"),
    lambda user: Q(risk_status="pending"),  # เฉพาะที่ยังไม่ประเมิน
)

# 4. Can manage CAP (create/edit/close)
can_manage_cap = (
    lambda user, obj=None: user.has_perm("safety.manage_cap"),
    lambda user: Q(cap_status__in=["open", "draft"]),
)

# 5. Can verify CAP
can_verify_cap = (
    lambda user, obj=None: user.has_perm("safety.verify_cap"),
    lambda user: Q(cap_status="submitted"),
)

# 6. Can access investigation module
can_access_investigation = (
    lambda user, obj=None: user.has_perm("safety.access_investigation"),
    lambda user: Q(module="investigation"),
)

# 7. Can manage evidence in oversight case
can_manage_evidence = (
    lambda user, obj=None: user.has_perm("safety.manage_evidence"),
    lambda user: Q(case_type="oversight"),
)



# --- register rules ---
affiliation_condition_rule = rules.predicate(affiliation_condition[0])
rtaf_admin_condition_rule = rules.predicate(rtaf_admin_condition[0])

rules.add_perm('report.can_view', affiliation_condition_rule)
# --- Register permissions ---
rules.add_perm("safety.add_report", can_create_report[0])
rules.add_perm("safety.view_hazardlog", can_view_hazard_log[0])
rules.add_perm("safety.assess_risk", can_risk_assess[0])
rules.add_perm("safety.manage_cap", can_manage_cap[0])
rules.add_perm("safety.verify_cap", can_verify_cap[0])
rules.add_perm("safety.access_investigation", can_access_investigation[0])
rules.add_perm("safety.manage_evidence", can_manage_evidence[0])

# --- combined Q filter for queryset ---
q_condition = {}
q_condition['report.can_view'] = lambda user: affiliation_condition[1](user)

# # ============== Examples ============================================
# office_condition = (
#     lambda user, doc: doc.office == user.office,
#     lambda user: Q(office=user.office),
# )

# user_rank_condition = (
#     lambda user, doc: doc.rank == user.rank,
#     lambda user: Q(rank=user.rank),
# )

# # --- register rules ---
# office_condition_rule = rules.predicate(office_condition[0])
# user_rank_condition_rule = rules.predicate(user_rank_condition[0])

# rules.add_perm('docs.edit_doc', office_condition_rule & user_rank_condition_rule)

# # --- combined Q filter for queryset ---
# q_condition = {}
# q_condition['docs.edit_doc'] = lambda user: office_condition[1](user) & user_rank_condition[1](user)


# ========================================================================
# from django.shortcuts import get_object_or_404, render
# from rules.contrib.views import permission_required
# from .models import Document

# # Decorate your view with rules' permission_required
# @permission_required('docs.edit_doc', fn=lambda request, *args, **kwargs: get_object_or_404(Document, id=kwargs['doc_id']))
# def document_detail(request, doc_id):
#     document = get_object_or_404(Document, id=doc_id)
#     return render(request, "documents/detail.html", {"document": document})


# # ========================================================================

# def document_list(request):
#     documents = Document.objects.filter(q_condition['docs.edit_doc'](request.user))
#     return render(request, "documents/list.html", {"documents": documents})
