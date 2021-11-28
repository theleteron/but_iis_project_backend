from rest_framework import permissions

class IsAdministrator(permissions.BasePermission):
    message = "User doesn't have role Administrator!"

    def has_permission(self, request, view):
        return request.user.role == '4'

class IsLibrarian(permissions.BasePermission):
    message = "User doesn't have role Librarian!"

    def has_permission(self, request, view):
        return request.user.role == '3'

class IsDistributor(permissions.BasePermission):
    message = "User doesn't have role Distributor!"

    def has_permission(self, request, view):
        return request.user.role == '2'

class IsRegisteredReader(permissions.BasePermission):
    message = "User doesn't have role Registered Reader!"

    def has_permission(self, request, view):
        return request.user.role == '1'

# This should be unreachable and unusable permission
class IsNotRegistered(permissions.BasePermission):
    message = "User is not unregistered!"

    def has_permission(self, request, view):
        return request.user.role == '0'