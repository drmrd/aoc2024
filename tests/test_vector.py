import hypothesis as hyp
import hypothesis.strategies as st

from aoc2024.vector import DimensionMismatch, Vector


@st.composite
def components(draw, dimension=st.integers(min_value=1)) -> tuple:
    # Complex numbers removed, since their strategy does not appear to
    # obey allow_nan.
    finite_real_strategies = [
        lambda: strategy(allow_infinity=False, allow_nan=False)
        for strategy in (st.decimals, st.floats)
    ]
    component_strategy = draw(st.sampled_from([
        st.integers, st.fractions, *finite_real_strategies
    ]))
    if isinstance(dimension, st.SearchStrategy):
        dimension = draw(dimension)
    return draw(st.lists(
        component_strategy(), min_size=dimension, max_size=dimension
    ))


@st.composite
def vectors(draw, dimension=st.integers(min_value=1)) -> Vector:
    return Vector(*draw(components(dimension=dimension)))


@hyp.given(components=st.lists(st.integers(), min_size=1))
def test_vector_can_be_constructed_with_any_dimension(components):
    Vector(components)


@hyp.given(
    components1=components(dimension=3),
    components2=components(dimension=3),
    scalar=st.floats(allow_infinity=False, allow_nan=False)
)
def test_vector_arithmetic(components1, components2, scalar):
    vector1 = Vector(*components1)
    vector2 = Vector(*components2)

    sum_ = Vector(*(x + y for x, y in zip(components1, components2)))
    difference = Vector(*(x - y for x, y in zip(components1, components2)))
    entrywise_product = Vector(*(x * y for x, y in zip(components1, components2)))
    negation = Vector(*(-x for x in components1))
    scalar_product = Vector(*(scalar * x for x in components1))

    assert vector1 + vector2 == sum_
    assert vector1 - vector2 == difference
    assert vector1 * vector2 == entrywise_product
    assert -vector1 == negation
    assert scalar * vector1 == scalar_product
    assert vector1 * scalar == scalar_product