from rest_framework import permissions


class CommentaryPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET', 'POST']:
            return True
        return bool(request.user and request.user.is_authenticated)
