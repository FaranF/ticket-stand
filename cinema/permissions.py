from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: #('GET', 'HEAD', 'OPTIONS')
            return True
        return bool(request.user and request.user.is_staff)


# class examplePermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.has_perm('cinema.permissionname')