"""Support for Teletask/IP lights."""
import voluptuous as vol

from .const import (
    DOMAIN
)

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    COLOR_MODE_BRIGHTNESS,
    COLOR_MODE_ONOFF,
    LightEntity,
)
#from homeassistant.components.teletask import DATA_TELETASK
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
import math
import teletask

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
        if self.device.supports_brightness:
            try:
                return int(self.device.current_brightness * 2.55)
            except:
                return 0
        else:
            return 0

    @property
    def is_on(self):
        """Return true if light is on."""
        return self.device.state

    @property
    def color_mode(self):
        """Return the color mode of the light."""
        if self.device.supports_brightness:
            return COLOR_MODE_BRIGHTNESS
        return COLOR_MODE_ONOFF

    @property
    def supported_color_modes(self):
        """Flag supported color modes."""
        return {self.color_mode}

    async def async_turn_on(self, **kwargs):
        """Turn the light on."""
        if ATTR_BRIGHTNESS in kwargs:
            if self.device.supports_brightness:
                if(int(kwargs[ATTR_BRIGHTNESS]) <= 3):
                    converted_value = 0
                else:
                    converted_value = int(kwargs[ATTR_BRIGHTNESS] / 2.55)
                await self.device.set_brightness(converted_value)
        else:
            await self.device.set_on()

    async def async_turn_off(self, **kwargs):
        """Turn the light off."""
        await self.device.set_off()
