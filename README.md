# Teletask Integration for Home Assistant

## Installation

You can only be logged into the ComNav/ZeroWire hub with the same user _once_; a subsequent login with the same user logs out the other. Since this tool/software actively polls and maintains a login session to your Hub, it can prevent you from being able to log into at the same time elsewhere (via it's website). **It is strongly recommended that you create a second user account on your Hub dedicated to just this service.**

### From HACS

1. Install HACS if you haven't already (see [installation guide](https://hacs.xyz/docs/setup/download)).
2. Find and install **Teletask** integration in HACS's "Integrations" tab.
3. Restart your Home Assistant.
4. Add "Teletask" integration in Home Assistant's config file 'configuration.yaml'

### Manual

1. Download and unzip the [repo archive](https://github.com/Tiemooowh/homeassistant-teletask/archive/refs/heads/main.zip). (You could also click "Download ZIP" after pressing the green button in the repo, alternatively, you could clone the repo from SSH add-on).
2. Copy contents of the archive/repo into your `/config` directory.
3. Restart your Home Assistant.
4. Add "Teletask" integration in Home Assistant's config file 'configuration.yaml'

## Configuration

Edit your HomeAssistant configuration.yaml File

**Note**: You can only be logged into one Teletask DoIP central connection unit.
**Note**: The functionality requires the Teletask "OPEN DOIP PROTOCOL" license to be activated in the Teletask Controller (SKU: TDS15132)

### Config

```yaml
teletask:
  host: 192.168.1.1
  port: 55957

  switch:
    - doip_component: relay
      address: "1"
      name: "Electrical Socket Carport"
      unique_id: { guid }

  light:
    - doip_component: relay
      address: "1"
      name: "Bulb Living Room"
      unique_id: { guid }

    - doip_component: relay
      address: "31"
      brightness_address: "1"
      name: "Led Strip Bedroom 1"
      unique_id: { guid }
```

### Global Attributes

| name | type    | mandatory field | description                                                                   |
| ---- | ------- | --------------- | ----------------------------------------------------------------------------- |
| host | String  | Yes             | The IP address or the Hostname where the Teletask DoIP API is running         |
| port | Integer | Yes             | The Porrt where the Teletask DoIP API is listening on (default is port 55957) |

### Light Attributes

| name               | type   | mandatory field | description                                                         |
| ------------------ | ------ | --------------- | ------------------------------------------------------------------- |
| doip_component     | String | Yes             | Possible Values: `relay`, `locmood`, `genmood` and `flag`           |
| address            | String | Yes             | The identifier on the Teletask DoIP Bus for the doip_component type |
| brightness_address | String | No              | The identifier on the Teletask DoIP Bus for the type 'dimmer'       |
| name               | String | Yes             | Friendly Name                                                       |
| unique_id          | String | No              | Unique Identifier for the entity (for example a guid).              |

### Switch Attributes

| name           | type   | mandatory field | description                                                         |
| -------------- | ------ | --------------- | ------------------------------------------------------------------- |
| doip_component | String | Yes             | Possible Values: `relay`, `locmood`, `genmood` and `flag`           |
| address        | String | Yes             | The identifier on the Teletask DoIP Bus for the doip_component type |
| name           | String | Yes             | Friendly Name                                                       |
| unique_id      | String | No              | Unique Identifier for the entity (for example a guid).              |
