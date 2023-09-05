import pytest

import ugropy as ug


# =============================================================================
# 1- CH2 Main group: CH3, CH2, CH, C
# =============================================================================
# UNIFAC
trials_unifac = [
    ("C1CC2CCCC3CCCC1C23", {"CH2": 8, "CH": 4}, "smiles"),
    ("C1C2CCCCC2C2CCCCC12", {"CH2": 9, "CH": 4}, "smiles"),
    ("C1C2CC1CCCC2", {"CH2": 6, "CH": 2}, "smiles"),
    ("C1CCCCCCCC1", {"CH2": 9}, "smiles"),
    ("C1CCCCCCCC1", {"CH2": 9}, "smiles"),
    ("C1C2CC3CC1CC(C2)C3", {"CH2": 6, "CH": 4}, "smiles"),
    ("C12C3C1C1C2C31", {"CH": 6}, "smiles"),
    ("C1CC2CC1CCC2", {"CH2": 6, "CH": 2}, "smiles"),
    ("C1CC2CC3CCC2CC13", {"CH2": 6, "CH": 4}, "smiles"),
    ("C12C3C4C1C1C2C3C41", {"CH": 8}, "smiles"),
    ("C1CC1", {"CH2": 3}, "smiles"),
    ("C1CCC1", {"CH2": 4}, "smiles"),
    ("C1C2CC1CCCC2", {"CH2": 6, "CH": 2}, "smiles"),
    # the space ship
    ("CC12C3CCC4CCC1C234", {"CH3": 1, "CH2": 4, "CH": 3, "C": 2}, "smiles"),
    ("CCC(CC)C(C)(C)C", {"CH3": 5, "CH2": 2, "CH": 1, "C": 1}, "smiles"),
    ("C1CCC2CCCCC2C1", {"CH2": 8, "CH": 2}, "smiles"),
    ("C1CCC(CC1)CC2CCCCC2", {"CH2": 11, "CH": 2}, "smiles"),
    ("ethane", {"CH3": 2}, "name"),
    ("hexane", {"CH3": 2, "CH2": 4}, "name"),
    ("2-methylpropane", {"CH3": 3, "CH": 1}, "name"),
    ("2,2-dimethylpropane", {"CH3": 4, "C": 1}, "name"),
    ("cyclohexane", {"CH2": 6}, "name"),
]


@pytest.mark.CH2
@pytest.mark.UNIFAC
@pytest.mark.parametrize("identifier, result, identifier_type", trials_unifac)
def test_ch2(identifier, result, identifier_type):
    groups = ug.Groups(identifier, identifier_type)
    assert groups.unifac_groups == result
