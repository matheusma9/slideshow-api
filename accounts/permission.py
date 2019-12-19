from rest_framework.permissions import BasePermission

class IsOwnerOrCreateOnly(BasePermission):
    """
    The request is authenticated as a user, or is a create-only request.
    """

    def has_object_permission(self, request, view, obj):
        return request.method == 'POST' or obj == request.user or request.user.is_staff