## Description
Mycroft wake word plugin for [Nyumaya](https://github.com/nyumaya)

![](./model_accuracy/cpu_usage.png)

The "plugins" are pip install-able modules that provide new engines for mycroft

more info in the [docs](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mycroft-core/plugins)

## Install

`mycroft-pip install jarbas-wake-word-plugin-nyumaya`

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


# Training your own wake word

I could not find instructions to train your own wake-word, I opened an issue [here](https://github.com/nyumaya/nyumaya_audio_recognition/issues/25) requesting instructions