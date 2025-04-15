from datetime import date
import math
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from LittlelemonAPI.models import Cart, MenuItem, Category, Order, OrderItem
from LittlelemonAPI.serializers import CartSerializer, MenuItemSerializer, CategorySerializer, ManagerListSerializer, OrderDetailSerializer, OrderSaveSerializer, OrderSerializer, RemoveFromCartSerializer, AddToCartSerializer


# Secure
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User, Group

class IsManagerOrAdminUser(IsAdminUser):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name='Manager').exists()


class IsDeliveryCrew(IsAdminUser):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name='DeliveryCrew').exists()


# Create your views here.
class CategoryView(generics.ListCreateAPIView):
     throttle_classes = [AnonRateThrottle, UserRateThrottle]
     queryset = Category.objects.all()
     serializer_class = CategorySerializer
     ordering_fields = ['slug','title']
     search_fields = ['title']
     permission_classes = [IsAuthenticated, IsManagerOrAdminUser]


class MenuItemsView(generics.ListCreateAPIView):
     throttle_classes = [AnonRateThrottle, UserRateThrottle]
     queryset = MenuItem.objects.select_related('category').all()
     serializer_class = MenuItemSerializer
     ordering_fields = ['price', 'featured']
     filters_fields = ['price', 'featured']
     search_fields = ['title', 'category__title']

     # Read only for anon user
     def get_permissions(self):
          permission_classes = []
          if self.request.method != 'GET':
               permission_classes = [IsAuthenticated, IsAdminUser]
          return [permission() for permission in permission_classes]


class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
     throttle_classes = [AnonRateThrottle, UserRateThrottle]
     queryset = MenuItem.objects.all()
     serializer_class = MenuItemSerializer

     # Read only for anon user
     def get_permissions(self):
          permission_classes = []
          if self.request.method != 'GET':
               # permission_classes = [IsAuthenticated, IsAdminUser]
               permission_classes = [IsAuthenticated, IsManagerOrAdminUser]
          return [permission() for permission in permission_classes]


class SingleCategoryView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
     throttle_classes = [AnonRateThrottle, UserRateThrottle]
     queryset = Category.objects.all()
     serializer_class = CategorySerializer
     # permission_classes = [IsAdminUser]
     permission_classes = [IsManagerOrAdminUser]


# MANAGERS CREATE
class ManagerView(generics.ListCreateAPIView):
     throttle_classes = [AnonRateThrottle, UserRateThrottle]
     queryset = User.objects.filter(groups__name="Manager")
     serializer_class = ManagerListSerializer
     permission_classes = [IsAuthenticated, IsManagerOrAdminUser ]
     def post(self, request):
          username = request.data['username']
          if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name='Manager')
            managers.user_set.add(user)
            return JsonResponse(status=201, data={'message': 'user added to the manager group'})


# DELEVERY CREW  CREATE
class DeliveryCrewView(generics.ListCreateAPIView):
     throttle_classes = [AnonRateThrottle, UserRateThrottle]
     queryset = User.objects.filter(groups__name="DeliveryCrew")
     serializer_class = ManagerListSerializer
     permission_classes = [IsAuthenticated, IsManagerOrAdminUser ]
     def post(self, request):
          username = request.data['username']
          if username:
            user = get_object_or_404(User, username=username)
            delivery_crew = Group.objects.get(name='Manager')
            delivery_crew.user_set.add(user)
            return JsonResponse(status=201, data={'message': 'user added to the DeliveryCrew group'})


# MANAGERS REMOVE
class ManagerDelView(generics.DestroyAPIView):
     throttle_classes = [AnonRateThrottle, UserRateThrottle]
     queryset = User.objects.filter(groups__name="Manager")
     serializer_class = ManagerListSerializer
     permission_classes = [IsAuthenticated, IsAdminUser]
     def delete(self, request, *arg,**kwargs):
          user_id = self.kwargs['pk']
          user = get_object_or_404(User, pk=user_id)
          managers = Group.objects.get(name='Manager')
          managers.user_set.remove(user)
          return JsonResponse(status=200, data={'message': 'User removed to Manager group'})


# DELEVERY CREW  REMOVE
class DeliveryCrewDelView(generics.DestroyAPIView):
     throttle_classes = [AnonRateThrottle, UserRateThrottle]
     queryset = User.objects.filter(groups__name="DeliveryCrew")
     serializer_class = ManagerListSerializer
     permission_classes = [IsAuthenticated, IsAdminUser]
     def delete(self, request, *arg,**kwargs):
          user_id = self.kwargs['pk']
          user = get_object_or_404(User, pk=user_id)
          managers = Group.objects.get(name='DeliveryCrew')
          managers.user_set.remove(user)
          return JsonResponse(status=200, data={'message': 'User removed to DeliveryCrew group'})


