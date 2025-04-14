import re
from dataclasses import dataclass
from typing import TypedDict, Optional,Union

_N_NUMBER_REGEX = re.compile(r"^N[1-9][0-9]{0,4}[A-HJ-NP-Z]{0,2}$")

class AircraftData(TypedDict, total=False):
    type: Optional[str]
    icao_type: Optional[str]
    manufacturer: Optional[str]
    mode_s: Optional[str]
    registration: Optional[str]
    registered_owner_country_iso_name: Optional[str]
    registered_owner_country_name: Optional[str]
    registered_owner_operator_flag_code: Optional[str]
    registered_owner: Optional[str]
    url_photo: Optional[str]
    url_photo_thumbnail: Optional[str]

class ErrorResponse(TypedDict):
    error: str

class AirlineInfo(TypedDict):
    name: str
    icao: str
    iata: Optional[str]
    country: str
    country_iso: str
    callsign: Optional[str]


class AirportInfo(TypedDict):
    country_iso_name: str
    country_name: str
    elevation: float
    iata_code: str
    icao_code: str
    latitude: float
    longitude: float
    municipality: str
    name: str


class FlightRoute(TypedDict):
    callsign: str
    callsign_icao: Optional[str]
    callsign_iata: Optional[str]
    airline: Optional[AirlineInfo]
    origin: AirportInfo
    destination: AirportInfo


class FlightRouteResponseData(TypedDict):
    flightroute: FlightRoute


class FlightRouteResponse(TypedDict):
    response: FlightRouteResponseData

@dataclass(frozen=True)
class NNumber:
    value: str

    @classmethod
    def create(cls, value: str) -> Union["NNumber", ErrorResponse]:
        if not _N_NUMBER_REGEX.fullmatch(value):
            return {
                "error": "Invalid N-Number format. It must start with 'N', not begin with zero, and use valid characters."
            }
        return cls(value)

@dataclass(frozen=True)
class ModeSCode:
    value: str

    @classmethod
    def create(cls, value: str) -> Union["ModeSCode", ErrorResponse]:
        if not re.fullmatch(r"[0-9A-Fa-f]{6}", value):
            return {
                "error": "Mode-S code must be exactly 6 hexadecimal characters."
            }
        return cls(value)