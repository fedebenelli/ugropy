"""Joback's module."""
from typing import Union

import numpy as np
from numpy.typing import NDArray

from ugropy.constants import (
    R,
    joback_properties_contibutions,
    joback_subgroups,
)
from ugropy.model_getters import (
    get_joback_groups,
)


class Joback:
    """Joback [1] group contribution properties estimator.

    Parameters
    ----------
    identifier : str or rdkit.Chem.rdchem.Mol
        Identifier of a molecule (name, SMILES, groups, or Chem.rdchem.Mol).
        Example: you can use hexane, CCCCCC, {"-CH3": 2, "-CH2-": 4} for name,
        SMILES and groups respectively.
    identifier_type : str, optional
        Use 'name' to search a molecule by name, 'smiles' to provide the
        molecule SMILES representation, 'groups' to provide Joback groups or
        'mol' to provide a rdkit.Chem.rdchem.Mol object, by default "name".
    normal_boiling_point : float, optional
        If provided, will be used to estimate critical temperature, acentric
        factor, and vapor pressure instead of the estimated normal boiling
        point, by default None.

    Attributes
    ----------
    groups : dict
        Joback functional groups of the molecule.
    exp_nbt : float
        User provided experimental normal boiling point [K].
    critical_temperature : float
        Joback estimated critical temperature [K].
    critical_pressure : float
        Joback estimated critical pressure [bar].
    critical_volume : float
        Joback estimated critical volume [cm³/mol].
    normal_boiling_point : float
        Joback estimated normal boiling point [K].
    fusion_temperature : float
        Joback estimated fusion temperature [K].
    h_formation : float
        Joback estimated enthalpy of formation ideal gas at 298 K [kJ/mol].
    g_formation : float
        Joback estimated Gibbs energy of formation ideal gas at 298 K [K].
    heat_capacity_ideal_gas_params : dict
        Joback estimated Reid's ideal gas heat capacity equation parameters
        [J/mol/K].
    h_fusion : float
        Joback estimated fusion enthalpy [kJ/mol].
    h_vaporization : float
        Joback estimated vaporization enthalpy at the normal boiling point
        [kJ/mol].
    sum_na : float
        Joback n_A contribution to liquid viscosity [N/s/m²].
    sum_nb : float
        Joback n_B contribution to liquid viscosity [N/s/m²].
    molecular_weight : float
        Molecular weight from Joback's subgroups [g/mol].
    acentric_factor : float
        Acentric factor from Lee and Kesler's equation [2].
    vapor_pressure_params : dict
        Vapor pressure G and k parameters for the Riedel-Plank-Miller [2]
        equation [bar].

    Bibliography
    ------------
    [1] Joback, K. G., & Reid, R. C. (1987). ESTIMATION OF PURE-COMPONENT
    PROPERTIES FROM GROUP-CONTRIBUTIONS. Chemical Engineering Communications,
    57(1–6), 233–243. https://doi.org/10.1080/00986448708960487

    [2] Joback, K. G. (1989). Designing molecules possessing desired physical
    property values [Thesis (Ph. D.), Massachusetts Institute of Technology].
    https://dspace.mit.edu/handle/1721.1/14191
    """

    def __init__(
        self,
        identifier: str,
        identifier_type: str = "name",
        normal_boiling_point: float = None,
    ) -> None:
        # Skip if instantiation from_groups is made.
        if identifier_type in ["name", "smiles", "mol"]:
            self.groups = get_joback_groups(identifier, identifier_type)
        elif identifier_type == "groups":
            self.groups = identifier
        else:
            raise ValueError(
                f"Identifier type ''{identifier_type}'' is incorrect. Use "
                "'name', 'smiles', 'mol' or 'groups'."
            )

        # experimental boiling temperature
        self.exp_nbt = normal_boiling_point

        # Original Joback properties
        self.critical_temperature = None
        self.critical_pressure = None
        self.critical_volume = None
        self.normal_boiling_point = None
        self.fusion_temperature = None
        self.h_formation = None
        self.g_formation = None
        self.heat_capacity_ideal_gas_params = np.array([])
        self.h_fusion = None
        self.h_vaporization = None
        self.sum_na = None
        self.sum_nb = None
        self.molecular_weight = None

        # Extra properties
        self.acentric_factor = None
        self.vapor_pressure_params = {}

        # Fill the properties' values
        if self.groups != {}:
            self._calculate_properties()

    def heat_capacity_ideal_gas(
        self, temperature: Union[float, NDArray]
    ) -> Union[float, NDArray]:
        """Calculate the ideal gas heat capacity [J/mol/K].

        Uses the Joback estimated Reid's ideal gas heat capacity equation
        parameters [J/mol/K].

        Parameters
        ----------
        temperature : Union[float, NDArray]
            Temperature [K]

        Returns
        -------
        Union[float, NDArray]
            Ideal gas heat capacity [J/mol/K].
        """
        a, b, c, d = self.heat_capacity_ideal_gas_params

        t = temperature

        return a + b * t + c * t**2 + d * t**3

    def heat_capacity_liquid(
        self, temperature: Union[float, NDArray]
    ) -> Union[float, NDArray]:
        """Calculate the liquid heat capacity [J/mol/K].

        Uses the Rowlinson-Bondi [1-2] equation with the Joback estimated
        properties.

        Parameters
        ----------
        temperature : Union[float, NDArray]
            Temperature [K]

        Returns
        -------
        Union[float, NDArray]
            Ideal gas heat capacity [J/mol/K].

        Bibliography
        ------------
        [1] Bondi, A. (1966). Estimation of Heat Capacity of Liquids.
        Industrial & Engineering Chemistry Fundamentals, 5(4), 442–449.
        https://doi.org/10.1021/i160020a001

        [2] Rowlinson, J. S., & Swinton, F. (2013). Liquids and liquid
        mixtures: Butterworths monographs in chemistry. Butterworth-Heinemann
        """
        tr = temperature / self.critical_temperature
        w = self.acentric_factor

        c_p0 = self.heat_capacity_ideal_gas(temperature)

        c_pl = c_p0 + R * (
            2.56
            + 0.436 * (1 - tr) ** (-1)
            + w
            * (
                2.91
                + 4.28 * (1 - tr) ** (-1 / 3) * tr ** (-1)
                + 0.296 * (1 - tr) ** (-1)
            )
        )

        return c_pl

    def viscosity_liquid(
        self, temperature: Union[float, NDArray]
    ) -> Union[float, NDArray]:
        """Calculate the Joback estimated liquid viscosity [N/s/m²].

        Parameters
        ----------
        temperature : Union[float, NDArray]
            Temperature [K]

        Returns
        -------
        Union[float, NDArray]
            Liquid viscosity [N/s/m²].
        """
        t = temperature

        n_l = self.molecular_weight * np.exp(
            (self.sum_na - 597.82) / t + self.sum_nb - 11.202
        )
        return n_l

    def vapor_pressure(
        self, temperature: Union[float, NDArray]
    ) -> Union[float, NDArray]:
        """Calculate the vapor pressure [bar].

        Uses the Riedel-Plank-Miller [1] equation with the Joback estimated
        properties.

        Parameters
        ----------
        temperature : Union[float, NDArray]
            Temperature [K]

        Returns
        -------
        Union[float, NDArray]
            Vapor pressure [bar]

        Bibliography
        ------------
        [1] Joback, K. G. (1989). Designing molecules possessing desired
        physical property values [Thesis (Ph. D.), Massachusetts Institute of
        Technology]. https://dspace.mit.edu/handle/1721.1/14191
        """
        tr = temperature / self.critical_temperature

        g = self.vapor_pressure_params["G"]
        k = self.vapor_pressure_params["k"]

        vp_r = np.exp(-g / tr * (1 - tr**2 + k * (3 + tr) * (1 - tr) ** 3))

        vp = vp_r * self.critical_pressure

        return vp

    def _calculate_properties(self) -> None:
        """Obtain the molecule properties from Joback's groups."""
        groups = list(self.groups.keys())
        ocurr = list(self.groups.values())

        df = joback_properties_contibutions.loc[groups]

        # =====================================================================
        # Calculate complete contribution properties (no contribution missing)
        # =====================================================================
        tc_c = df["Tc"].to_numpy()
        pc_c = df["Pc"].to_numpy()
        vc_c = df["Vc"].to_numpy()
        tb_c = df["Tb"].to_numpy()
        tf_c = df["Tf"].to_numpy()
        hform_c = df["Hform"].to_numpy()
        gform_c = df["Gform"].to_numpy()
        hvap_c = df["Hvap"].to_numpy()
        numa_c = df["num_of_atoms"].to_numpy()
        mw_c = joback_subgroups.loc[groups, "molecular_weight"].to_numpy()

        # Molecular weight
        self.molecular_weight = np.dot(ocurr, mw_c)

        # Joback normal boiling point (Tb)
        self.normal_boiling_point = 198.2 + np.dot(ocurr, tb_c)

        # Fusion temperature (Tf)
        self.fusion_temperature = 122.5 + np.dot(ocurr, tf_c)

        # Used normal boiling point for calculations
        if self.exp_nbt is not None:
            tb = self.exp_nbt
        else:
            tb = self.normal_boiling_point

        # Critical temperature (Tc) normal boiling temperature for calculations
        self.critical_temperature = tb * (
            0.584 + 0.965 * np.dot(ocurr, tc_c) - (np.dot(ocurr, tc_c)) ** 2
        ) ** (-1)

        # Critical pressure (Pc)
        self.critical_pressure = (
            0.113 + 0.0032 * np.dot(ocurr, numa_c) - np.dot(ocurr, pc_c)
        ) ** (-2)

        # Critical volume (Vc)
        self.critical_volume = 17.5 + np.dot(ocurr, vc_c)

        # Standard enthalpy of formation (298 K)
        self.h_formation = 68.29 + np.dot(ocurr, hform_c)

        # Standard Gibbs energy of formation (298 K)
        self.g_formation = 53.88 + np.dot(ocurr, gform_c)

        # Enthalpy of vaporization
        self.h_vaporization = 15.30 + np.dot(ocurr, hvap_c)

        # =====================================================================
        # Incomplete contribution properties (some contribution missing)
        # =====================================================================
        # Heat capacity
        if "-N= (ring)" not in groups:
            a_c = df["a"].to_numpy()
            b_c = df["b"].to_numpy()
            c_c = df["c"].to_numpy()
            d_c = df["d"].to_numpy()

            a = np.dot(ocurr, a_c) - 37.93
            b = np.dot(ocurr, b_c) + 0.21
            c = np.dot(ocurr, c_c) - 3.91e-4
            d = np.dot(ocurr, d_c) + 2.06e-7

            self.heat_capacity_ideal_gas_params = np.array([a, b, c, d])

        # Enthalpy of fusion
        if all(df["Hfusion"].notnull()):
            hfusion_c = df["Hfusion"].to_numpy()
            self.h_fusion = -0.88 + np.dot(ocurr, hfusion_c)

        # Liquid viscosity
        if all(df["na"].notnull()):
            na_c = df["na"].to_numpy()
            nb_c = df["nb"].to_numpy()

            self.sum_na = np.dot(ocurr, na_c)
            self.sum_nb = np.dot(ocurr, nb_c)

        # =====================================================================
        # Extra properties
        # =====================================================================
        # Reduced normal boiling point temperature
        t_br = tb / self.critical_temperature

        # Lee and Kesler's equation (acentric factor)
        pc = self.critical_pressure
        self.acentric_factor = (
            -np.log(pc)
            - 5.92714
            + 6.09648 / t_br
            + 1.28862 * np.log(t_br)
            - 0.169347 * t_br**6
        ) / (
            15.2518
            - 15.6875 / t_br
            - 13.4721 * np.log(t_br)
            + 0.43577 * t_br**6
        )

        # Riedel-Plank-Miller equation (vapor pressure [bar])
        h = t_br * np.log(self.critical_pressure / 1.01325) / (1 - t_br)

        g = 0.4835 + 0.4605 * h

        k = (h / g - (1 + t_br)) / ((3 + t_br) * (1 - t_br) ** 2)

        self.vapor_pressure_params = {"G": g, "k": k}
