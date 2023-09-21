import pytest

import ugropy as ug


# =============================================================================
# 36- ACRY Main group: ACRY
# =============================================================================

# UNIFAC
trials_unifac = [
    ("acrylonitrile", {"ACRY": 1}, "name"),
]


@pytest.mark.ACRY
@pytest.mark.UNIFAC
@pytest.mark.parametrize("identifier, result, identifier_type", trials_unifac)
def test_acry_unifac(identifier, result, identifier_type):
    groups = ug.Groups(identifier, identifier_type)
    assert groups.unifac_groups == result