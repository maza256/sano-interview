from datetime import date

import pytest

from ..models.models import AlleleEnum, ChromosomeEnum, GeneticData, User
from ..utils import file_parser


def test_valid_get_header_order():
    line = "#Variant ID,Position on chromosome,Chromosome,Reference allele,Alternate allele,Alternate allele frequency"
    result = file_parser.get_header_order(line)

    assert len(result) == 6
    assert result["variant_id"] == 0
    assert result["position"]   ==  1
    assert result ["chromosome"] == 2
    assert result["reference_allele"] == 3
    assert result["alternate_allele"] == 4
    assert result["alternate_allele_frequency"] ==  5


def test_invalid_start_get_header_order():
    line = "Variant ID,Position on chromosome,Chromosome,Reference allele,Alternate allele,Alternate allele frequency"
    with pytest.raises(AssertionError):
        file_parser.get_header_order(line)


def test_invalid_length_get_header_order():
    line = "#Position on chromosome,Chromosome,Reference allele,Alternate allele,Alternate allele frequency"
    with pytest.raises(AssertionError):
        file_parser.get_header_order(line)


def test_parse_file_to_genetic_data():
    with open("tests/individual123.sano") as f:
        contents = f.read().split("\n")
        expected_line_one_data = GeneticData(variant_id="rs12345",chromosome=ChromosomeEnum.CHR1,position=1234567,reference_allele=AlleleEnum.A,alternate_allele=AlleleEnum.G,alternate_allele_frequency=0.12)
        result = list(file_parser.parse_file_to_genetic_data(contents))
        assert result[0] == expected_line_one_data

def test_invalid_parse_file_to_genetic_data():
    with pytest.raises(TypeError):
        with open("tests/wrong_individual123.sano") as f:
            contents = f.read().split("\n")
            expected_line_one_data = GeneticData(variant_id="rs12345",chromosome=ChromosomeEnum.CHR1,position=1234567,reference_allele=AlleleEnum.A,alternate_allele=AlleleEnum.G,alternate_allele_frequency=0.12)
            result = list(file_parser.parse_file_to_genetic_data(contents))
            assert result[0] == expected_line_one_data
