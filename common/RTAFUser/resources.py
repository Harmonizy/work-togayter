from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import RTAFUser, Rank, Affiliation


class RTAFUserResource(resources.ModelResource):
    rank = fields.Field(
        column_name="ยศ",
        attribute="rank",
        widget=ForeignKeyWidget(Rank, "short_name")
    )

    affiliation = fields.Field(
        column_name="สังกัด",
        attribute="affiliation",
        widget=ForeignKeyWidget(Affiliation, "short_name")
    )

    work_affiliation = fields.Field(
        column_name="ปฏิบัติงานที่",
        attribute="work_affiliation",
        widget=ForeignKeyWidget(Affiliation, "short_name")
    )

    class Meta:
        model = RTAFUser
        fields = (
            "id",
            "af_id",
            "person_id",
            "rank",
            "first_name",
            "last_name",
            "position",
            "affiliation",
            "work_affiliation",
            "is_active",
        )
