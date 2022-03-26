def get_for_update(model_item):
    """
    Returns the same instance of the model item retrieved from the database with `.select_for_update()`

    Args:
        model_item: the model item to re-fetch from the database

    Returns:
        the model item
    """
    queryset = model_item._meta.model.objects.select_for_update()
    model_item_for_update = queryset.get(pk=model_item.pk)

    return model_item_for_update
