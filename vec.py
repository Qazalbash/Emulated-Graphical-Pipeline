class vec:

    def __init__(self,
                 x: int | float,
                 y: int | float,
                 z: int | float = 0.0) -> None:
        self.x = x
        self.y = y
        self.z = z

    # def __repr__(self) -> str:
    #     return f"[{self.x}, {self.y}, {self.z}]"


def add(u: vec, v: vec) -> vec:
    return vec(u.x + v.x, u.y + v.y, u.z + v.z)


def scale(factor: int | float, u: vec) -> vec:
    return vec(u.x * factor, u.y * factor, u.z * factor)
