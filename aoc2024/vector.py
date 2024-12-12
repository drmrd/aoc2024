import numbers


class DimensionMismatch(ValueError):
    pass


class Vector[T]:
    def __init__(self, *components: T):
        self._components = tuple(components)
        self._dimension = len(self._components)

    def __getitem__(self, item):
        return self._components[item]

    def __setitem__(self, key, value):
        raise TypeError('Vectors are immutable.')

    def __iter__(self):
        return iter(self._components)

    def __add__(self, other):
        self._raise_on_dimension_mismatch(other)
        return Vector(*(x + other_x for x, other_x in zip(self, other)))

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        self._raise_on_dimension_mismatch(other)
        return Vector(*(x - other_x for x, other_x in zip(self, other)))

    def __rsub__(self, other):
        self._raise_on_dimension_mismatch(other)
        return Vector(*(-x + other_x for x, other_x in zip(self, other)))

    def __neg__(self):
        return Vector(*(-x for x in self))

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            return Vector(*(other * x for x in self))
        elif isinstance(other, Vector):
            return Vector(*(x * other_x for x, other_x in zip(self, other)))
        raise ValueError(
            'No implementation for the product of types Vector and '
            f'{type(other)}.'
        )

    def __rmul__(self, other):
        return self * other

    def __eq__(self, other):
        return all(x == other_x for x, other_x in zip(self, other))

    def __hash__(self):
        return hash(self._components)

    def __repr__(self):
        return f'Vector({', '.join(map(str, self._components))})'

    def __str__(self):
        return f'<{', '.join(map(str, self._components))}>'

    @property
    def dimension(self) -> int:
        return self._dimension

    def _raise_on_dimension_mismatch(self, other):
        if self.dimension != other.dimension:
            raise DimensionMismatch