"""
ja_props.py

Parameter container for the isotropic Jiles-Atherton hysteresis model.

All five material/physical parameters that define a J-A model instance are
grouped into a single immutable dataclass so they can be passed as one
cohesive object instead of individual primitives.

References
----------
[1] Jiles D. C., Atherton D. "Theory of ferromagnetic hysteresis."
    Journal of Magnetism and Magnetic Materials, 61 (1986) 48.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class JAProps:
    """
    Jiles-Atherton model parameters for an isotropic ferromagnetic material.

    Parameters
    ----------
    ms : float
        Saturation magnetization, A/m.
    a : float
        Domain density / shape parameter for the anhysteretic curve, A/m.
        Must be nonzero.
    alpha : float
        Mean-field (Bloch) coupling coefficient, dimensionless.
    k : float, optional
        Average energy required to break a pinning site, A/m.  Only required
        by the full hysteresis solver; defaults to 0.0.
    c : float, optional
        Magnetization reversibility, dimensionless (0 ≤ c ≤ 1).  Only
        required by the full hysteresis solver; defaults to 0.0.
    """

    ms: float
    a: float
    alpha: float
    k: float = 0.0
    c: float = 0.0
