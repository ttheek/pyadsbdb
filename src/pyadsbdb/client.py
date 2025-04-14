import requests
import re
from typing import Union, Optional
from .types import AircraftData, ErrorResponse, NNumber,ModeSCode

class Client:
    BASE_URL = "https://api.adsbdb.com/v0"

    def __init__(self):
        pass

    def _validate_str(self, value: Union[str, None], name: str, max_len: Optional[int] = None) -> Union[None, ErrorResponse]:
        if not isinstance(value, str) or not value.strip():
            return {"error": f"{name} must be a non-empty string."}
        if max_len is not None and len(value) > max_len:
            return {"error": f"{name} must be at most {max_len} characters long."}
        return None

    def _get(self, endpoint: str):
        """Helper method to send a GET request to the API."""
        url = f"{self.BASE_URL}/{endpoint}" if not endpoint.startswith("http") else endpoint
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 404:
                try:
                    return {"error": response.json().get("response", "not found")}
                except ValueError:
                    return {"error": "Resource not found (404)."}
            return {"error": f"HTTP error occurred: {http_err}"}
        except requests.exceptions.ConnectionError:
            return {"error": "Connection error occurred. Please check your network."}
        except requests.exceptions.Timeout:
            return {"error": "The request timed out."}
        except requests.exceptions.RequestException as req_err:
            return {"error": f"Request error occurred: {req_err}"}

    def get_aircraft_data(self, identifier: str) -> Union[AircraftData, ErrorResponse]:
        """
        Retrieve detailed aircraft data based on the provided identifier.

        Args:
            identifier (str): The unique identifier for the aircraft (e.g., Mode S code or registration).

        Returns:
            AircraftData: A dictionary containing aircraft data or an error message. The dictionary may include:
                - "type" (str): The type of the aircraft.
                - "icao_type" (str): The ICAO type designator of the aircraft.
                - "manufacturer" (str): The manufacturer of the aircraft.
                - "mode_s" (str): The Mode S transponder code of the aircraft.
                - "registration" (str): The registration number of the aircraft.
                - "registered_owner_country_iso_name" (str): The ISO name of the country where the aircraft is registered.
                - "registered_owner_country_name" (str): The full name of the country where the aircraft is registered.
                - "registered_owner_operator_flag_code" (str): The operator flag code of the registered owner.
                - "registered_owner" (str): The name of the registered owner of the aircraft.
                - "url_photo" (str): A URL to a photo of the aircraft.
                - "url_photo_thumbnail" (str): A URL to a thumbnail photo of the aircraft.
                - "error" (str): An error message if the request fails or the data is invalid.
        """
        if (err := self._validate_str(identifier, "Identifier")):
            return err
        response = self._get(f"aircraft/{identifier}")
        if "error" in response:
            return {"error": response["error"]}
        aircraft_data = response.get("aircraft", {})
        if not isinstance(aircraft_data, dict):
            return {"error": "Invalid aircraft data format."}
        return {
            "type": aircraft_data.get("type"),
            "icao_type": aircraft_data.get("icao_type"),
            "manufacturer": aircraft_data.get("manufacturer"),
            "mode_s": aircraft_data.get("mode_s"),
            "registration": aircraft_data.get("registration"),
            "registered_owner_country_iso_name": aircraft_data.get("registered_owner_country_iso_name"),
            "registered_owner_country_name": aircraft_data.get("registered_owner_country_name"),
            "registered_owner_operator_flag_code": aircraft_data.get("registered_owner_operator_flag_code"),
            "registered_owner": aircraft_data.get("registered_owner"),
            "url_photo": aircraft_data.get("url_photo"),
            "url_photo_thumbnail": aircraft_data.get("url_photo_thumbnail"),
        }

    def get_flight_route(self, callsign: str):
        if (err := self._validate_str(callsign, "Callsign")):
            return err
        return self._get(f"callsign/{callsign}")

    def get_airline(self, airline_code: str) -> Union[dict, ErrorResponse]:
        if (err := self._validate_str(airline_code, "Airline code", max_len=3)):
            return err
        return self._get(f"airline/{airline_code}")

    def mode_s_to_n_number(self, mode_s: str) -> Union[dict, ErrorResponse]:
        if (err := self._validate_str(mode_s, "Mode-S code", 6)):
            return err

        result = ModeSCode.create(mode_s)
        if isinstance(result, dict):  # ErrorResponse
            return result

        return self._get(f"{self.BASE_URL}/mode-s/{result.value}")


    def n_number_to_mode_s(self, n_number: str) -> Union[dict, ErrorResponse]:
        if (err := self._validate_str(n_number, "N-Number")):
            return err

        result = NNumber.create(n_number)
        if isinstance(result, dict):
            return result

        return self._get(f"{self.BASE_URL}/n-number/{result.value}")


    def get_online_status(self) -> Union[dict, ErrorResponse]:
        return self._get(f"{self.BASE_URL}/online")

if __name__ == "__main__":
    client = Client()
    online_status = client.get_online_status()
    print("online:", online_status)
