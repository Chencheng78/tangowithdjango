from django.conf.urls import url
from rango import  views
#123
urlpatterns =[
	url(r'^$',views.index,name='index'),
]