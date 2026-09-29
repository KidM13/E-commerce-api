from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
class IsCartOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user== request.user
class IsCartItemOwner(permissions.BasePermission):
    """Protects CartItem objects, checking through their cart"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.cart.user == request.user

class IsAdminOrReadOnly(BasePermission):
    """For Product and Category — anyone can read, only staff can write"""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
class IsOrderOwnerOrStaffReadOnly(BasePermission):
    """For Order — owner or staff can view; no direct edits through the standard endpoints"""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return obj.user == request.user or request.user.is_staff
        return False   # blocks PUT/PATCH/DELETE entirely through the normal ViewSet actions

