import pytest

import ugropy as ug


# =============================================================================
# 4- ACCH2 Main group: ACCH3, ACCH2, ACCH
# =============================================================================

# UNIFAC
trials_unifac = [
    # Atrolactic acid
    (
        "CC(C1=CC=CC=C1)(C(=O)O)O",
        {"ACH": 5, "AC": 1, "OH": 1, "CH3": 1, "C": 1, "COOH": 1},
        "smiles",
    ),
    # 1-Phenyl-2-methyl-1,3-butadiene
    (
        "CC(=CC1=CC=CC=C1)C=C",
        {"ACH": 5, "AC": 1, "CH=C": 1, "CH2=CH": 1, "CH3": 1},
        "smiles",
    ),
    # 9-(3-Butenyl)anthracene
    (
        "C=CCCC1=C2C=CC=CC2=CC3=CC=CC=C31",
        {"ACH": 9, "ACCH2": 1, "AC": 4, "CH2": 1, "CH2=CH": 1},
        "smiles",
    ),
    # 9-Methylanthracene
    (
        "CC1=C2C=CC=CC2=CC3=CC=CC=C13",
        {"ACH": 9, "ACCH3": 1, "AC": 4},
        "smiles",
    ),
    # 3-Methylbiphenyl
    ("CC1=CC(=CC=C1)C2=CC=CC=C2", {"ACH": 9, "ACCH3": 1, "AC": 2}, "smiles"),
    # 1,2,4-Trimethyl-3-Ethylbenzene
    (
        "CCC1=C(C=CC(=C1C)C)C",
        {"ACH": 2, "ACCH3": 3, "ACCH2": 1, "CH3": 1},
        "smiles",
    ),
    # 1-t-Butyl-3-ethylbenzene
    (
        "CCC1=CC(=CC=C1)C(C)(C)C",
        {"ACH": 4, "ACCH2": 1, "CH3": 4, "AC": 1, "C": 1},
        "smiles",
    ),
    # 1-Ethyl-2,3-dimethylbenzene
    (
        "CCC1=CC=CC(=C1C)C",
        {"ACH": 3, "ACCH2": 1, "ACCH3": 2, "CH3": 1},
        "smiles",
    ),
    # 1-Ethyl-2-methylbenzene
    ("CCC1=CC=CC=C1C", {"ACH": 4, "ACCH3": 1, "ACCH2": 1, "CH3": 1}, "smiles"),
    # Benzene, 1-ethyl-4-(1-methylethyl)-
    (
        "CCC1=CC=C(C=C1)C(C)C",
        {"ACH": 4, "ACCH": 1, "ACCH2": 1, "CH3": 3},
        "smiles",
    ),
    ("Gastrodigenin", {"ACH": 4, "ACOH": 1, "ACCH2": 1, "OH": 1}, "name"),
    ("cumene", {"CH3": 2, "ACH": 5, "ACCH": 1}, "name"),
    ("ethylbenzene", {"CH3": 1, "ACH": 5, "ACCH2": 1}, "name"),
    ("toluene", {"ACH": 5, "ACCH3": 1}, "name"),
]


@pytest.mark.ACCH2
@pytest.mark.UNIFAC
@pytest.mark.parametrize("identifier, result, identifier_type", trials_unifac)
def test_acch2_unifac(identifier, result, identifier_type):
    groups = ug.Groups(identifier, identifier_type)
    assert groups.unifac_groups == result
    assert groups.psrk_groups == result
