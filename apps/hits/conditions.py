def check_permissions(instance):
    from tracing.middleware import TracingMiddleware

    information = TracingMiddleware.get_info()
    user = information.get("user", False)
    if (
        user.pk == 1
        or instance.assigned.pk == user.boss
        or instance.assigned.pk == user.pk
    ):
        return True
    return False
