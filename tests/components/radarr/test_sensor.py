"""The tests for Radarr sensor platform."""
from datetime import timedelta

from homeassistant.components.radarr.sensor import SENSOR_TYPES
from homeassistant.const import ATTR_UNIT_OF_MEASUREMENT
from homeassistant.core import HomeAssistant
import homeassistant.util.dt as dt_util

from . import setup_integration

from tests.common import async_fire_time_changed
from tests.test_util.aiohttp import AiohttpClientMocker


async def test_sensors(hass: HomeAssistant, aioclient_mock: AiohttpClientMocker):
    """Test for successfully setting up the Radarr platform."""
    for description in SENSOR_TYPES.values():
        description.entity_registry_enabled_default = True
    await setup_integration(hass, aioclient_mock)

    next_update = dt_util.utcnow() + timedelta(seconds=30)
    async_fire_time_changed(hass, next_update)
    await hass.async_block_till_done()

    state = hass.states.get("sensor.radarr_disk_space_downloads")
    assert state.state == "263.10"
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == "GB"
    state = hass.states.get("sensor.radarr_movies")
    assert state.state == "1"
    assert state.attributes.get(ATTR_UNIT_OF_MEASUREMENT) == "Movies"


async def test_windows(hass: HomeAssistant, aioclient_mock: AiohttpClientMocker):
    """Test for successfully setting up the Radarr platform on Windows."""
    await setup_integration(hass, aioclient_mock, windows=True)

    state = hass.states.get("sensor.radarr_disk_space_tv")
    assert state.state == "263.10"
