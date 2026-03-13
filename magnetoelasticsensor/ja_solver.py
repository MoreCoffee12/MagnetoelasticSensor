"""
ja_solver.py

Solves the isotropic Jiles-Atherton ODE (dM/dH) for a single monotone
field-sweep segment, returning the (H, M) trajectory.

The four solver options parallel those of the original MATLAB ``JAsolver.m``:

    1 — RK23   (SciPy ``RK23``, equivalent to MATLAB ``ode23``)
    2 — RK45   (SciPy ``RK45``, equivalent to MATLAB ``ode45``)
    3 — Radau  (SciPy ``Radau``, stiff solver, equivalent to MATLAB ``ode23s``)
    4 — RK4    (fixed-step 4th-order Runge-Kutta, 50 uniform steps)

Important
---------
``h_start`` and ``h_end`` must differ; the field must vary monotonically within
each call.  To simulate a full hysteresis loop, call this function in segments
(e.g., 0 → H_max → -H_max → 0) and concatenate the results.

References
----------
[1] Jiles D. C., Atherton D. "Theory of ferromagnetic hysteresis."
    Journal of Magnetism and Magnetic Materials, 61 (1986) 48.
[2] Szewczyk R. "Computational problems connected with Jiles-Atherton model
    of magnetic hysteresis." Advances in Intelligent Systems and Computing
    (Springer), 267 (2014) 275.
"""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp

from magnetoelasticsensor.dmdh import dmdh

_SCIPY_METHODS: dict[int, str] = {
    1: "RK23",
    2: "RK45",
    3: "Radau",
}


def ja_solver(
    a: float,
    k: float,
    c: float,
    ms: float,
    alpha: float,
    h_start: float,
    h_end: float,
    m0: float,
    solver_type: int = 1,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Solve the Jiles-Atherton ODE for one monotone field-sweep segment.

    Parameters
    ----------
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
        Initial applied field value, A/m.
    h_end : float
        Final applied field value, A/m.
    m0 : float
        Magnetization at ``h_start`` (initial condition), A/m.
    solver_type : int, optional
        Numerical integration method:

        * ``1`` — RK23  (default, equivalent to MATLAB ``ode23``)
        * ``2`` — RK45  (equivalent to MATLAB ``ode45``)
        * ``3`` — Radau (stiff; equivalent to MATLAB ``ode23s``)
        * ``4`` — RK4   (fixed-step, 50 uniform steps)

    Returns
    -------
    h_out : numpy.ndarray
        Applied-field values at each solver evaluation point, A/m.
    m_out : numpy.ndarray
        Magnetization values at each solver evaluation point, A/m.

    Raises
    ------
    ValueError
        If ``solver_type`` is not in ``{1, 2, 3, 4}``.

    Notes
    -----
    When ``h_start == h_end`` the function returns the two-point arrays
    ``[h_end, h_start]`` and ``[m0, m0]``, consistent with the behaviour of
    the original MATLAB implementation.
    """
    if h_end == h_start:
        return np.array([h_end, h_start]), np.array([m0, m0])

    if solver_type not in (1, 2, 3, 4):
        raise ValueError(
            f"solver_type must be 1, 2, 3, or 4; got {solver_type!r}."
        )

    def _rhs(h: float, m_vec: list[float]) -> list[float]:
        return [
            dmdh(
                h=h,
                m=m_vec[0],
                a=a,
                k=k,
                c=c,
                ms=ms,
                alpha=alpha,
                h_start=h_start,
                h_end=h_end,
            )
        ]

    span = (h_start, h_end)
    y0 = [float(m0)]
    step_size = abs(h_end - h_start) / 10.0

    if solver_type == 4:
        return _rk4(_rhs, span, y0, n_steps=50)

    sol = solve_ivp(
        _rhs,
        span,
        y0,
        method=_SCIPY_METHODS[solver_type],
        rtol=1e-4,
        atol=1e-6,
        max_step=step_size,
        first_step=step_size,
    )

    return sol.t, sol.y[0]


def _rk4(
    f,
    t_span: tuple[float, float],
    y0: list[float],
    n_steps: int = 50,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Fixed-step classical 4th-order Runge-Kutta integrator.

    Equivalent to the ``rk4(f, [t0 tf], y0, n_steps)`` call used in the
    original MATLAB ``JAsolver.m``.

    Parameters
    ----------
    f : callable
        ODE right-hand side ``f(t, y) -> list[float]``.
    t_span : (float, float)
        Integration interval ``(t_start, t_end)``.
    y0 : list[float]
        Initial state vector.
    n_steps : int
        Number of uniform steps.

    Returns
    -------
    ts : numpy.ndarray
        Field evaluation points.
    ys : numpy.ndarray
        State values at each evaluation point.
    """
    t0, tf = t_span
    h = (tf - t0) / n_steps
    t = t0
    y = np.array(y0, dtype=float)
    ts = [t]
    ys = [float(y[0])]

    for _ in range(n_steps):
        k1 = np.array(f(t, y), dtype=float)
        k2 = np.array(f(t + h / 2.0, y + (h / 2.0) * k1), dtype=float)
        k3 = np.array(f(t + h / 2.0, y + (h / 2.0) * k2), dtype=float)
        k4 = np.array(f(t + h, y + h * k3), dtype=float)
        y = y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        t = t + h
        ts.append(t)
        ys.append(float(y[0]))

    return np.array(ts), np.array(ys)
