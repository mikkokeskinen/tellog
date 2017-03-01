from django.conf.urls import url

from . import views

app_name = 'transcript'

urlpatterns = [
    url(r'^record_telegram$', views.record_telegram, name="record_telegram"),
    url(r'^message/search$', views.message_search, name="message_search"),
]
