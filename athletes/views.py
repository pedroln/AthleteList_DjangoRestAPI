from django.http import HttpResponse
from django.shortcuts import render
from athletes.models import Athletes, Regions
from athletes.serializers import AthleteSerializer, FileUploadSerializer
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
import pandas as pd

class UploadAthletesView(generics.CreateAPIView):
    serializer_class = FileUploadSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        reader = pd.read_csv(file, delimiter = ',')
        athletes = []
        
        for _, row in reader.iterrows():
            new_athlete = Athletes(
                        Name = row['Name'],
                        Sex = row['Sex'],
                        Age = row['Age'],
                        Height = row['Height'],
                        Weight = row['Weight'],
                        Team = row['Team'],
                        NOC = row['NOC'],
                        Games = row['Games'],
                        Year = row['Year'],
                        Season = row['Season'],
                        City = row['City'],
                        Sport = row['Sport'],
                        Event = row['Event'],
                        Medal = row['Medal'],
                       )
            athletes.append(new_athlete)
            if len(athletes) > 10000:
                Athletes.objects.bulk_create(athletes)
                athletes = []
        if(athletes):
            Athletes.objects.bulk_create(athletes)
        return Response({"status": "Atletas adicionados ao banco de dados com sucesso"},
                        status.HTTP_201_CREATED)

class UploadRegionsView(generics.CreateAPIView):
    serializer_class = FileUploadSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        reader = pd.read_csv(file, delimiter = ',')
        
        
        for _, row in reader.iterrows():
            new_region = Regions(
                        NOC = row['NOC'],
                        Region = row['region'],
                        Notes = row['notes']
                       )
           
            new_region.save()
        return Response({"status": "Regi??es adicionadas ao banco de dados com sucesso"},
                        status.HTTP_201_CREATED)

class AthletesListView(ListAPIView):
    queryset = Athletes.objects.all()
    serializer_class = AthleteSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 50
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('id', 'Name', 'Sex', 'Age', 'Height', 'Weight', 'Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal')

@api_view(['POST'])
def AthletePost(request):
    serializer = AthleteSerializer(data = request.data)
    if serializer.is_valid():  
        if(ValidateFields(request)):
            return ValidateFields(request)
        if(CheckRepeatedAthlete(request)):
            return CheckRepeatedAthlete(request)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST) 

@api_view(['PUT'])
def AthletePut(request, pk):
    athleteToUpdate = Athletes.objects.get(id = pk)
    serializer = AthleteSerializer(athleteToUpdate, data = request.data)
    if serializer.is_valid():
        if(ValidateFields(request)):
            return ValidateFields(request)
        if(CheckRepeatedAthlete(request)):
            return CheckRepeatedAthlete(request)
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST) 

@api_view(['DELETE'])
def AthleteDelete(request, pk):
    athleteToDelete = Athletes.objects.get(id = pk)
    athleteToDelete.delete()
    return Response('Apagado', status=status.HTTP_204_NO_CONTENT)

