from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request

from library.models import Book, Posts


class IsBookOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request: Request, view, obj: Book) -> bool:
        if request.method in SAFE_METHODS:
            return True

        #          Ksenia   ==   Petya
        return request.user == obj.owner


class IsPostAuthorOrReadOnly(BasePermission):

    def has_object_permission(self, request: Request, view, obj: Posts) -> bool:
        if request.method in SAFE_METHODS:
            return True

        #          Ksenia   ==   Petya
        return request.user == obj.author


class IsStaffAndOwner(BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user == obj.reviewer



class CanGetStatistic(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.has_perm('library.can_get_statistic')
        )
