def serializer_create(serializer_cls, **kwargs):
    serializer = serializer_cls(**kwargs)
    serializer.is_valid(raise_exception = True)
    serializer.save()
    return serializer.data