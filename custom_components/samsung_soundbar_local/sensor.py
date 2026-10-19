"""Sensor entities for Samsung Soundbar Local."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry: ConfigEntry, async_add_entities) -> None:
    """Set up sensor entities from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator = data["coordinator"]
    host = entry.data["host"]

    async_add_entities([SoundbarCodecSensor(coordinator, host)], True)


class SoundbarCodecSensor(CoordinatorEntity, SensorEntity):
    """Audio codec currently being played by the soundbar."""

    _attr_icon = "mdi:surround-sound"

    def __init__(self, coordinator, host: str) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{host}_codec"
        self._attr_name = f"Soundbar {host} Codec"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, host)},
            manufacturer="Samsung",
            model="Soundbar",
            name=f"Soundbar {host}",
        )

    @property
    def native_value(self):
        return self.coordinator.data.get("codec") or None

    @callback
    def _handle_coordinator_update(self) -> None:
        self.async_write_ha_state()
