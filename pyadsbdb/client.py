import requests
import re
from typing import Union, Optional
from .types import Aircraft, Airline, ErrorResponse, NNumber,ModeSCode

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

    def get_aircraft_data(self, identifier: str) -> Union[Aircraft, ErrorResponse]:
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
        try:
            return Aircraft.from_dict(aircraft_data)
        except Exception as e:
            return {"error": f"Failed to parse aircraft data: {str(e)}"}

    def get_flight_route(self, callsign: str):
        """
        Retrieves the flight route information for a given callsign.

        Args:
            callsign (str): The callsign of the flight to retrieve route information for.

        Returns:
            dict or str: The flight route information as a dictionary if the request is successful,
                         or an error message string if the callsign validation fails.
        """
        if (err := self._validate_str(callsign, "Callsign")):
            return err
        return self._get(f"callsign/{callsign}")

    def get_airline(self, airline_code: str) -> Union[Airline, ErrorResponse]:
        """
        Retrieve information about an airline using its airline code.

        Args:
            airline_code (str): The IATA airline code (maximum length of 3 characters).

        Returns:
            Union[dict, ErrorResponse]: A dictionary containing airline information if the request is successful,
            or an ErrorResponse object if there is an error.
        """
        if (err := self._validate_str(airline_code, "Airline code", max_len=3)):
            return err
        response = self._get(f"airline/{airline_code}")
        if "error" in response:
            return {"error": response["error"]}
        airline_data = response.get("response", [])[0]
        if not isinstance(airline_data, dict):
            return {"error": "Invalid airline data format."}
        try:
            return Airline.from_dict(airline_data)
        except Exception as e:
            return {"error": f"Failed to parse airline data: {str(e)}"}

    def modeS2nNumber(self, mode_s: str) -> Union[str, ErrorResponse]:
        """
        Converts a Mode-S code to an N-Number (aircraft registration number).
        Args:
            mode_s (str): The Mode-S code to be converted. It must be a string of length 6.
        Returns:
            Union[str, ErrorResponse]: 
                - If successful, returns the N-Number as a string.
                - If an error occurs during validation or processing, returns an ErrorResponse.
        """

        if (err := self._validate_str(mode_s, "Mode-S code", 6)):
            return err

        result = ModeSCode.create(mode_s)
        if isinstance(result, dict):
            return result

        response: dict = self._get(f"{self.BASE_URL}/mode-s/{result.value}")
        n_number = response.get("response")
        if isinstance(n_number, str) and n_number.startswith('N'):
            return n_number
        return {"error": f"Invalid Mode-S {mode_s}"}


    def nNumber2ModeS(self, n_number: str) -> Union[dict, ErrorResponse]:
        """
        Converts an N-Number (aircraft registration number) to its corresponding Mode S code.
        Args:
            n_number (str): The N-Number (aircraft registration number) to be converted.
        Returns:
            Union[dict, ErrorResponse]: 
                - A dictionary containing the Mode S code if the conversion is successful.
                - An ErrorResponse object if the input validation or conversion fails.
        """
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
