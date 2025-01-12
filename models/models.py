from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Set


class ChromosomeEnum(Enum):
    CHRX = "X"
    CHRY = "Y"
    CHR1 = "1"
    CHR2 = "2"


class AlleleEnum(Enum):
    A = "A"
    C = "C"
    G = "G"
    T = "T"


@dataclass
class GeneticData:
    variant_id: str
    chromosome: ChromosomeEnum
    position: int
    reference_allele: AlleleEnum
    alternate_allele: AlleleEnum
    alternate_allele_frequency: float

    def __post_init__(self) -> None:
        supported_chromosomes: Set[ChromosomeEnum] = set()
        supported_alleles: Set[AlleleEnum] = set()

        for memberC in ChromosomeEnum.__members__.values():
            if memberC is not None:
                supported_chromosomes.add(memberC)

        for member in AlleleEnum.__members__.values():
            if member is not None:
                supported_alleles.add(member)

        if self.chromosome not in supported_chromosomes:
            raise ValueError(f"Unsupported chromosome value: {self.chromosome}")

        if self.reference_allele not in supported_alleles:
            raise ValueError(f"Unsupported allele value: {self.reference_allele}")

        if self.alternate_allele not in supported_alleles:
            raise ValueError(f"Unsupported allele value: {self.reference_allele}")


@dataclass
class User:
    username: str
    date_created: date
    id: int


class HeaderOrder(Enum):
    variant_id = "Variant ID"
    chromosome = "Chromosome"
    position = "Position on chromosome"
    reference_allele = "Reference allele"
    alternate_allele = "Alternate allele"
    alternate_allele_frequency = "Alternate allele frequency"
