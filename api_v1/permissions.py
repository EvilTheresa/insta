from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class IsAuthenticatedToEdit(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['create', 'like', 'unlike']:
            return request.user and request.user.is_authenticated
        return True
