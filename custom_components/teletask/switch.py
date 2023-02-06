"""Support for Teletask/IP switchs."""
import voluptuous as vol

from .const import (
    DOMAIN
)

from homeassistant.components.switch import (
    SwitchEntity
)
#from homeassistant.components.teletask import DATA_TELETASK
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
import math

import homeassistant.helpers.config_validation as cv

async def async_setup_platform(hass, config, async_add_entities, discovery_info):
    import teletask

    """Set up switchs for Teletask platform."""
    print(config)
    platform_config = discovery_info["platform_config"]
    for config in platform_config:
        switch = teletask.devices.Light(
            teletask=hass.data[DOMAIN].teletask,
            name=config.get(CONF_NAME),
            group_address_switch=config.get("address"),
            doip_component=config.get("doip_component"),
        )
        await switch.current_state()
        hass.data[DOMAIN].teletask.devices.add(switch)
        async_add_entities([TeletaskSwitch(switch, config.get("unique_id"))])


class TeletaskSwitch(SwitchEntity):
    """Representation of a Teletask Switch."""

    def __init__(self, device, unique_id):
        """Initialize of Teletask Switch."""
        self.device = device
        self.teletask = device.teletask
        if unique_id is not None:
            self._attr_unique_id = unique_id

    @callback
    def async_register_callbacks(self):
        """Register callbacks to update hass after device was changed."""

        async def after_update_callback(device):
            """Call after device was updated."""
            await self.async_update_ha_state()

        self.device.register_device_updated_cb(after_update_callback)

    async def async_added_to_hass(self):
        """Store register state change callback."""
        self.async_register_callbacks()

    @property
    def name(self):
        """Return the name of the Teletask device."""
        return self.device.name

    @property
    def available(self):
        """Return True if entity is available."""
        return self.hass.data[DOMAIN].connected

    @property
    def brightness(self):
        """Return the brightness of this switch between 0..100."""
        return (
            int(self.device.current_brightness * 2.55) if self.device.supports_brightness else None
        )

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self.device.state

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        await self.device.set_on()

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        await self.device.set_off()
