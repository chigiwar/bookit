from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS
from ..models import Flight


SAFE_METHODS = set(SAFE_METHODS)


def is_safe(request):
    return request.method in SAFE_METHODS


def is_own(request, obj):
    return obj.owner.id == request.user.id


def is_admin(request):
    return request.user.group == 'admin'


def is_manager(request):
    return request.user.group == 'manager'


def is_stuff(request):
    return is_admin(request) or is_manager(request)


class IsOwn(BasePermission):

    def has_object_permission(self, request, view, obj):
        return is_own(request, obj)


class IsManager(BasePermission):

    def has_permission(self, request, view):
        return is_manager(request)

    def has_object_permission(self, request, view, obj):
        return is_manager(request)


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return is_admin(request)

    def has_object_permission(self, request, view, obj):
        return is_admin(request)


class IsStuff(BasePermission):

    def has_permission(self, request, view):

        return is_stuff(request)

    def has_object_permission(self, request, view, obj):
        return is_stuff(request)


class BookPermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        if is_stuff(request):
            return True

        if is_safe(request):
            return is_own(request, obj)

        else:
            if is_own(request, obj) and request.user.vip:
                return True

            elif is_own(request, obj) and not obj.flight.airline.vip:
                return True

    def has_permission(self, request, view):
        if is_stuff(request) or request.user.vip:
            return True

        flight = get_object_or_404(Flight, id=request.data.get('flight_id'))
        return not flight.airline.vip


class FlightPermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        if is_stuff(request):
            return True

        if is_safe(request):
            return request.user.vip or not obj.airline.vip

    def has_permission(self, request, view):
        return is_stuff(request) or is_safe(request)


class AirlinePermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.method)
        if request.user.group in {'admin', 'manager'}:
            return True
        if request.method == 'get':
            if obj.airline.vip:
                return request.user.vip
            return True

    def has_permission(self, request, view):
        if request.user.group in {'admin', 'manager'}:
            return True
