class CreateItemError(Exception):
    pass


class ItemAlreadyExistsError(CreateItemError):
    pass
