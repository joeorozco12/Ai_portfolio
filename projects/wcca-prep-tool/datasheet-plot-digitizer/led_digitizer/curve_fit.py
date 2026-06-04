"""Curve interpolation utilities for digitized LED plot data."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from .calibration import EngineeringPoint


@dataclass(frozen=True)
class PchipSegment:
    """One interval of a shape-preserving cubic Hermite interpolation."""

    x0: float
    x1: float
    a: float
    b: float
    c: float
    d: float

    def evaluate(self, x_value: float) -> float:
        t = x_value - self.x0
        return self.a + self.b * t + self.c * t * t + self.d * t * t * t


def sort_unique_points(points: Iterable[EngineeringPoint]) -> list[EngineeringPoint]:
    """Sort points by x and reject duplicate x-values."""

    sorted_points = sorted(points, key=lambda point: point.x)
    seen: set[float] = set()
    for point in sorted_points:
        rounded_x = round(point.x, 12)
        if rounded_x in seen:
            raise ValueError("PCHIP interpolation requires unique x-values.")
        seen.add(rounded_x)
    if len(sorted_points) < 2:
        raise ValueError("At least two points are required.")
    return sorted_points


def linear_interpolate(points: Sequence[EngineeringPoint], x_value: float) -> float:
    """Piecewise-linear interpolation with endpoint clamping."""

    sorted_points = sort_unique_points(points)
    if x_value <= sorted_points[0].x:
        return sorted_points[0].y
    if x_value >= sorted_points[-1].x:
        return sorted_points[-1].y

    for left, right in zip(sorted_points, sorted_points[1:]):
        if left.x <= x_value <= right.x:
            fraction = (x_value - left.x) / (right.x - left.x)
            return left.y + fraction * (right.y - left.y)

    raise ValueError("Interpolation failed to find an interval.")


def build_pchip_segments(points: Sequence[EngineeringPoint]) -> list[PchipSegment]:
    """Build monotone shape-preserving PCHIP segments.

    This is a dependency-free implementation of the Fritsch-Carlson style
    slope limiting used by PCHIP. It is adequate for transparent portfolio
    demonstration output and still requires engineering review.
    """

    sorted_points = sort_unique_points(points)
    xs = [point.x for point in sorted_points]
    ys = [point.y for point in sorted_points]
    n = len(xs)
    h = [xs[i + 1] - xs[i] for i in range(n - 1)]
    delta = [(ys[i + 1] - ys[i]) / h[i] for i in range(n - 1)]

    if n == 2:
        derivatives = [delta[0], delta[0]]
    else:
        derivatives = [0.0 for _ in range(n)]
        derivatives[0] = _edge_derivative(h[0], h[1], delta[0], delta[1])
        derivatives[-1] = _edge_derivative(h[-1], h[-2], delta[-1], delta[-2])

        for index in range(1, n - 1):
            left_slope = delta[index - 1]
            right_slope = delta[index]
            if left_slope == 0.0 or right_slope == 0.0:
                derivatives[index] = 0.0
            elif (left_slope > 0) != (right_slope > 0):
                derivatives[index] = 0.0
            else:
                w1 = 2.0 * h[index] + h[index - 1]
                w2 = h[index] + 2.0 * h[index - 1]
                derivatives[index] = (w1 + w2) / (
                    (w1 / left_slope) + (w2 / right_slope)
                )

    segments: list[PchipSegment] = []
    for index in range(n - 1):
        interval = h[index]
        slope = delta[index]
        d0 = derivatives[index]
        d1 = derivatives[index + 1]
        c = (3.0 * slope - 2.0 * d0 - d1) / interval
        d = (d0 + d1 - 2.0 * slope) / (interval * interval)
        segments.append(
            PchipSegment(
                x0=xs[index],
                x1=xs[index + 1],
                a=ys[index],
                b=d0,
                c=c,
                d=d,
            )
        )

    return segments


def evaluate_pchip(segments: Sequence[PchipSegment], x_value: float) -> float:
    """Evaluate PCHIP with endpoint clamping."""

    if not segments:
        raise ValueError("At least one PCHIP segment is required.")
    if x_value <= segments[0].x0:
        return segments[0].a
    if x_value >= segments[-1].x1:
        return segments[-1].evaluate(segments[-1].x1)

    for segment in segments:
        if segment.x0 <= x_value <= segment.x1:
            return segment.evaluate(x_value)

    raise ValueError("PCHIP evaluation failed to find an interval.")


def _edge_derivative(h0: float, h1: float, delta0: float, delta1: float) -> float:
    derivative = ((2.0 * h0 + h1) * delta0 - h0 * delta1) / (h0 + h1)
    if derivative == 0.0:
        return 0.0
    if (derivative > 0) != (delta0 > 0):
        return 0.0
    if (delta0 > 0) != (delta1 > 0) and abs(derivative) > abs(3.0 * delta0):
        return 3.0 * delta0
    return derivative
