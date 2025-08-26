from rest_framework import serializers

from .models import RTAFUser, Affiliation, Rank


class AffiliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Affiliation
        fields = ['id', 'hris_code', 'short_name', 'full_name']


class RankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = "__all__"


class GroupMixins:
    def get_groups(self, obj):
        return [g.name for g in obj.groups.all()]


class ShortRTAFUserSerializer(GroupMixins, serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    full_name = serializers.CharField(source='get_full_name',read_only=True)
    groups = serializers.SerializerMethodField()
    work_affiliation = AffiliationSerializer()

    class Meta:
        model = RTAFUser
        fields = ['id', 'full_name', 'work_affiliation', 'groups',]
        

class RTAFUserSerializer(GroupMixins, serializers.ModelSerializer):
    work_affiliation = AffiliationSerializer()
    rank = serializers.CharField(source='rank.short_name')
    groups = serializers.SerializerMethodField()
    full_name = serializers.CharField(source='get_full_name')
    data_status = serializers.CharField(source='get_data_status_display')

    class Meta:
        model = RTAFUser
        fields = [
            'id', 
            # 'person_id', 
            # 'af_id', 
            'full_name', 
            'position', 
            'email', 
            'affiliation', 
            'work_affiliation', 
            'rank', 
            'data_status',
            'login_limited',
            'groups',
        ]


