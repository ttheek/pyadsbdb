import requests
import re

class Client:
    BASE_URL = "https://api.adsbdb.com/v0"

    def __init__(self):
        pass

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
        """Fetch aircraft data by Mode S code or registration number."""
        if not isinstance(identifier, str) or not identifier.strip():
            return {"error": "Identifier must be a non-empty string."}
        return self._get(f"aircraft/{identifier}")

    def get_flight_route(self, callsign: str):
        """Fetch flight route data by callsign."""
        if not isinstance(callsign, str) or not callsign.strip():
            return {"error": "Callsign must be a non-empty string."}
        return self._get(f"callsign/{callsign}")

    def get_airline(self, airline_code: str) -> dict:
        """Fetch Airline data by an Airline's ICAO or IATA short code (max 3 characters)."""
        if not isinstance(airline_code, str) or not airline_code.strip():
            return {"error": "Airline code must be a non-empty string."}
        if len(airline_code) > 3:
            return {"error": "Airline code must be at most 3 characters long."}
        return self._get(f"airline/{airline_code}")

    def mode_s_to_n_number(self, mode_s: str) -> dict:
        """Convert a MODE-S string to an N-Number string."""
        if not isinstance(mode_s, str) or not mode_s.strip():
            return {"error": "Mode-S code must be a non-empty string."}
        if not re.fullmatch(r"[0-9A-Fa-f]{6}", mode_s):
            return {"error": "Mode-S code must be exactly 6 hexadecimal characters."}
        return self._get(f"{self.BASE_URL}/mode-s/{mode_s}")

    def n_number_to_mode_s(self, n_number: str) -> dict:
        """Convert an N-Number string to a MODE-S string."""
        if not isinstance(n_number, str) or not n_number.strip():
            return {"error": "N-Number must be a non-empty string."}
        if not re.fullmatch(r"[N][1-9][0-9]{0,4}[A-HJ-NP-Z]{0,2}", n_number):
            return {"error": "Invalid N-Number format. It must start with 'N', not begin with zero, and use valid characters."}
        return self._get(f"{self.BASE_URL}/n-number/{n_number}")

    def get_online_status(self) -> dict:
        """Get the online status of the API."""
        return self._get(f"{self.BASE_URL}/online")

if __name__ == "__main__":
    client = Client()
    online_status = client.get_online_status()
    print("online:", online_status)
