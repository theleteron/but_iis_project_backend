from rest_framework import permissions

class IsAdministrator(permissions.BasePermission):
    message = "User doesn't have role Administrator!"

    def has_permission(self, request, view):
        return request.user.role == 4

class IsLibrarian(permissions.BasePermission):
    message = "User doesn't have role Librarian!"

    def has_permission(self, request, view):
        return request.user.role == 3

class IsDistributor(permissions.BasePermission):
    message = "User doesn't have role Distributor!"

    def has_permission(self, request, view):
        return request.user.role == 2

class IsRegistredReader(permissions.BasePermission):
    message = "User doesn't have role Registred Reader!"

    def has_permission(self, request, view):
        return request.user.role == 1