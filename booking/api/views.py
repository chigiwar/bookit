from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..models import Book, Flight, Airline, Airport
from .serializers import BookSerializer, FlightSerializer, AirlineSerializer
from .permissions import IsAdmin, BookPermissions, FlightPermissions, AirlinePermissions


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, BookPermissions]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(owner__id=self.request.user.id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        book_data = request.data.dict()
        if request.user.group == 'user':
            book_data['owner_id'] = request.user.id
        new_book = self.get_queryset().create(**book_data)
        new_book_serialized = self.get_serializer(new_book)
        headers = self.get_success_headers(new_book_serialized.data)
        return Response(new_book_serialized.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        book_id = kwargs.get('pk')
        print(book_id)
        book = get_object_or_404(Book, pk=book_id)
        book.deleted = True
        book.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsAuthenticated, FlightPermissions]

    def list(self, request, *args, **kwargs):
        if not self.request.user.vip or self.request.user.group in {'admin', 'manager'}:
            queryset = self.filter_queryset(self.get_queryset()).filter(airline__vip=False)
        else:
            queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AirlineView(viewsets.ModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    permission_classes = [IsAuthenticated, AirlinePermissions]

    def list(self, request, *args, **kwargs):
        if not self.request.user.vip or self.request.user.group in {'admin', 'manager'}:
            queryset = self.filter_queryset(self.get_queryset()).filter(vip=False)
        else:
            queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AirportView(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]
