from django.urls import path 
from athletes import views

urlpatterns = [
    path('getAthletes', views.AthleteList, name = 'List'),
    path('postAthletes', views.AthletePost, name = 'Send New Athlete'),
    path('putAthletes/<str:pk>', views.AthletePut, name = 'Update Athlete'),
    path('deleteAthletes/<str:pk>', views.AthleteDelete, name = 'Delete Athlete'),
    path('filterAthletes', views.AthletesListView.as_view(), name = "Filter Athletes"),
    path('uploadAthletes', views.UploadAthletesView.as_view(), name='Upload Athletes CSV'),
    path('uploadRegions', views.UploadRegionsView.as_view(), name='Upload Athletes Regions CSV')
    ]