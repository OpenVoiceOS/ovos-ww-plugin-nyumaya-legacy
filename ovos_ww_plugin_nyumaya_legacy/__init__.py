# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from os.path import dirname, join, exists
from ovos_plugin_manager.templates.hotwords import HotWordEngine
from ovos_ww_plugin_nyumaya_legacy.libnyumaya import NyumayaDetector, FeatureExtractor


class NyumayaWakeWordPlugin(HotWordEngine):
    """Nyumaya Wake Word"""

    def __init__(self, hotword="nyumaya", config=None, lang="en-us"):
        config = config or {}
        super(NyumayaWakeWordPlugin, self).__init__(hotword, config, lang)
        self.extractor = FeatureExtractor()
        self.extractor_gain = config.get("extractor_gain", 1.0)
        self.sensitivity = config.get("sensitivity", 0.5)
        self.labels = config.get("labels")

        model = config.get("model", "alexa")
        models_folder = join(dirname(__file__), "models", "hotwords")
        if model == "alexa_big":
            self.model = join(models_folder, model + "_0.3.tflite")
            self.labels = join(models_folder, "alexa_labels.txt")
        elif model == "alexa" or model == "alexa_small":
            self.model = join(models_folder, "alexa_small_0.3.tflite")
            self.labels = join(models_folder, "alexa_labels.txt")
        elif model == "marvin_big":
            self.model = join(models_folder, model + "_0.3.tflite")
            self.labels = join(models_folder, "marvin_labels.txt")
        elif model == "marvin" or model == "marvin_small":
            self.model = join(models_folder, "marvin_small_0.3.tflite")
            self.labels = join(models_folder, "marvin_labels.txt")
        elif model == "sheila_big":
            self.model = join(models_folder, model + "_0.3.tflite")
            self.labels = join(models_folder, "sheila_labels.txt")
        elif model == "sheila" or model == "sheila_small":
            self.model = join(models_folder, "sheila_small_0.3.tflite")
            self.labels = join(models_folder, "sheila_labels.txt")
        elif exists(model):
            self.model = model
        elif exists(join(models_folder, model)):
            self.model = join(models_folder, model)
            self.labels = join(models_folder,
                               model.split("_")[1] + "_labels.txt")
        else:
            raise ValueError("Model not found: " + str(model))

        if self.labels and not exists(self.labels):
            self.labels = None
        self.detector = NyumayaDetector(self.model, self.labels)
        self.detector.set_sensitivity(self.sensitivity)
        self.bufsize = self.detector.get_input_data_size()
        print("Nyumaya lib version: " + self.detector.version)

    def found_wake_word(self, frame_data):
        """ frame data contains audio data that needs to be checked for a wake
        word, you can process audio here or just return a result
        previously handled in update method """
        features = self.extractor.signal_to_mel(frame_data,
                                                self.extractor_gain)
        prediction = self.detector.run_detection(features)
        if prediction:
            if self.labels:
                label = self.detector.get_prediction_label(prediction)
                print("Detected", label)
            return True
        return False

    def update(self, chunk):
        """ In here you have access to live audio chunks, allows for
        streaming predictions, result still need to be returned in
        found_wake_word method """

    def stop(self):
        """ Perform any actions needed to shut down the hot word engine.

            This may include things such as unload loaded data or shutdown
            external processes.
        """
