from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""
        # if method is GET, then always true
        if request.method in permissions.SAFE_METHODS:
            return True

        # if method is other(PUT, PATCH) then only when current user is same as requested user
        return obj.id == request.user.id


class UpdateOwnFeedItem(permissions.BasePermission):
    """Allow users to edit own feed item"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own feed item"""
        # if method is GET, then always true
        if request.method in permissions.SAFE_METHODS:
            return True

        # if method is other(PUT, PATCH) then only when current user is same as requested user
        return obj.user_profile.id == request.user.id
