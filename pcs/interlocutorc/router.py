from rest_framework.routers import DefaultRouter
from interlocutorc.views import ApiPrueba,ApiFacturas

router_posts=DefaultRouter()

router_posts.register(prefix='post',basename='post',viewset=ApiPrueba)
router_posts.register(prefix='facturas',basename='facturas',viewset=ApiFacturas)