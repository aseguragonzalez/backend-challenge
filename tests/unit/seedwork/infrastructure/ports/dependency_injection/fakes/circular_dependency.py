class CircularDependency:
    def __init__(self, circular_relation: "CircularDependency") -> None:
        self.circular_relation = circular_relation
