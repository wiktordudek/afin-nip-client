from typing import Self

import requests

from .constants import API_URL
from .exceptions import (
    AfinApiError,
    EmptyResponse,
    InvalidNipError,
    InvalidResponse,
    NipChecksumError,
    NipLengthError,
)
from .models import Address, AdministrativeArea, CompanyInfo, EntityClassification


class AfinClient:
    def __init__(
        self,
        timeout: float = 10.0,
    ) -> None:
        self.timeout = timeout
        self.session = requests.Session()

    def _clean_nip(
        self,
        nip: str | int,
    ) -> str:
        return "".join(ch for ch in str(nip) if ch.isdigit())

    def validate(
        self,
        nip: str,
    ) -> bool:
        if len(nip) != 10:
            raise NipLengthError

        weights: tuple[int, ...] = (6, 5, 7, 2, 3, 4, 5, 6, 7)
        checksum: int = sum(w * int(d) for w, d in zip(weights, nip)) % 11
        if checksum != 10 and checksum == int(nip[9]):
            return True
        raise NipChecksumError

    def _parse_response(
        self,
        text: str,
    ) -> CompanyInfo:
        text = text.strip()

        if not text:
            raise EmptyResponse

        if text.startswith("#"):
            message: str = text.lstrip("#").strip()
            raise InvalidNipError(message)

        fields: list[str] = [f.strip() for f in text.split(", ")]

        if len(fields) < 12:
            raise InvalidResponse

        (
            regon,
            nip,
            name,
            voivodeship,
            county,
            community,
            city,
            postal_code,
            street,
            building_number,
            entity_type,
            silos_code,
            *optional,
        ) = fields

        return CompanyInfo(
            regon=regon,
            nip=nip,
            name=name,
            address=Address(
                street=street,
                building_number=building_number,
                postal_code=postal_code,
                city=city,
                post_office=optional[0] or None if optional else None,
            ),
            area=AdministrativeArea(
                voivodeship=voivodeship,
                county=county,
                community=community,
            ),
            classification=EntityClassification(
                entity_type_raw=entity_type,
                silos_code_raw=silos_code,
            ),
        )

    def get(
        self,
        nip: str | int,
    ) -> CompanyInfo:
        _nip: str = self._clean_nip(nip)

        self.validate(_nip)

        try:
            response: requests.Response = self.session.get(
                API_URL,
                params={"nip": _nip},
                timeout=self.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as e:
            raise AfinApiError(e) from e

        # The server returns only "Content-Type: text/plain"
        # without charset, so we need to enforce UTF-8 to
        # avoid mojibake
        response.encoding = response.apparent_encoding or "utf-8"

        company_info: CompanyInfo = self._parse_response(response.text)
        return company_info

    def close(self) -> None:
        self.session.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type,
        exc,
        tb,
    ) -> None:
        self.close()
