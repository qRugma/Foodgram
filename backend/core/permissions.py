from rest_framework import permissions


class UserOrReadAnother(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            (request.path[-3:] == 'me/' and request.user.is_authenticated)
            or request.path[-3:] != 'me/'
        )
