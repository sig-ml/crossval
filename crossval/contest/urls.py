from django.conf.urls import url
from contest import views

urlpatterns = [
    url(r'^$', views.contests_home, name='contest_home'),
    url(r'^(?P<pk>\d+)/$', views.contest, name='contest' ),
    url(r'^(?P<pk>\d+)/contract/$', views.contract, name='contract' ),
    url(r'^(?P<pk>\d+)/leaderboard/$', views.contest_lb, name='contest_lb'),
    url(r'^(?P<pk>\d+)/submit/$', views.contest_submit, name='contest_submit'),
    url(r'^resource/(?P<pk>\d+)/$', views.contest_resource, name='contest_resource'),
]
