import re
from dataclasses import dataclass
from typing import TypedDict, Optional,Union

_N_NUMBER_REGEX = re.compile(r"^N[1-9][0-9]{0,4}[A-HJ-NP-Z]{0,2}$")

class Aircraft:
    def __init__(
        self,
        type: str,
        icao_type: str,
        manufacturer: str,
        mode_s: str,
        registration: str,
        registered_owner_country_iso_name: str,
        registered_owner_country_name: str,
        registered_owner_operator_flag_code: Optional[str],
        registered_owner: str,
        url_photo: Optional[str],
        url_photo_thumbnail: Optional[str]
    ):
        self.type = type
        self.icao_type = icao_type
        self.manufacturer = manufacturer
        self.mode_s = mode_s
        self.registration = registration
        self.registered_owner_country_iso_name = registered_owner_country_iso_name
        self.registered_owner_country_name = registered_owner_country_name
        self.registered_owner_operator_flag_code = registered_owner_operator_flag_code
        self.registered_owner = registered_owner
        self.url_photo = url_photo
        self.url_photo_thumbnail = url_photo_thumbnail

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

class ErrorResponse(TypedDict):
    error: str

class Airline:
    def __init__(
        self,
        name: str,
        icao: str,
        iata: Optional[str],
        country: str,
        country_iso: str,
        callsign: Optional[str]
    ):
        self.name = name
        self.icao = icao
        self.iata = iata
        self.country = country
        self.country_iso = country_iso
        self.callsign = callsign

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            name=data.get("name", "None"),
            icao=data.get("icao", "None"),
            iata=data.get("iata", "None"),
            country=data.get("country", "None"),
            country_iso=data.get("country_iso", "None"),
            callsign=data.get("callsign", "None")
        )


class Airport:
    def __init__(
        self,
        name: str,
        icao: str,
        iata: str,
        latitude: float,
        longitude: float,
        elevation: float,
        municipality: str,
        country_iso_name: str,
        country_name: str
    ):
        self.name = name
        self.icao = icao
        self.iata = iata
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.municipality = municipality
        self.country_iso_name = country_iso_name
        self.country_name = country_name

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


class FlightRoute:
    def __init__(
        self,
        callsign: str,
        callsign_icao: Optional[str],
        callsign_iata: Optional[str],
        airline: Optional[Airline],
        origin: Airport,
        destination: Airport
    ):
        self.callsign = callsign
        self.callsign_icao = callsign_icao
        self.callsign_iata = callsign_iata
        self.airline = airline
        self.origin = origin
        self.destination = destination

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)



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