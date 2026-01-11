# Daikin Humidifier Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub Release](https://img.shields.io/github/release/longlife1st/ha_daikin_humidifier_integration.svg)](https://github.com/longlife1st/ha_daikin_humidifier_integration/releases)

Custom Home Assistant integration for Daikin air purifier/humidifier devices with local HTTP API support.

## Features

- 🌡️ **Humidifier Platform** - Control power, humidity levels, and operating modes
- 🌀 **Fan Control** - Adjust fan speed (Silent, Low, Normal, Turbo, Auto)
- 📊 **Air Quality Sensors** - PM2.5, temperature, and humidity monitoring
- ⚠️ **Filter Status** - Filter replacement warnings
- 🏠 **Local Control** - No cloud dependency,  direct local HTTP API communication
- ⚡ **Real-time Updates** - 60-second polling interval

## Supported Devices

This integration works with Daikin air purifier/humidifier models that support the local HTTP API, including:
- MCK55W series
- MCK70W series
- Other models with compatible local API

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add `https://github.com/longlife1st/ha_daikin_humidifier_integration` as an Integration
6. Click "Install"
7. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/daikin_humidifier` folder to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "Daikin Humidifier"
4. Enter your device's IP address (e.g., `192.168.1.100`)
5. Click **Submit**

### Finding Your Device IP Address

Check your router's DHCP client list or use a network scanner to find your Daikin device's IP address. It's recommended to set a static IP or DHCP reservation for your device.

## Entities

After setup, the following entities will be created:

| Entity | Description |
|--------|-------------|
| `humidifier.<device_name>` | Main humidifier control with modes |
| `fan.<device_name>_fan` | Fan speed control |
| `sensor.<device_name>_pm25` | PM2.5 air quality sensor |
| `sensor.<device_name>_humidity` | Current humidity sensor |
| `sensor.<device_name>_temperature` | Current temperature sensor |
| `binary_sensor.<device_name>_filter` | Filter replacement indicator |

## Operating Modes

- **Auto** (おまかせ) - Automatic operation
- **Eco** (節電) - Energy-saving mode
- **Pollen** (花粉) - Pollen mode
- **Moisturize** (のど・はだ) - Throat & skin mode
- **Circulator** (サーキュレーター) - Air circulation mode

## Troubleshooting

### Device Not Found
- Ensure your Daikin device is connected to the same network as Home Assistant
- Verify the IP address is correct
- Check that the device's local API is accessible (try accessing `http://<device_ip>/common/basic_info` in a browser)

### Entities Show "Unavailable"
- Check network connectivity between Home Assistant and the device
- Restart the integration from Settings → Devices & Services
- Verify the device is powered on

## Development

This integration is based on the [Daikin API documentation](https://github.com/nasshu2916/DAIKIN-API).

### Running Development Environment

```bash
./scripts/develop
```

### Linting

```bash
source .venv/bin/activate
ruff check custom_components/daikin_humidifier/
```

## Credits

- API documentation by [nasshu2916](https://github.com/nasshu2916/DAIKIN-API)
- Integration structure based on [integration_blueprint](https://github.com/ludeeus/integration_blueprint)

## License

MIT License - see [LICENSE](LICENSE) file for details

## Support

For issues and feature requests, please use the [GitHub issue tracker](https://github.com/longlife1st/ha_daikin_humidifier_integration/issues).
