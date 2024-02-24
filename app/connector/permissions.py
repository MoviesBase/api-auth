from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class HasAccessPermissions(BasePermission):
    message = 'Permission Denied'

    def has_object_permission(self, request, view, obj):
        # Check if the authenticated user matches the user who created the ECG
        if obj.user != request.user:
            raise PermissionDenied(self.message)
        return True
