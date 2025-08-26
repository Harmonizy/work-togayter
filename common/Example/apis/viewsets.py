from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from common.Configurations.models import Config
from .serializers import ConfigSerializer


@api_view(['POST'])
def set_config(request):
    serializer = ConfigSerializer(data=request.data)
    if serializer.is_valid():
        key = serializer.validated_data['key']
        value = serializer.validated_data['value']
        
        config, created = Config.objects.get_or_create(key=key)
        
        config.value = value
        config.save()

        response = "created", status.HTTP_201_CREATED if created else "updated", status.HTTP_200_OK
        return Response({'message': f'Config {response[0]} successfully.'}, status=response[1])
    

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
