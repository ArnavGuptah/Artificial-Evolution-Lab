class Action:

    def __init__(

        self,

        action_type,

        data=None

    ):

        self.type = action_type

        self.data = (

            data

            if data

            else {}

        )

    def __repr__(self):

        return (

            f"Action("

            f"type={self.type}, "

            f"data={self.data}"

            f")"

        )