
from django.urls import path
from .views import *


urlpatterns = [
    path('',home,name="home"),
    path('blog/<str:id>', blog, name="blog"),
    path('blog/like/<str:blog>/<str:user>',doLike,name="doLike"),
    
    # path('triggerLikes',tri,name="triggerLike"),
    # path('triggerDislikes',triggerDisike,name="triggerDislike"),

]
