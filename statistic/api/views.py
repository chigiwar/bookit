from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from account.models import User
from booking.models import Book, Airline
from booking.api.permissions import IsAdmin
from django.db.models import Count
from .serializers import UserStatSerializer, AirlineStatSerializer


class UserBookStatView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = UserStatSerializer

    def retrieve(self, request, *args, **kwargs):
        user_id = self.kwargs['pk']
        book_count = Book.objects.filter(owner__id=user_id).count()
        return Response({'user_id': user_id, 'book_count': book_count},
                        status=200,
                        content_type='application/javascript')

    def prepare_filter_query(self):
        query = {}
        vip = self.request.query_params.get('vip', None)
        month = self.request.query_params.get('month', None)
        year = self.request.query_params.get('year', None)
        airline_id = self.request.query_params.get('airline', None)
        if vip is not None:
            query['owner_book__flight__airline__vip'] = vip
        if airline_id is not None:
            query['owner_book__flight__airline__id'] = airline_id
        for period_name, period in ('month', month), ('year', year):
            if period:
                query[f'owner_book__flight__takeoff_time__{period_name}'] = period
        return query

    def list(self, request, *args, **kwargs):
        filter_query = self.prepare_filter_query()
        queryset = User.objects.filter(**filter_query).annotate(count_books=Count('owner_book'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AirlineBookStatView(viewsets.ReadOnlyModelViewSet):
    queryset = Airline.objects.all()
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = AirlineStatSerializer

    def prepare_filter_query(self):
        query = {'flight_airline__booked_flight__deleted': False}
        vip = self.request.query_params.get('vip', False)
        month = self.request.query_params.get('month', None)
        year = self.request.query_params.get('year', None)
        user_id = self.request.query_params.get('id', None)
        deleted = self.request.query_params.get('deleted', None)
        query['vip'] = vip
        if user_id:
            query[f'flight_airline__booked_flight__owner_book'] = user_id
        if deleted:
            query[f'flight_airline__booked_flight__deleted'] = True
        for period_name, period in ('month', month), ('year', year):
            if period:
                query[
                    f'flight_airline__takeoff_time__{period_name}'] = period
        return query

    def list(self, request, *args, **kwargs):
        filter_query = self.prepare_filter_query()
        queryset = Airline.objects.filter(**filter_query).annotate(
            count_books=Count('flight_airline__booked_flight'))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
