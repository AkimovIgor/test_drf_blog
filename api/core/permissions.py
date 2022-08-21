from rest_framework.permissions import BasePermission


class AllowedMethods(BasePermission):

    ALLOWED_METHODS = ('GET', 'POST', 'PUT', 'DELETE')

    def has_permission(self, request, view):
        return request.method in self.ALLOWED_METHODS
