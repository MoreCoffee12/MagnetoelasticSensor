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

from dataclasses import dataclass, field


@dataclass
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
    theta : float, optional
        Angle between the applied stress axis and magnetization axis,
        radians. Used in the stress-induced field term; defaults to 0.0.
    nu : float, optional
        Poisson ratio used in the stress coupling term; defaults to 0.3.
    sigma0 : float, optional
        Applied uniaxial stress, Pa. Updating this value updates the
        computed read-only ``gamma1`` and ``gamma2`` values.
    gamma1_intercept : float, optional
        Public intercept for the linear ``gamma1(sigma0)`` model.
    gamma2_intercept : float, optional
        Public intercept for the linear ``gamma2(sigma0)`` model.
    gamma1_sigma_slope : float, optional
        Linear slope for ``gamma1`` as a function of ``sigma0``.
    gamma2_sigma_slope : float, optional
        Linear slope for ``gamma2`` as a function of ``sigma0``.
    """

    ms: float
    a: float
    alpha: float
    k: float = 0.0
    c: float = 0.0
    theta: float = 0.0
    nu: float = 0.3
    sigma0: float = 0.0
    gamma1_intercept: float = 0.0
    gamma2_intercept: float = 0.0
    gamma1_sigma_slope: float = 0.0
    gamma2_sigma_slope: float = 0.0

    _gamma1: float = field(init=False, repr=False, default=0.0)
    _gamma2: float = field(init=False, repr=False, default=0.0)

    def __post_init__(self) -> None:
        object.__setattr__(self, "sigma0", float(self.sigma0))
        object.__setattr__(self, "gamma1_intercept", float(self.gamma1_intercept))
        object.__setattr__(self, "gamma2_intercept", float(self.gamma2_intercept))
        object.__setattr__(self, "gamma1_sigma_slope", float(self.gamma1_sigma_slope))
        object.__setattr__(self, "gamma2_sigma_slope", float(self.gamma2_sigma_slope))

        self._update_stress_dependent_gammas()

    @property
    def gamma1(self) -> float:
        """Read-only first-order magnetoelastic coefficient at current stress."""
        return self._gamma1

    @property
    def gamma2(self) -> float:
        """Read-only third-order magnetoelastic coefficient at current stress."""
        return self._gamma2

    def __setattr__(self, name: str, value) -> None:
        if name in {"gamma1", "gamma2"}:
            raise AttributeError(
                f"'{name}' is read-only. Update sigma0, intercepts, or slopes instead."
            )

        if name in {
            "sigma0",
            "gamma1_intercept",
            "gamma2_intercept",
            "gamma1_sigma_slope",
            "gamma2_sigma_slope",
        }:
            value = float(value)

        object.__setattr__(self, name, value)

        # During dataclass initialization, dependent fields may not yet exist.
        if "_gamma1" not in self.__dict__:
            return

        if name in {
            "sigma0",
            "gamma1_intercept",
            "gamma2_intercept",
            "gamma1_sigma_slope",
            "gamma2_sigma_slope",
        }:
            self._update_stress_dependent_gammas()

    def _update_stress_dependent_gammas(self) -> None:
        object.__setattr__(
            self,
            "_gamma1",
            float(self.gamma1_intercept) + self.gamma1_sigma_slope * self.sigma0,
        )
        object.__setattr__(
            self,
            "_gamma2",
            float(self.gamma2_intercept) + self.gamma2_sigma_slope * self.sigma0,
        )
