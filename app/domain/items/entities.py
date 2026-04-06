from app.domain.items.dto import ItemDTO


class ItemEntity:
    def __init__(self, data: ItemDTO) -> None:
        self.data = data
