from django.shortcuts import render
from athletes.models import Athletes
from athletes.serializers import AthleteSerializer
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend

class AthletesListView(ListAPIView):
    queryset = Athletes.objects.all()
    serializer_class = AthleteSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 50
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('Sex', 'Age', 'Height', 'Weight', 'Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal')

@api_view(['GET'])
def AthleteList(request):
    paginator = PageNumberPagination()
    paginator.page_size = 50
    athletes = Athletes.objects.all()
    result_page = paginator.paginate_queryset(athletes, request)
    serializer = AthleteSerializer(result_page, many= True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
def AthletePost(request):
    serializer = AthleteSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST) 

@api_view(['PUT'])
def AthletePut(request, pk):
    athleteToUpdate = Athletes.objects.get(id = pk)
    serializer = AthleteSerializer(athleteToUpdate, data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST) 

@api_view(['DELETE'])
def AthleteDelete(request, pk):
    athleteToDelete = Athletes.objects.get(id = pk)
    athleteToDelete.delete()
    return Response('Apagado')




