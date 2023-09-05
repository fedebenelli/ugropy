import pytest

import ugropy as ug


# =============================================================================
# 10- CHO Main group (aldehyde): CHO
# =============================================================================

# UNIFAC
trials_unifac = [
    ("C(=O)C=O", {"CHO": 2}, "smiles"),
    # salicylaldehyde
    (
        "C1=CC=C(C(=C1)C=O)O",
        {"ACH": 4, "ACOH": 1, "AC": 1, "CHO": 1},
        "smiles",
    ),
    # 2-Methyl-3-butenal
    ("CC(C=C)C=O", {"CH3": 1, "CH": 1, "CH2=CH": 1, "CHO": 1}, "smiles"),
    # Cinnamaldehyde
    (
        "C1=CC=C(C=C1)C=CC=O",
        {"ACH": 5, "AC": 1, "CH=CH": 1, "CHO": 1},
        "smiles",
    ),
    # benzaldehyde
    ("C1=CC=C(C=C1)C=O", {"ACH": 5, "AC": 1, "CHO": 1}, "smiles"),
    # cyclohexanecarbaldehyde
    (
        "C1CCC(CC1)C=O",
        {
            "CH2": 5,
            "CH": 1,
            "CHO": 1,
        },
        "smiles",
    ),
    # pentanal
    ("CCCCC=O", {"CH3": 1, "CH2": 3, "CHO": 1}, "smiles"),
    # 3-methylbutanal
    ("CC(C)CC=O", {"CH3": 2, "CH2": 1, "CH": 1, "CHO": 1}, "smiles"),
    ("acetaldehyde", {"CH3": 1, "CHO": 1}, "name"),
    (
        "2-Hexyl-3-Phenyl-2-Propenal",
        {"ACH": 5, "AC": 1, "CH=C": 1, "CH2": 5, "CH3": 1, "CHO": 1},
        "name",
    ),
]


@pytest.mark.CHO
@pytest.mark.UNIFAC
@pytest.mark.parametrize("identifier, result, identifier_type", trials_unifac)
def test_cho_unifac(identifier, result, identifier_type):
    groups = ug.Groups(identifier, identifier_type)
    assert groups.unifac_groups == result
