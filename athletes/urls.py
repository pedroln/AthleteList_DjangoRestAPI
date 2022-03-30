from django.urls import path 
from athletes import views

urlpatterns = [
    path('postAthlete', views.AthletePost, name = 'Send New Athlete'),
    path('updateAthlete/<str:pk>', views.AthletePut, name = 'Update Athlete'),
    path('deleteAthlete/<str:pk>', views.AthleteDelete, name = 'Delete Athlete'),
    path('getAthletes', views.AthletesListView.as_view(), name = "Athletes List"),
    path('uploadAthletes', views.UploadAthletesView.as_view(), name='Upload Athletes CSV'),
    path('uploadRegions', views.UploadRegionsView.as_view(), name='Upload Athletes Regions CSV')
    ]