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
        return Response({"status": "Regiões adicionadas ao banco de dados com sucesso"},
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
    requestSex = request.data.get('Sex') #Campo Sex da requisição
    requestYear = request.data.get('Year') #Campo Year da Requisição
    requestSeason = request.data.get('Season') #Campo Season da Requisição
    requestMedal = request.data.get('Medal') #Campo Medal da requisição
    requestNOC = request.data.get('NOC') #Campo NOC da requisição
    requestTeam = request.data.get('Team') #Campo Team da requisição
    nationality = Regions.objects.filter(NOC = requestNOC)
    region = Regions.objects.filter(Region = requestTeam)

    #Validação adicional de alguns campos
    if (requestSex != 'M' and requestSex != 'F'): #Checar se o sexo inserido é valido dentre as opções, se algo diferente for inserido retorna exceção
        return Response("Sexo inserido inválido, necessário que o sexo inserido seja Masculino (M) ou Feminino(F)", 
        status = status.HTTP_400_BAD_REQUEST)
    elif (requestMedal != None and requestMedal != 'Gold' and requestMedal != 'Silver' and requestMedal != 'Bronze' and requestMedal != 'nan'): #Checar se a informação da medalha é válida dentre as opções
        return Response("Tipo de Medalha inserida inválida, necessário que a medalha inserida seja Ouro(Gold), Prata(Silver) ou Bronze(Bronze) ou Nenhuma Medalha(nan)", 
        status = status.HTTP_400_BAD_REQUEST)
    elif (requestSeason != 'Summer' and requestSeason != 'Winter'): #Checar se a informação da estação dos jogos é válida, os jogos só se passam no verão/inverno
        return Response("Estação dos Jogos inserida inválida, necessário que seja Verão(Summer) ou Inverno(Winter)", 
        status = status.HTTP_400_BAD_REQUEST)
    elif (int(requestYear) > 2022): #Checar se o ano é válido, só aceitar anos que sejam do ano atual para trás
        return Response("Ano inserido inválido, necessário que o ano inserido seja menor ou igual ao ano atual (2022)", 
        status = status.HTTP_400_BAD_REQUEST)
    elif (nationality.count() == 0): #Checar se a sigla da nacionalidade existe, ou seja, se ela se encontra no arquivo noc_regions.csv
        return Response("Sigla da nacionalidade inserida inválida, para saber qual siglas são aceitas na nacionalidade, checar o arquivo noc_regions.csv (campo NOC)", 
        status = status.HTTP_400_BAD_REQUEST)
    elif (region.count() == 0): #Checar se a região do time existe, ou seja, se ela se encontra no arquivo noc_regions.csv
        return Response("Região inserida inválida, para saber qual siglas são aceitas na nacionalidade, checar o arquivo noc_regions.csv (campo Region)", 
        status = status.HTTP_400_BAD_REQUEST)

def CheckRepeatedAthlete(request):
        requestName = request.data.get('Name') #Campo Name da requisição
        requestSex = request.data.get('Sex') #Campo Sex da requisição
        requestAge = request.data.get('Age') #Campo Age da requisição
        requestHeight = request.data.get('Height') #Campo Height da requisição
        requestWeight = request.data.get('Weight') #Campo Weight da requisição
        requestTeam = request.data.get('Team') #Campo Team da requisição
        requestNOC = request.data.get('NOC') #Campo NOC da requisição
        requestGames = request.data.get('Games') #Campo Games da requisição
        requestYear = request.data.get('Year') #Campo Year da Requisição
        requestSeason = request.data.get('Season') #Campo Season da Requisição
        requestCity = request.data.get('City') #Campo City da requisição
        requestSport = request.data.get('Sport') #Campo Sport da requisição
        requestEvent = request.data.get('Event') #Campo Event da requisição
        requestMedal = request.data.get('Medal') #Campo Medal da requisição

        #Verificação se este atleta já se encontra na base de dados 
        #Checa campo por campo, se existe algum atleta com exatamente as mesmas informações
        athletes = Athletes.objects.filter(Name = requestName, Sex = requestSex, Age = requestAge,
        Height = requestHeight, Weight = requestWeight, Team = requestTeam, NOC = requestNOC, Games = requestGames,
        Year = requestYear, Season = requestSeason, City = requestCity, Sport = requestSport,
        Event = requestEvent, Medal = requestMedal)
        
        if (athletes.count() != 0): #O count serve para checar se retornou algum atleta com estas informações se for 0 é porque nenhum atleta foi inserido com estas infos ainda
            return Response("Atleta com estas informações já está inserido na base de dados", 
            status = status.HTTP_400_BAD_REQUEST)