# CART
class CartView(generics.ListCreateAPIView):
     throttle_classes = [AnonRateThrottle, UserRateThrottle]
     serializer_class = CartSerializer
     permission_classes = [IsAuthenticated]
     def get_queryset(self, *args, **kwargs):
          return Cart.objects.filter(user=self.request.user)

     def post(self, request, *args, **kwargs):
          serializer_item = AddToCartSerializer(data=request.data)
          serializer_item.is_valid(raise_exception=True)
          item_id = request.data['menuitem']
          quantity = request.data['quantity']
          item = get_object_or_404(MenuItem, id=item_id)
          price = int(quantity) * item.price
          try:
               Cart.objects.create(
                    user=request.user,
                    quantity=quantity,
                    unit_price=item.price,
                    price=price, menuitem_id=item_id
               )
          except Exception as e:
               return JsonResponse(status=409, data={'message': 'item already exist !'})
          return JsonResponse(status=201, data={'message': 'item added to cart !'})

     def delete(self, request, *args, **kwargs):
          if 'menuitem' in request.data:
               serializer_item = RemoveFromCartSerializer(data=request.data)
               serializer_item.is_valid(raise_exception=True)
               menuitem = request.data['menuitem']
               cart = get_object_or_404(Cart, user=request.user, menuitem=menuitem)
               cart.delete()
               return JsonResponse(status=200, data={'message': 'item removed from cart !'})
          else:
            Cart.objects.filter(user=request.user).delete()
            return JsonResponse(status=201, data={'message': 'Cart cleared !'})


# ORDER
class OrderView(generics.ListCreateAPIView):
     throttle_classes = [AnonRateThrottle, UserRateThrottle]
     serializer_class = OrderSerializer
     def get_queryset(self, *args, **kwargs):
          if IsManagerOrAdminUser:
               query = Order.objects.all()
          elif self.request.user.groups.filter(name='DeliveryCrew').exists():
               query = Order.objects.filter(delivery_crew = self.request.user)
          else:
               query = Order.objects.filter(user=self.request.user)
          return query

     def get_permissions(self):
          permission_classes = []
          if self.request.method == 'GET' or self.request.method == 'POST':
               permission_classes = [IsAuthenticated]
          return [permission() for permission in permission_classes]

     def post(self, request, *args, **kwargs):
          cart = Cart.object.filter(user=request.user)
          items_count=cart.values_list()
          if len(items_count) == 0:
               return HttpResponseBadRequest()
          total = math.fsum([float(items_count[-1]) for items_count in items_count ])
          order = Order.objects.create(user=request.user, status=False, total=total, date=date.today())
          for item in cart.values():
               menuitem = get_object_or_404(MenuItem, id=item['menuitem_id'])
               orderitem= OrderItem.objects.create(order=order, menuitem=menuitem, quantity=item['quantity'])
               orderitem.save()
          cart.delete()
          return JsonResponse(status=201, data={'message':'order placed !'})


class DetailOrderView(generics.ListCreateAPIView):
     throttle_classes = [AnonRateThrottle, UserRateThrottle]
     serializer_class = OrderDetailSerializer
     def get_queryset(self, *args, **kwargs):
          query = OrderItem.objects.filter(order_id=self.kwargs['pk'])
          return query

     def get_permissions(self):
          order = Order.objects.get(pk=self.kwargs['pk'])
          if self.request.user == order.user and self.request.method == 'GET' :
               permission_classes = [IsAuthenticated]
          elif self.request.method == 'PUT' or self.request.method == 'DELETE' or 'PATCH':
               permission_classes = [IsAuthenticated]
          else:
               permission_classes = [IsAuthenticated, IsManagerOrAdminUser, IsDeliveryCrew]
          return [permission() for permission in permission_classes]

     def patch(self, request, *args, **kwargs):
          order = Order.objects.get(pk=self.kwargs['pk'])
          order.status = not order.status
          order.save()
          return JsonResponse(status=200, data={'message':'order updated !'})

     def put(self, request, *args, **kwargs):
          serializer_item = OrderSaveSerializer(data=request.data)
          serializer_item.is_valid(raise_exception=True)
          order_pk = self.kwargs['pk']
          crew_pk = request.data['delivery_crew']
          order = get_object_or_404(Order, pk=order_pk)
          crew = get_object_or_404(User, pk=crew_pk)
          order.delivery_crew = crew
          order.save()
          return JsonResponse(status=200, data={'message': str(crew.username)+ ' assigned to ' +str(order.id)})

     def patch(self, request, *args, **kwargs):
          order = Order.objects.get(pk=self.kwargs['pk'])
          order_id = str(order.id)
          order.delete()
          return JsonResponse(status=200, data={'message':'order {} deleted !'.format(order_id)})
