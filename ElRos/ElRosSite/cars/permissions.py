from rest_framework import permissions


class CommentaryPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in ['GET', 'POST']:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated and
                    obj.email == request.user.email)
