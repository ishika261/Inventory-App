from rest_framework import permissions
from .models import Event


class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""
        # if method is GET, then always true
        if request.method in permissions.SAFE_METHODS:
            return True

        # if method is other(PUT, PATCH) then only when current user is same as requested user
        return obj.id == request.user.id


# class UpdateOwnFeedItem(permissions.BasePermission):
#     """Allow users to edit own feed item"""

#     def has_object_permission(self, request, view, obj):
#         """Check user is trying to edit their own feed item"""
#         # if method is GET, then always true
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         # if method is other(PUT, PATCH) then only when current user is same as requested user
#         return obj.user_profile.id == request.user.id


class UpdateOwnInventoryItem(permissions.BasePermission):
    """Allow users to edit own Inventory item"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own feed item"""
        # if method is GET, then always true
        if request.method in permissions.SAFE_METHODS:
            return True

        # if method is other(PUT, PATCH) then only when current user is same as requested user
        return obj.owner_club.id == request.user.id


class UpdateOwnEvent(permissions.BasePermission):
    """Allow users to edit own event details"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own feed item"""
        # if method is GET, then always true
        if request.method in permissions.SAFE_METHODS:
            return True

        # if method is other(PUT, PATCH) then only when current user is same as requested user
        return obj.owner_club.id == request.user.id


class UpdateOwnEventInventory(permissions.BasePermission):
    """Allow users to edit own Inventory item"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own feed item"""
        # if method is GET, then always true
        if request.method in permissions.SAFE_METHODS:
            return True

        # if method is other(PUT, PATCH) then only when current user is same as requested user
        event = Event.objects.get(pk=obj.event_id.id)
        return event.owner_club.id == request.user.id
