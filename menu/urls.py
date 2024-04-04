from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import *

urlpatterns = [
    path('menu-list/', MenuViews.as_view(), name="Menu-list" ),
    path('menu-item/<int:p_id>/', Menu_Item.as_view(), name="Menu_item"),
    path('menu-list/<int:p_id>/',MenuViews.as_view(), name='update'),

    path('category/',CategoryListAPIView.as_view(), name='category-list'),
    path('category/<str:category>',CategoryListAPIView.as_view(), name='category-list'),

    path('veg-menu-list/<str:veg>/',VegFoodCategoryAPIView.as_view(), name='veg-item'),



]

router = DefaultRouter()
router.register(r'menuitems', MenuItemViewSet)

urlpatterns += [
    path('', include(router.urls)),
]

