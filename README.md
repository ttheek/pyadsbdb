# pyadsbdb

<p align="center">
  <img src="https://github.com/mrjackwills/adsbdb/blob/main/.github/logo.svg" alt="ADSBDB Logo" width="150">
</p>

pyadsbdb is a Python wrapper for the [adsbdb](https://github.com/mrjackwills/adsbdb) API by [Jack Wills](https://github.com/mrjackwills), allowing easy access to aircraft, flight route, and airline data.

## Installation

Install the package using pip:
```sh
pip install pyadsbdb
```

## Usage

### Import and Initialize
```python
from pyadsbdb import Client

client = Client()
```

### Get Aircraft Data
```python
result = client.get_aircraft_data("A1B2C3")
print(result)
```

### Get Flight Route Data
```python
result = client.get_flight_route("BA123")
print(result)
```

### Get Airline Data
```python
result = client.get_airline("BA")
print(result)
```

### Convert Mode-S to N-Number
```python
result = client.mode_s_to_n_number("A1B2C3")
print(result)
```

### Convert N-Number to Mode-S
```python
result = client.n_number_to_mode_s("N12345")
print(result)
```

### Get API Online Status
```python
result = client.get_online_status()
print(result)
```

## License

This project is licensed under the MIT License.

