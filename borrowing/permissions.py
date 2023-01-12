from rest_framework.permissions import BasePermission


class IsAdminOrReadAndUpdateOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in [
            "GET",
            "HEAD",
            "OPTIONS",
            "POST",
            "PUT",
            "PATCH"
        ]:
            return True

        return bool(request.user and request.user.is_staff)
