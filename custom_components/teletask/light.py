"""Support for Teletask/IP lights."""
import voluptuous as vol

from .const import (
    DOMAIN
)

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    SUPPORT_BRIGHTNESS,
    LightEntity,
)
#from homeassistant.components.teletask import DATA_TELETASK
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
import math

import homeassistant.helpers.config_validation as cv

async def async_setup_platform(hass, config, async_add_entities, discovery_info):
    import teletask

    """Set up lights for Teletask platform."""
    print(config)
    platform_config = discovery_info["platform_config"]
    for config in platform_config:
        light = teletask.devices.Light(
            teletask=hass.data[DOMAIN].teletask,
            name=config.get(CONF_NAME),
            group_address_switch=config.get("address"),
            group_address_brightness=config.get("brightness_address"),
            doip_component=config.get("doip_component"),
        )
        await light.current_state()
        hass.data[DOMAIN].teletask.devices.add(light)
        async_add_entities([TeletaskLight(light)])


# @callback
# async def async_add_entities_config(hass, config):
#     """Set up light for Teletask platform configured within platform."""
#     import teletask

#     light = teletask.devices.Light(
#         teletask=hass.data[DOMAIN].teletask,
#         name=config.get(CONF_NAME),
#         group_address_switch=config.get("address"),
#         group_address_brightness=config.get("brightness_address"),
#         doip_component=config.get("doip_component"),
#     )
#     await light.current_state()
#     hass.data[DOMAIN].teletask.devices.add(light)
#     async_add_entities([TeletaskLight(light)])


class TeletaskLight(LightEntity):
    """Representation of a Teletask light."""

    def __init__(self, device):
        """Initialize of Teletask light."""
        self.device = device
        self.teletask = device.teletask

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
        """Return the brightness of this light between 0..100."""
        return (
            int(self.device.current_brightness * 2.55) if self.device.supports_brightness else None
        )

    @property
    def is_on(self):
        """Return true if light is on."""
        return self.device.state

    @property
    def supported_features(self):
        """Flag supported features."""
        flags = 0
        if self.device.supports_brightness:
            flags |= SUPPORT_BRIGHTNESS
        return flags

    async def async_turn_on(self, **kwargs):
        """Turn the light on."""
        if ATTR_BRIGHTNESS in kwargs:
            if self.device.supports_brightness:
                converted_value = int(kwargs[ATTR_BRIGHTNESS] / 2.55)
                await self.device.set_brightness(converted_value)
        else:
            await self.device.set_on()

    async def async_turn_off(self, **kwargs):
        """Turn the light off."""
        await self.device.set_off()
