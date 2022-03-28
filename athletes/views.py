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
        
        requestName = request.data.get('Name')
        requestSex = request.data.get('Sex') #Campo Sex da requisição
        requestAge = request.data.get('Age')
        requestHeight = request.data.get('Height')
        requestWeight = request.data.get('Weight')
        requestTeam = request.data.get('Team')
        requestNOC = request.data.get('NOC')
        requestGames = request.data.get('Games')
        requestYear = request.data.get('Year') #Campo Year da Requisição
        requestSeason = request.data.get('Season') #Campo Season da Requisição
        requestCity = request.data.get('City')
        requestSport = request.data.get('Sport')
        requestEvent = request.data.get('Event')
        requestMedal = request.data.get('Medal') #Campo Medal da requisição

        #Validação adicional de alguns campos
        if (requestSex != 'M' and requestSex != 'F'): #Checar se o sexo inserido é valido dentre as opções, se algo diferente for inserido retorna exceção
            return Response("Sexo inserido inválido, necessário que o sexo inserido seja Masculino (M) ou Feminino(F)", 
            status = status.HTTP_400_BAD_REQUEST)
        elif (requestMedal != 'Gold' and requestMedal != 'Silver' and Medal != 'Bronze' and Medal != 'NA'): #Checar se a informação da medalha é válida dentre as opções
            return Response("Tipo de Medalha inserida inválida, necessário que o sexo inserido seja Ouro(Gold), Prata(Silver) ou Bronze(Bronze)", 
            status = status.HTTP_400_BAD_REQUEST)
        elif (requestSeason != 'Summer' and requestSeason != 'Winter'): #Checar se a informação da estação dos jogos é válida, os jogos só se passam no verão/inverno
            return Response("Estação dos Jogos inserida inválida, necessário que seja Verão(Summer) ou Inverno(Winter)", 
            status = status.HTTP_400_BAD_REQUEST)
        elif (int(requestYear) > 2022): #Checar se o ano é válido, só aceitar anos que sejam do ano atual para trás
            return Response("Ano inserido inválido, necessário que o ano inserido seja menor ou igual ao ano atual (2022)", 
            status = status.HTTP_400_BAD_REQUEST)

        #Verificação se este atleta já se encontra na base de dados 
        #Checa campo por campo, se existe algum atleta com exatamente as mesmas informações
        athletes = Athletes.objects.filter(Name = requestName, Sex = requestSex, Age = requestAge,
        Height = requestHeight, Weight = requestWeight, Team = requestTeam, NOC = requestNOC, Games = requestGames,
        Year = requestYear, Season = requestSeason, City = requestCity, Sport = requestSport,
        Event = requestEvent, Medal = requestMedal )
        if (athletes.count() != 0): #O count serve para checar se retornou algum atleta com estas informações se for é porque nenhum atleta foi inserido com estas infos ainda
            return Response("Atleta com estas informações já está inserido na base de dados", 
            status = status.HTTP_400_BAD_REQUEST)

           
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




