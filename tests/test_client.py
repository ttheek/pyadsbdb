import pytest
import requests
from pyadsbdb import Client

@pytest.fixture
def client():
    """Fixture to create a Client instance."""
    return Client()

def test_get_aircraft_data(mocker, client):
    mock_response = {"response": "aircraft data"}
    mocker.patch("requests.get", return_value=mocker.Mock(status_code=200, json=lambda: mock_response))

    result = client.get_aircraft_data("A1B2C3")
    assert result == mock_response

def test_get_flight_route(mocker, client):
    mock_response = {"response": "route data"}
    mocker.patch("requests.get", return_value=mocker.Mock(status_code=200, json=lambda: mock_response))

    result = client.get_flight_route("BA123")
    assert result == mock_response

def test_get_airline_valid_code(mocker, client):
    mock_response = {"response": [{"name": "Test Airline", "icao": "TST", "iata": None, "country": "Testland"}]}
    mocker.patch("requests.get", return_value=mocker.Mock(status_code=200, json=lambda: mock_response))

    result = client.get_airline("TST")
    assert result == mock_response

def test_get_airline_invalid_code(client):
    result = client.get_airline("TEST")
    assert "error" in result
    assert result["error"] == "Airline code must be at most 3 characters long."

def test_mode_s_to_n_number_valid(mocker, client):
    mock_response = {"response": "N12345"}
    mocker.patch("requests.get", return_value=mocker.Mock(status_code=200, json=lambda: mock_response))

    result = client.mode_s_to_n_number("A1B2C3")
    assert result == mock_response

def test_mode_s_to_n_number_invalid(client):
    result = client.mode_s_to_n_number("12345G")
    assert "error" in result
    assert result["error"] == "Mode-S code must be exactly 6 hexadecimal characters."

def test_n_number_to_mode_s_valid(mocker, client):
    mock_response = {"response": "A1B2C3"}
    mocker.patch("requests.get", return_value=mocker.Mock(status_code=200, json=lambda: mock_response))

    result = client.n_number_to_mode_s("N12345")
    assert result == mock_response

def test_n_number_to_mode_s_invalid(client):
    result = client.n_number_to_mode_s("01234Z")
    assert "error" in result
    assert result["error"] == "Invalid N-Number format. It must start with 'N', not begin with zero, and use valid characters."

def test_get_online_status(mocker, client):
    mock_response = {"response": {"uptime": 12345, "api_version": "0.4.1"}}
    mocker.patch("requests.get", return_value=mocker.Mock(status_code=200, json=lambda: mock_response))

    result = client.get_online_status()
    assert result == mock_response
