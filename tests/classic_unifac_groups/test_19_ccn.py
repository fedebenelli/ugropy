import pytest

import ugropy as ug


# =============================================================================
# 19- CCN Main group: CH3CN, CH2CN
# =============================================================================

# UNIFAC
trials_unifac = [
    ("acetonitrile", {"CH3CN": 1}, "name"),
    ("propionitrile", {"CH3": 1, "CH2CN": 1}, "name"),
]


@pytest.mark.CCN
@pytest.mark.UNIFAC
@pytest.mark.parametrize("identifier, result, identifier_type", trials_unifac)
def test_ccn_unifac(identifier, result, identifier_type):
    groups = ug.Groups(identifier, identifier_type)
    assert groups.unifac_groups == result
    assert groups.psrk_groups == result
