from nyumaya_hotword_plugin.libnyumaya import NyumayaDetector


class MultiDetector:

    def __init__(self, timeout=40):
        self.current_index = 0
        self.number_detectors = 0
        self.countdown = 0
        self.timeout = timeout
        self.detectors = []
        self.commands = []
        self.history = []
        self.last_frames = []
        self.max_last_frames = 5
        self.detected_callback = None
        self.history_callback = None
        self.possible_words = []
        self.current_detectors = []

    @staticmethod
    def _get_index(cmd, history):
        index = 0
        while index < len(history) and index < len(cmd):
            if history[index] != cmd[index]:
                return -1
            index += 1
        return index

    def get_possible_words(self, history):
        words = []
        for cmd in self.commands:
            index = self._get_index(cmd['command'], history)

            if index >= len(cmd['command']):
                print("Error index out of range:")
                print("Command: " + str(cmd))
                print("Index: " + str(index))
                print("History: " + str(history))
                return []

            if index >= 0:
                cmd = cmd['command'][index]
                if cmd not in words:
                    words.append(cmd)
        return words

    def get_detectors_for_words(self, words):
        detectors = []
        for detector in self.detectors:
            for word in words:
                if word in detector.labels_list and detector not in detectors:
                    detectors.append(detector)
        return detectors

    def update_last_frames(self, frame):
        self.last_frames.append(frame)
        if len(self.last_frames) > self.max_last_frames:
            self.last_frames.pop(0)

    def add_command(self, command, callback_function):
        if len(command.split(",")) == 0:
            print("No valid command")
            return

        self.commands.append(
            {'command': command.split(","), 'function': callback_function})
        self.update_word_and_detector()

    def add_detector(self, graph, labels, sensitivity):
        detector = NyumayaDetector(graph, labels)
        detector.set_sensitivity(sensitivity)
        self.detectors.append(detector)

    def add_reset_history_callback(self, callback_function):
        self.history_callback = callback_function

    def add_detected_callback(self, callback_function):
        self.detected_callback = callback_function

    def get_input_data_size(self):
        return self.detectors[0].get_input_data_size()

    def _maybe_execute(self):
        executed_cmd = False
        for cmd in self.commands:
            if cmd['command'] == self.history:
                cmd['function']()
                self.history = []
                self.countdown = 0
                self.last_frames = []
                executed_cmd = True

        return executed_cmd

    def check_timeout(self):

        if self.countdown > 0:
            self.countdown -= 1
            if self.countdown == 0:
                self.history = []
                self.update_word_and_detector()
                if self.history_callback:
                    self.history_callback()

    def update_word_and_detector(self):
        self.possible_words = self.get_possible_words(self.history)
        self.current_detectors = self.get_detectors_for_words(
            self.possible_words)

    def run_frame(self, frame, update_frames=True):

        if update_frames:
            self.update_last_frames(frame)

        self.check_timeout()

        for detector in self.current_detectors:
            prediction = detector.run_detection(frame)
            if prediction:
                label = detector.get_prediction_label(prediction)
                print("Got prediction: " + label)
                if label in self.possible_words:

                    self.countdown = self.timeout
                    self.history.append(label)
                    result = self._maybe_execute()
                    self.update_word_and_detector()

                    if self.detected_callback:
                        self.detected_callback()

                    if not result:
                        self.run_last_frames()

    def run_last_frames(self):
        for frame in self.last_frames:
            self.run_frame(frame, update_frames=False)

    def print_commands(self):
        for cmd in self.commands:
            print(cmd)
