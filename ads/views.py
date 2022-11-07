import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from ads.models import Category, Ad, Selection
from ads.permissions import OwnerPermission
from ads.serializers import AdSerializer, SelectionListSerializer, SelectionDetailSerializer, SelectionCreateSerializer, \
    AdCreateSerializer
from users.models import User


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def root(request):
    return JsonResponse({
        "status": "ok"
    })


class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    # def get(self, request, *args, **kwargs):
    #     cat = request.GET.get('cat')
    #     if cat:
    #         self.queryset = Ad.objects.filter(category=cat)
    #     text = request.GET.get('text')
    #     if text:
    #         self.queryset = Ad.objects.filter(name__contains=text)
    #     location = request.GET.get('location')
    #     if location:
    #         self.queryset = Ad.objects.filter(author__locations__name__icontains=location)
    #     price_from = request.GET.get('price_from')
    #     price_to = request.GET.get('price_to')
    #     if price_from:
    #         self.queryset = Ad.objects.filter(price__gte=price_from)
    #     if price_to:
    #         self.queryset = Ad.objects.filter(price__lte=price_to)
    #     return super().get(self, request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated]


@method_decorator(csrf_exempt, name='dispatch')
class AdImageView(UpdateView):
    model = Ad
    fields = ['image']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES['image']
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author.username,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "image": self.object.image.url,
            "category": self.object.category.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateAPIView):
    model = Ad
    serializer_class = AdCreateSerializer


class AdUpdateView(UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer
    permission_classes = [IsAuthenticated, OwnerPermission]


class AdDeleteView(DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdCreateSerializer
    permission_classes = [IsAuthenticated, OwnerPermission]


class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.order_by('name')

        categories = []
        for category in self.object_list:
            categories.append(
                {
                    "id": category.id,
                    "name": category.name,
                }
            )
        return JsonResponse(categories, safe=False)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.id,
            "name": category.name,
        })


@method_decorator(csrf_exempt, name="dispatch")
class CategoryCreateView(CreateView):
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)

        category = Category()
        category.name = category_data["name"]

        category.save()

        return JsonResponse(
            {
                "id": category.id,
                "name": category.name,

            }
        )


@method_decorator(csrf_exempt, name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ["name"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        category_data = json.loads(request.body)
        self.object.name = category_data["name"]
        self.object.save()
        return JsonResponse(
            {
                "id": self.object.id,
                "name": self.object.name,
            }
        )


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({'status': 'ok'}, status=200)


class SelectionListView(ListAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionListSerializer


class SelectionDetailView(RetrieveAPIView):
    queryset = Selection.objects.all()
    serializer_class = SelectionDetailSerializer


class SelectionCreateView(CreateAPIView):
    serializer_class = SelectionCreateSerializer
    queryset = Selection.objects.all()
    permission_classes = [IsAuthenticated]


class SelectionUpdateView(UpdateAPIView):
    serializer_class = SelectionCreateSerializer
    queryset = Selection.objects.all()
    permission_classes = [IsAuthenticated, OwnerPermission]


class SelectionDeleteView(DestroyAPIView):
    serializer_class = SelectionCreateSerializer
    queryset = Selection.objects.all()
    permission_classes = [IsAuthenticated]