def ValidateFields(request):
    requestSex = request.data.get('Sex') #Campo Sex da requisi????o
    requestYear = request.data.get('Year') #Campo Year da Requisi????o
    requestSeason = request.data.get('Season') #Campo Season da Requisi????o
    requestMedal = request.data.get('Medal') #Campo Medal da requisi????o
    requestNOC = request.data.get('NOC') #Campo NOC da requisi????o
    requestTeam = request.data.get('Team') #Campo Team da requisi????o
    nationality = Regions.objects.filter(NOC = requestNOC)
    region = Regions.objects.filter(Region = requestTeam)

    #Valida????o adicional de alguns campos
    if (requestSex != 'M' and requestSex != 'F'): #Checar se o sexo inserido ?? valido dentre as op????es, se algo diferente for inserido retorna exce????o
        return Response("Sexo inserido inv??lido, necess??rio que o sexo inserido seja Masculino (M) ou Feminino(F)", 
        status = status.HTTP_400_BAD_REQUEST)
    elif (requestMedal != None and requestMedal != 'Gold' and requestMedal != 'Silver' and requestMedal != 'Bronze' and requestMedal != 'nan'): #Checar se a informa????o da medalha ?? v??lida dentre as op????es
        return Response("Tipo de Medalha inserida inv??lida, necess??rio que a medalha inserida seja Ouro(Gold), Prata(Silver) ou Bronze(Bronze) ou Nenhuma Medalha(nan)", 
        status = status.HTTP_400_BAD_REQUEST)
    elif (requestSeason != 'Summer' and requestSeason != 'Winter'): #Checar se a informa????o da esta????o dos jogos ?? v??lida, os jogos s?? se passam no ver??o/inverno
        return Response("Esta????o dos Jogos inserida inv??lida, necess??rio que seja Ver??o(Summer) ou Inverno(Winter)", 
        status = status.HTTP_400_BAD_REQUEST)
    elif (int(requestYear) > 2022): #Checar se o ano ?? v??lido, s?? aceitar anos que sejam do ano atual para tr??s
        return Response("Ano inserido inv??lido, necess??rio que o ano inserido seja menor ou igual ao ano atual (2022)", 
        status = status.HTTP_400_BAD_REQUEST)
    elif (nationality.count() == 0): #Checar se a sigla da nacionalidade existe, ou seja, se ela se encontra no arquivo noc_regions.csv
        return Response("Sigla da nacionalidade inserida inv??lida, para saber qual siglas s??o aceitas na nacionalidade, checar o arquivo noc_regions.csv (campo NOC)", 
        status = status.HTTP_400_BAD_REQUEST)
    elif (region.count() == 0): #Checar se a regi??o do time existe, ou seja, se ela se encontra no arquivo noc_regions.csv
        return Response("Regi??o inserida inv??lida, para saber qual siglas s??o aceitas na nacionalidade, checar o arquivo noc_regions.csv (campo Region)", 
        status = status.HTTP_400_BAD_REQUEST)

def CheckRepeatedAthlete(request):
        requestName = request.data.get('Name') #Campo Name da requisi????o
        requestSex = request.data.get('Sex') #Campo Sex da requisi????o
        requestAge = request.data.get('Age') #Campo Age da requisi????o
        requestHeight = request.data.get('Height') #Campo Height da requisi????o
        requestWeight = request.data.get('Weight') #Campo Weight da requisi????o
        requestTeam = request.data.get('Team') #Campo Team da requisi????o
        requestNOC = request.data.get('NOC') #Campo NOC da requisi????o
        requestGames = request.data.get('Games') #Campo Games da requisi????o
        requestYear = request.data.get('Year') #Campo Year da Requisi????o
        requestSeason = request.data.get('Season') #Campo Season da Requisi????o
        requestCity = request.data.get('City') #Campo City da requisi????o
        requestSport = request.data.get('Sport') #Campo Sport da requisi????o
        requestEvent = request.data.get('Event') #Campo Event da requisi????o
        requestMedal = request.data.get('Medal') #Campo Medal da requisi????o

        #Verifica????o se este atleta j?? se encontra na base de dados 
        #Checa campo por campo, se existe algum atleta com exatamente as mesmas informa????es
        athletes = Athletes.objects.filter(Name = requestName, Sex = requestSex, Age = requestAge,
        Height = requestHeight, Weight = requestWeight, Team = requestTeam, NOC = requestNOC, Games = requestGames,
        Year = requestYear, Season = requestSeason, City = requestCity, Sport = requestSport,
        Event = requestEvent, Medal = requestMedal)
        
        if (athletes.count() != 0): #O count serve para checar se retornou algum atleta com estas informa????es se for 0 ?? porque nenhum atleta foi inserido com estas infos ainda
            return Response("Atleta com estas informa????es j?? est?? inserido na base de dados", 
            status = status.HTTP_400_BAD_REQUEST)



