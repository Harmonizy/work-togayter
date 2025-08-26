from datetime import datetime

from django.core.cache import cache

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import viewsets, permissions, filters

from ..models import RTAFUser, Affiliation, Rank
from ..serializers import ShortRTAFUserSerializer, RTAFUserSerializer, AffiliationSerializer, RankSerializer


class AuthTokenWithRTAFUser(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.last_login = datetime.now()
        user.save()
        token, _ = Token.objects.get_or_create(user=user)
        user_data = ShortRTAFUserSerializer(user).data
        user_data['token'] = token.key

        return Response(user_data)


class RTAFUserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RTAFUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return RTAFUser.objects.all()
        return RTAFUser.objects.filter(id=self.request.user.id)
    

class AffiliationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Affiliation.objects.all()
    serializer_class = AffiliationSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name', 'short_name']
   
    def get_queryset(self):
        cache_key = 'affiliation_queryset'
        queryset = cache.get(cache_key)
        if not queryset:
            queryset = Affiliation.objects.all()
            cache.set(cache_key, queryset, timeout=60*60*24)
        return queryset
    

class RankViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Rank.objects.all()
    serializer_class = RankSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        cache_key = 'rank_queryset'
        queryset = cache.get(cache_key)
        if not queryset:
            queryset = Rank.objects.all()
            cache.set(cache_key, queryset, timeout=60*60*24)
        return queryset