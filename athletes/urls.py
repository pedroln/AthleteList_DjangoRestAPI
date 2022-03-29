from django.urls import path 
from athletes import views

urlpatterns = [
    path('getAthletes', views.AthleteList, name = 'List'),
    path('postAthlete', views.AthletePost, name = 'Send New Athlete'),
    path('updateAthlete/<str:pk>', views.AthletePut, name = 'Update Athlete'),
    path('deleteAthlete/<str:pk>', views.AthleteDelete, name = 'Delete Athlete'),
    path('filterAthletes', views.AthletesListView.as_view(), name = "Filter Athletes"),
    path('uploadAthletes', views.UploadFileView.as_view(), name='upload-file')

    ]