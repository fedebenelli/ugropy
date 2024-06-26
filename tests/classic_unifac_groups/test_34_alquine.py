import pytest

from ugropy import constantinou_gani_primary, get_groups, psrk, unifac
from ugropy.core import fit_atoms


# =============================================================================
# 34- C=-C Main group: CH=-C, C=-C
# =============================================================================

# UNIFAC
trials_unifac = [
    ("CC#CC1=CC=CC=C1", {"ACH": 5, "AC": 1, "C=-C": 1, "CH3": 1}, "smiles"),
    # 1-hexyne
    ("CCCCC#C", {"CH3": 1, "CH2": 3, "CH=-C": 1}, "smiles"),
    # 2-hexyne
    ("CCCC#CC", {"CH3": 2, "CH2": 2, "C=-C": 1}, "smiles"),
]


@pytest.mark.UNIFAC
@pytest.mark.parametrize("identifier, result, identifier_type", trials_unifac)
def test_alquine_unifac(identifier, result, identifier_type):
    mol = get_groups(unifac, identifier, identifier_type)
    assert mol.subgroups == result
    assert fit_atoms(mol.mol_object, mol.subgroups, unifac) != {}


@pytest.mark.PSRK
@pytest.mark.parametrize("identifier, result, identifier_type", trials_unifac)
def test_alquine_psrk(identifier, result, identifier_type):
    mol = get_groups(psrk, identifier, identifier_type)
    assert mol.subgroups == result
    assert fit_atoms(mol.mol_object, mol.subgroups, psrk) != {}


@pytest.mark.ConstantinouGani
@pytest.mark.parametrize("identifier, result, identifier_type", trials_unifac)
def test_alquine_cg(identifier, result, identifier_type):
    mol = get_groups(constantinou_gani_primary, identifier, identifier_type)
    assert mol.subgroups == result
    assert (
        fit_atoms(mol.mol_object, mol.subgroups, constantinou_gani_primary)
        != {}
    )
