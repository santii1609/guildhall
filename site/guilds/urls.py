from django.urls import path

from . import views

app_name = 'guilds'


urlpatterns = [
    # ex: /polls/
    path('', views.IndexView.as_view(), name='index'),
    # ex: /guilds/5/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # ex: /guilds/5/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # ex: /guilds/5/vote/
    path('<int:guild_id>/vote/', views.vote, name='vote'),
]
