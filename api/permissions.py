from rest_framework import permissions


class AllowedToCreate(permissions.BasePermission):
    message = "Not an allowed for creation."

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated
