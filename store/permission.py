from rest_framework import permissions
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
