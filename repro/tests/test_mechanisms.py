from repro.src.verify_mechanisms import interval_symmetric_difference_mass, mass


def test_normal_interval_mass_is_in_unit_range() -> None:
    assert 0.0 < mass([(-1.0, 1.0)]) < 1.0


def test_same_interval_has_zero_symmetric_difference() -> None:
    interval = [(-1.0, 0.2), (0.8, 1.3)]
    assert interval_symmetric_difference_mass(interval, interval) == 0.0
