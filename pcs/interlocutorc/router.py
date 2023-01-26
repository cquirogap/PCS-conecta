from rest_framework.routers import DefaultRouter
from interlocutorc.views import ApiPrueba

router_posts=DefaultRouter()

router_posts.register(prefix='post',basename='post',viewset=ApiPrueba)