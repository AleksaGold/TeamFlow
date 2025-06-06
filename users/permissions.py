from rest_framework import permissions


class IsUserPermission(permissions.BasePermission):
    """Проверка прав доступа для пользователей с ролью "user"."""

    def has_permission(self, request, view):
        """Проверяет роль пользователя."""
        return request.user.role == "user"


class IsManagerPermission(permissions.BasePermission):
    """Проверка прав доступа для пользователей с ролью "manager"."""

    def has_permission(self, request, view):
        """Проверяет роль пользователя."""
        return request.user.role == "manager"


class IsAdminPermission(permissions.BasePermission):
    """Проверка прав доступа для пользователей с ролью "admin"."""

    def has_permission(self, request, view):
        """Проверяет роль пользователя."""
        return request.user.role == "admin"


class IsOwnerPermission(permissions.BasePermission):
    """Проверка прав доступа для пользователя."""

    def has_object_permission(self, request, view, obj):
        """Проверяет является ли пользователь объектом."""
        return obj == request.user
