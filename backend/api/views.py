from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response


def standart_action_POST(request, serializer_class):
    serializer = serializer_class(
        data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def standart_action_DELETE(request, model_class):
    try:
        obj = model_class.objects.get(**request.data)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
