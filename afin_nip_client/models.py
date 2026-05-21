from dataclasses import asdict, dataclass
from enum import StrEnum


class EntityType(StrEnum):  # "Typ" w BIR1
    LEGAL = "P"  # osoba (P)rawna
    NATURAL = "F"  # osoba (F)izyczna prowadząca działalność
    LEGAL_LOCAL = "LP"  # jednostka (L)okalna osoby (P)rawnej
    NATURAL_LOCAL = "LF"  # jednostka (L)okalna osoby (F)izycznej


class SilosKind(StrEnum):  # "SilosID" w BIR1
    CEIDG = "1"  # działalność zarejestrowana w CEIDG
    AGRICULTURAL = "2"  # działalność rolnicza
    OTHER = "3"  # działalność pozostała (komornik, notariusz, agroturystyka)
    HISTORICAL = "4"  # działalność skreślona w starym KRUPGN (przed 2014-11-08)
    LEGAL_ENTITY = "6"  # działalność jednostki prawnej


@dataclass(frozen=True)
class Address:
    street: str
    building_number: str
    postal_code: str
    city: str
    post_office: str | None = None

    def __str__(self) -> str:
        return f"{self.street} {self.building_number}, {self.postal_code} {self.city}".strip()


@dataclass(frozen=True)
class AdministrativeArea:
    voivodeship: str  # województwo
    county: str  # powiat
    community: str  # gmina

    def __str__(self) -> str:
        return f"{self.voivodeship} / {self.county} / {self.community}".strip()


@dataclass(frozen=True)
class EntityClassification:
    entity_type_raw: str  # raw value to be mapped by EntityType enum
    silos_code_raw: str  # raw value to be mapped by SilosKind enum

    @property
    def entity_type(self) -> EntityType | None:
        try:
            return EntityType(self.entity_type_raw)
        except ValueError:
            return None

    @property
    def silos(self) -> SilosKind | None:
        try:
            return SilosKind(self.silos_code_raw)
        except ValueError:
            return None

    @property
    def is_legal_entity(self) -> bool:
        return self.entity_type in (EntityType.LEGAL, EntityType.LEGAL_LOCAL)

    @property
    def is_natural_person(self) -> bool:
        return self.entity_type in (EntityType.NATURAL, EntityType.NATURAL_LOCAL)


@dataclass
class CompanyInfo:
    regon: str
    nip: str
    name: str

    address: Address
    area: AdministrativeArea
    classification: EntityClassification

    def to_dict(self) -> dict:
        return asdict(self)
