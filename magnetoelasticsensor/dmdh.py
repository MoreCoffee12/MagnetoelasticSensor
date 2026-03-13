"""
dmdh.py

Implements the dM/dH differential equation for the isotropic Jiles-Atherton
hysteresis model (Equation 34 of reference [1]).

Formula
-------
    dM/dH = (Man - M)_clip / [(1+c)*(delta*k - alpha*(Man-M))]
            + c/(1+c) * dMan/dH_eff

Where:

    Man      = anhysteretic magnetization = ms * L((H + alpha*M) / a)
    L(x)     = Langevin function = coth(x) - 1/x
    delta    = +1 when H is increasing, -1 when H is decreasing
    (Man-M)_clip = Man - M, but forced to zero when it violates the physical
                 realizability condition (see Notes)

Notes
-----
The irreversible magnetization component can only increase while H is
increasing and only decrease while H is decreasing.  When the operating
point temporarily sits on the wrong side of the anhysteretic curve (e.g.,
during reversal), the irreversible numerator is clipped to zero to enforce
this constraint [2].

This is the direct Python translation of the ``dMdH.m`` MATLAB function from
the reference JAmodel implementation, with ``Mah_iso`` replaced by the
``anhysteretic_magnetization`` function from this library.

References
----------
[1] Jiles D. C., Atherton D. "Theory of ferromagnetic hysteresis."
    Journal of Magnetism and Magnetic Materials, 61 (1986) 48.
[2] Chwastek K., Szczyglowski J. "Identification of a hysteresis model
    parameters with genetic algorithms." Mathematics and Computers in
    Simulation, 71 (2006) 206.
"""

from __future__ import annotations

import numpy as np

from magnetoelasticsensor.anhyst_iso import (
    anhysteretic_magnetization,
    anhysteretic_magnetization_deriv,
)


def dmdh(
    h: float | np.ndarray,
    m: float | np.ndarray,
    a: float,
    k: float,
    c: float,
    ms: float,
    alpha: float,
    h_start: float,
    h_end: float,
) -> float | np.ndarray:
    """
    Compute dM/dH for the isotropic Jiles-Atherton model (Eq. 34 of [1]).

    Parameters
    ----------
    h : float or numpy.ndarray
        Applied magnetic field, A/m.
    m : float or numpy.ndarray
        Magnetization, A/m.  Must have the same shape as ``h``.
    a : float
        Domain density / shape parameter for the anhysteretic curve, A/m.
    k : float
        Average energy required to break a pinning site, A/m.
    c : float
        Magnetization reversibility, dimensionless (0 ≤ c ≤ 1).
    ms : float
        Saturation magnetization, A/m.
    alpha : float
        Mean-field (Bloch) coupling coefficient, dimensionless.
    h_start : float
        Starting field value for the current monotone sweep segment, A/m.
    h_end : float
        Ending field value for the current monotone sweep segment, A/m.

    Returns
    -------
    float or numpy.ndarray
        dM/dH value(s), same shape as ``h``.

    Raises
    ------
    ValueError
        If any of ``a``, ``k``, ``c``, ``ms``, ``alpha``, ``h_start``,
        ``h_end`` is not a scalar, or if ``h`` and ``m`` have mismatched
        shapes.
    """
    # Validate scalar model parameters (mirrors the MATLAB guard)
    for name, val in (
        ("a", a),
        ("k", k),
        ("c", c),
        ("ms", ms),
        ("alpha", alpha),
        ("h_start", h_start),
        ("h_end", h_end),
    ):
        if not np.isscalar(val):
            raise ValueError(
                f"Parameter '{name}' must be a scalar; "
                f"got shape {np.shape(val)}."
            )

    h_arr = np.asarray(h, dtype=float)
    m_arr = np.asarray(m, dtype=float)

    if h_arr.shape != m_arr.shape:
        raise ValueError(
            f"'h' and 'm' must have the same shape; "
            f"got h.shape={h_arr.shape}, m.shape={m_arr.shape}."
        )

    # Anhysteretic magnetization at the effective field H + alpha*M
    man = anhysteretic_magnetization(h=h_arr, m=m_arr, ms=ms, a=a, alpha=alpha)

    # Irreversible numerator (Man - M), clipped to enforce realizability
    dm1 = man - m_arr
    if h_end > h_start:
        dm1 = np.maximum(dm1, 0.0)
        delta = 1.0
    else:
        dm1 = np.minimum(dm1, 0.0)
        delta = -1.0

    # Denominator: (1+c) * (delta*k - alpha*(Man-M))
    dm2 = (1.0 + c) * (delta * k - alpha * (man - m_arr))

    # Reversible contribution: c/(1+c) * dMan/dH_eff
    dm3 = (c / (1.0 + c)) * anhysteretic_magnetization_deriv(
        h=h_arr, m=m_arr, ms=ms, a=a, alpha=alpha
    )

    result = dm1 / dm2 + dm3

    if np.isscalar(h) and np.isscalar(m):
        return float(result)

    return result
