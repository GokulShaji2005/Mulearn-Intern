from rest_framework.permissions import BasePermission

from rest_framework.permissions import BasePermission
from rest_framework import permissions
class IsAdminUserRole(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'admin' and
            request.user.is_staff
        )

class IsCompany(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == 'company'
        )
    
class IsOwnerCompany(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.company == request.user
