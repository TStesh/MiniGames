"""
Class vector 3D
"""

class Vec3:

    __dim = 3

    def __init__(self, a):
        if len(a) != self.__dim:
            raise ArithmeticError('Can not create the Vec3 instance')
        self.vec = a

    def prn(self):
        print(f"({', '.join(map(str, self.vec))})")

    def __add__(self, other):
        if not isinstance(other, Vec3):
            raise ArithmeticError('Type of other must be Vec3')
        return Vec3(tuple(map(lambda x: x[0] + x[1], zip(self.vec, other.vec))))

    def __iadd__(self, other):
        if not isinstance(other, Vec3):
            raise ArithmeticError('Type of other must be Vec3')
        self.vec = tuple(map(lambda x: x[0] + x[1], zip(self.vec, other.vec)))
        return self

    def __sub__(self, other):
        if not isinstance(other, Vec3):
            raise ArithmeticError('Type of other must be Vec3')
        return Vec3(tuple(map(lambda x: x[0] - x[1], zip(self.vec, other.vec))))

    def __isub__(self, other):
        if not isinstance(other, Vec3):
            raise ArithmeticError('Type of other must be Vec3')
        self.vec = tuple(map(lambda x: x[0] - x[1], zip(self.vec, other.vec)))
        return self

    def __mul__(self, other):
        if not isinstance(other, (int, float, Vec3)):
            raise ArithmeticError('Type of other must be number or Vec3')
        if isinstance(other, (int, float)):
            return Vec3(tuple(map(lambda x: x * other, self.vec)))
        else:
            return sum(map(lambda x: x[0] * x[1], zip(self.vec, other.vec)))

    def __imul__(self, other):
        if not isinstance(other, (int, float)):
            raise ArithmeticError('Type of other must be number')
        self.vec = tuple(map(lambda x: x * other, self.vec))
        return self

    def __neg__(self):
        return self * -1

    def cross(self, other):
        if not isinstance(other, Vec3):
            raise ArithmeticError('Type of other must be Vec3')
        return Vec3((
            self.vec[1] * other.vec[2] - self.vec[2] * other.vec[1],
            self.vec[2] * other.vec[0] - self.vec[0] * other.vec[2],
            self.vec[0] * other.vec[1] - self.vec[1] * other.vec[0]
        ))

    def length(self) -> float:
        return (self * self) ** .5

    def ort(self):
        return self * (1 / self.length())
