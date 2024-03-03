def has_access(user, product):
    """
    Проверяет доступ пользователя к продукту.

    Args:
        user: Пользователь, для которого проверяется доступ.
        product: Продукт, к которому проверяется доступ.

    Returns:
        bool: True, если у пользователя есть доступ к продукту, False в противном случае.
    """
    return user in product.users_with_access.all()
