def get_for_update(model_item, nowait: bool = True):
    """
    Returns the same instance of the model item retrieved from the database with `.select_for_update()`

    By default this is a non-blocking call; to change the behavior, set nowait=False

    Args:
        model_item: the model item to re-fetch from the database
        nowait: whether to block until the row is unlocked

    Returns:
        the model item
    """
    queryset = model_item._meta.model.objects.select_for_update(nowait=nowait)
    model_item_for_update = queryset.get(pk=model_item.pk)

    return model_item_for_update
