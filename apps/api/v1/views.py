from rest_framework import generics, views, viewsets, response
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
)

from django_filters.rest_framework import DjangoFilterBackend

from apps.api.v1.serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
)
from apps.core.models import Product


class ProductViewSet(viewsets.ViewSet):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()


class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
    queryset = Product.objects.all()
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    filterset_fields = ('category',)
    search_fields = ('title', 'description')
    ordering_fields = ('id', 'title', 'price')
    pagination_class = PageNumberPagination
    # permission_classes = (IsAuthenticated,)


class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductDetailSerializer
    permission_classes = (IsAdminUser,)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductDetailSerializer
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)


class TestAPIView(views.APIView):

    def get(self, request, *args, **kwargs):
        return response.Response({'data': 'message'})

    def post(self, request, *args, **kwargs):
        return


class TestGenericAPIView(generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

    def get(self, request, *args, **kwargs):
        return response.Response({'data': 'message'})

    def post(self, request, *args, **kwargs):
        return
