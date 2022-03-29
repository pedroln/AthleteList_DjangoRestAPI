from django.urls import path 
from athletes import views

urlpatterns = [
    path('getAthletes', views.AthleteList, name = 'List All Athletes'),
    path('getAthletes/<str:pk>', views.AthleteById, name = 'Get Athlete By Id'),
    path('postAthlete', views.AthletePost, name = 'Send New Athlete'),
    path('updateAthlete/<str:pk>', views.AthletePut, name = 'Update Athlete'),
    path('deleteAthlete/<str:pk>', views.AthleteDelete, name = 'Delete Athlete'),
    path('filterAthletes', views.AthletesListView.as_view(), name = "Filter Athletes"),
    path('uploadAthletes', views.UploadAthletesView.as_view(), name='Upload Athletes CSV'),
    path('uploadRegions', views.UploadRegionsView.as_view(), name='Upload Athletes Regions CSV')
    ]