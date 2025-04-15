from django.urls import path
from LittlelemonAPI import views

urlpatterns = [
    path('menu-items/', views.MenuItemsView.as_view()),
    path('categories/', views.CategoryView.as_view()),

    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('menu-items/categories/<int:pk>', views.SingleCategoryView.as_view()),

    path('groups/manager/users', views.ManagerView.as_view()),
    path('groups/managers/users/<int:pk>', views.ManagerDelView.as_view()),

    path('groups/delivery-crew/users', views.DeliveryCrewView.as_view()),
    path('groups/delivery-crew/users/<int:pk>', views.DeliveryCrewDelView.as_view()),

    path('cart/menu-items/', views.CartView.as_view()),


    path('orders/', views.OrderView.as_view()),
    path('orders/<int:pk>', views.DetailOrderView.as_view()),



]
