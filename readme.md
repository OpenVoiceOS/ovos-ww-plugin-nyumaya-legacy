## Description
Mycroft wake word plugin for [Nyumaya](https://github.com/nyumaya)

![](./model_accuracy/cpu_usage.png)

The "plugins" are pip install-able modules presenting one or more entrypoints with a entrypoint group defined in setup.py

Wake-word group: "mycroft.plugin.wake_word"

more info in the [original PR](https://github.com/MycroftAI/mycroft-core/pull/2594)

## Install

`mycroft-pip install git+https://github.com/JarbasAl/numaya_hotword`

## Configuration

Add the following to your hotwords section in mycroft.conf 

```json
  "hotwords": {
    "alexa": {
        "module": "nyumaya_ww_plug",
        "model": "alexa",
        "sensitivity": 0.5,
        "extractor_gain": 1.0
    },
    "alexa_big": {
        "module": "nyumaya_ww_plug",
        "model": "alexa_big",
        "sensitivity": 0.5,
        "extractor_gain": 1.0
    },
    "marvin": {
        "module": "nyumaya_ww_plug",
        "model": "marvin",
        "sensitivity": 0.5,
        "extractor_gain": 1.0
    },
    "marvin_big": {
        "module": "nyumaya_ww_plug",
        "model": "marvin_big",
        "sensitivity": 0.5,
        "extractor_gain": 1.0
    },
    "sheila": {
        "module": "nyumaya_ww_plug",
        "model": "sheila",
        "sensitivity": 0.5,
        "extractor_gain": 1.0
    },
     "sheila_big": {
        "module": "nyumaya_ww_plug",
        "model": "sheila_big",
        "sensitivity": 0.5,
        "extractor_gain": 1.0
    }
  }
```

Then select what wakeword to use

```json
 "listener": {
      "wake_word": "alexa_big"
 }
 
```