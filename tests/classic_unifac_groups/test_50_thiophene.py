import pytest

from ugropy import constantinou_gani_primary, get_groups, psrk, unifac
from ugropy.core import fit_atoms


# =============================================================================
# 50- thiophene Main group: C4H4S, C4H3S, C4H2S
# =============================================================================

# UNIFAC
trials_unifac = [
    # 2,3-dimethylthiophene
    ("OC1=CSC=C1", {"C4H3S": 1, "OH": 1}, "smiles"),
    ("CC1=C(SC=C1)C", {"C4H2S": 1, "CH3": 2}, "smiles"),
    # thiophene
    ("C1=CSC=C1", {"C4H4S": 1}, "smiles"),
    # 2-methylthiophene
    ("CC1=CC=CS1", {"C4H3S": 1, "CH3": 1}, "smiles"),
    ("OC1=CC=CS1", {"C4H3S": 1, "OH": 1}, "smiles"),
    ("OC1=CSC=C1O", {"C4H2S": 1, "OH": 2}, "smiles"),
    ("OC1=CC(O)=CS1", {"C4H2S": 1, "OH": 2}, "smiles"),
    ("OC1=CC=C(O)S1", {"C4H2S": 1, "OH": 2}, "smiles"),
]


@pytest.mark.UNIFAC
@pytest.mark.parametrize("identifier, result, identifier_type", trials_unifac)
def test_thiophene_unifac(identifier, result, identifier_type):
    mol = get_groups(unifac, identifier, identifier_type)
    assert mol.subgroups == result
    assert fit_atoms(mol.mol_object, mol.subgroups, unifac) != {}


@pytest.mark.PSRK
@pytest.mark.parametrize("identifier, result, identifier_type", trials_unifac)
def test_thiophene_psrk(identifier, result, identifier_type):
    mol = get_groups(psrk, identifier, identifier_type)
    assert mol.subgroups == result
    assert fit_atoms(mol.mol_object, mol.subgroups, psrk) != {}


@pytest.mark.ConstantinouGani
@pytest.mark.parametrize("identifier, result, identifier_type", trials_unifac)
def test_thiophene_cg(identifier, result, identifier_type):
    mol = get_groups(constantinou_gani_primary, identifier, identifier_type)

    if identifier != "C1=CSC=C1":
        assert mol.subgroups == result
        assert (
            fit_atoms(mol.mol_object, mol.subgroups, constantinou_gani_primary)
            != {}
        )
    else:
        assert mol.subgroups == {}
