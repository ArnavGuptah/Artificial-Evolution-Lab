class Resource:

    def __init__(
        self,
        x,
        y,
        quantity=1,
        properties=None
    ):

        self.x = x

        self.y = y

        self.quantity = quantity

        self.properties = (
            properties
            if properties
            else {}
        )