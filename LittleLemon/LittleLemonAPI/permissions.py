from rest_framework import permissions

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
       if request.user.groups.filter(name='Managers').exists():
            return True

class IsDeliveryCrew(permissions.BasePermission):
    def has_permission(self, request, view):
       if request.user.groups.filter(name='Delivery crew').exists():
            return True
       

class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)
