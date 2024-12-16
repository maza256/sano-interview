from datetime import date

import pytest

from ..models.models import AlleleEnum, ChromosomeEnum, GeneticData, User


def test_genetic_data_init():
    genetic_data = GeneticData(
        variant_id="some_variant",
        chromosome=ChromosomeEnum.CHRX,
        position=100,
        reference_allele=AlleleEnum.A,
        alternate_allele=AlleleEnum.C,
        alternate_allele_frequency=0.5,
    )

    assert genetic_data.variant_id == "some_variant"
    assert genetic_data.chromosome == ChromosomeEnum.CHRX
    assert genetic_data.position == 100
    assert genetic_data.reference_allele == AlleleEnum.A
    assert genetic_data.alternate_allele == AlleleEnum.C
    assert genetic_data.alternate_allele_frequency == 0.5


def test_genetic_data_init_invalid_type():
    with pytest.raises(ValueError):
        genetic_data = GeneticData(
            variant_id="some_variant",
            chromosome="invalid_chromosome",
            position=100,
            reference_allele=AlleleEnum.A,
            alternate_allele=AlleleEnum.C,
            alternate_allele_frequency=0.5,
        )
        assert genetic_data.chromosome == "invalid_chromosome"


def test_user_init():
    user = User(username="john_doe", date_created=date(2022, 1, 1), id=123)

    assert user.username == "john_doe"
    assert user.date_created == date(2022, 1, 1)
    assert user.id == 123
