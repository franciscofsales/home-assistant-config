# [![Build Status](https://travis-ci.org/aneisch/home-assistant-config.svg?branch=master)](https://travis-ci.org/aneisch/home-assistant-config) My Home Assistant Config

I do my best to keep Home Assistant on the latest release. I'm heavily utilizing [AppDaemon](http://appdaemon.readthedocs.io/en/latest/) for advanced/templated automations. See [Appdaemon config](https://github.com/aneisch/home-assistant-config/tree/master/extras/appdaemon) for details. Using [Home Assistant Companion](https://itunes.apple.com/us/app/home-assistant-companion/id1099568401?mt=8) for iOS, built-in browser shortcut in Android. Also using [Tasker Plugin](https://github.com/MarkAdamson/home-assistant-plugin-for-tasker) from [MarkAdamsom](https://github.com/MarkAdamson) to trigger some automations and scripts from the client-side. 

My Home Assistant installation contains many different components and runs on a Gen7 i3 NUC running Centos 7:

- Owntracks for iOS and Android
- [Sonoff Switches](https://www.itead.cc/sonoff-wifi-wireless-switch.html) running [ESPHome](https://esphome.io/index.html)
- Orvibo Switches
- Radio Thermostat CT-50 (monitoring done through bash script querying local API and publishing to MQTT)
- Raspberry Pi hosted USB Camera (M-JPEG streamer)
- ESP32 Cameras running ESPHome
- Milights with [Homebrew MiLight controller](http://blog.christophermullins.com/2017/02/11/milight-wifi-gateway-emulator-on-an-esp8266/) using D1 Mini and NRF24L01. 
- Wemo wall plugs
- Aeon Labs ZW090 Z Stick
- Aeon Labs DSA03202 v1 - z-wave Minimote
- GE Z-wave in-wall switch/fan controllers
- [Lustreon E27](https://www.banggood.com/LUSTREON-E27-Smart-WiFi-Bulb-Adapter-Socket-Lamp-Holder-Work-With-Alexa-Google-Home-IFTTT-AC85-265V-p-1285550.html) bulb holders for lamp control using ~~Tasmota/MQTT~~ ESPHome (1MB flash)
  - Check out [my blog post](http://blog.aneis.ch/2019/01/tuya-convert-for-lustreon.html) for alternative firmware flashing instructions
- Various z-wave sensors
- Various MQTT Sensors (eg: [moon status](https://github.com/aneisch/home-assistant-config/blob/master/extras/helper_scripts/moon_phase_mqtt), determined using bash and published to MQTT))
- Arlo Cameras (controlled through IFTTT)
- [AppDaemon](https://appdaemon.readthedocs.io/en/latest/) controlling a majority of automations. See [/extras/appdaemon](https://github.com/aneisch/home-assistant-config/tree/master/extras/appdaemon) for configs.
- Amazon Echo Dots
  - Home Assistant Emulated Hue (devices are explicitly exposed via customize.yaml)
  - Custom skills via Alexa API.
  - Custom routines configured in the Alexa App.
  - [Alexa Media Player Custom Component](https://github.com/keatontaylor/alexa_media_player)
- MQTT remote and local server (via Docker). Using remote with SSL for Owntracks (on a box through Digital Ocean with static public IP), and local MQTT to communicate with various sensors/switches around the house. The remote MQTT shares messages with the local via a MQTT bridge.
- Numerous Wemos D1 Mini sensors via [ESPHome API](https://esphome.io/components/api.html). See [/extras/esphome](https://github.com/aneisch/home-assistant-config/tree/master/extras/esphome) for configs. 

Also using Grafana/Influx for graphing, both running in Docker containers on my NUC. 
 
Thanks to Deviant Engineer for the [guides](https://deviant.engineer/2016/11/hass-centos7/) that helped me during installation!!


# Interface
![UI](images/screenshot1.png)  
![UI](images/screenshot2.png)  
![UI](images/screenshot3.png)
![UI](images/screenshot4.png)
![UI](images/grafana.png)
