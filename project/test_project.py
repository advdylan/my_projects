import pytest
from project import get_cords, link_generator, format_date, print_weather_data
from unittest.mock import patch, MagicMock

def test_get_cords():
    with patch('geopy.geocoders.Nominatim.geocode') as mock_geocode:
        mock_location = MagicMock()
        mock_location.latitude = 51.5074
        mock_location.longitude = 0.1278
        mock_geocode.return_value = mock_location

        latitude, longitude = get_cords("London")
        assert latitude == 51.51
        assert longitude == 0.13

def test_link_generator():
    link = link_generator(51.51, 0.13, 3)
    assert link == 'https://api.open-meteo.com/v1/forecast?latitude=51.51&longitude=0.13&hourly=temperature_2m,rain&timezone=auto&forecast_days=3'

def test_format_date():
    time = ["2023-09-25T00:00", "2023-09-26T00:00", "2023-09-27T00:00"]
    formatted_time = format_date(time)
    assert formatted_time == ["2023-09-25: 00:00", "2023-09-26: 00:00", "2023-09-27: 00:00"]

@patch('builtins.print')
def test_print_weather_data(mock_print):
    weather_data = {
        'hourly': {
            'time': ["2023-09-25T00:00", "2023-09-26T00:00", "2023-09-27T00:00"],
            'temperature_2m': [15, 16, 17],
            'rain': [0, 0, 1]
        }
    }
    print_weather_data(weather_data)
    mock_print.assert_called_once()