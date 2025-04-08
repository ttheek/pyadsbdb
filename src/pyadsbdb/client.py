import requests
import re
from typing import Union, Optional

class Client:
    BASE_URL = "https://api.adsbdb.com/v0"

    def __init__(self):
        pass

    def _validate_str(self, value: Union[str, None], name: str, max_len: Optional[int] = None) -> Union[None, dict]:
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

    def get_aircraft_data(self, identifier: str):
        if (err := self._validate_str(identifier, "Identifier")):
            return err
        return self._get(f"aircraft/{identifier}")

    def get_flight_route(self, callsign: str):
        if (err := self._validate_str(callsign, "Callsign")):
            return err
        return self._get(f"callsign/{callsign}")

    def get_airline(self, airline_code: str) -> dict:
        if (err := self._validate_str(airline_code, "Airline code", max_len=3)):
            return err
        return self._get(f"airline/{airline_code}")

    def mode_s_to_n_number(self, mode_s: str) -> dict:
        if (err := self._validate_str(mode_s, "Mode-S code")):
            return err
        if not re.fullmatch(r"[0-9A-Fa-f]{6}", mode_s):
            return {"error": "Mode-S code must be exactly 6 hexadecimal characters."}
        return self._get(f"{self.BASE_URL}/mode-s/{mode_s}")

    def n_number_to_mode_s(self, n_number: str) -> dict:
        if (err := self._validate_str(n_number, "N-Number")):
            return err
        if not re.fullmatch(r"[N][1-9][0-9]{0,4}[A-HJ-NP-Z]{0,2}", n_number):
            return {"error": "Invalid N-Number format. It must start with 'N', not begin with zero, and use valid characters."}
        return self._get(f"{self.BASE_URL}/n-number/{n_number}")

    def get_online_status(self) -> dict:
        return self._get(f"{self.BASE_URL}/online")

if __name__ == "__main__":
    client = Client()
    online_status = client.get_online_status()
    print("online:", online_status)
