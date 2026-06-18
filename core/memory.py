from collections import deque


class Memory:

    def __init__(

        self,

        max_events=100

    ):

        # recent experiences

        self.events = deque(

            maxlen=max_events

        )


        # persistent information

        self.state = {}



    def remember(

        self,

        key,

        value

    ):

        self.state[key] = value



    def recall(

        self,

        key,

        default=None

    ):

        return self.state.get(

            key,

            default

        )



    def add_event(

        self,

        event

    ):

        self.events.append(

            event

        )



    def recent_events(

        self

    ):

        return list(

            self.events

        )



    def forget(

        self,

        key

    ):

        if key in self.state:

            del self.state[key]