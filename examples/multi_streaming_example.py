from nyumaya_hotword_plugin.libnyumaya import FeatureExtractor
from nyumaya_hotword_plugin.record import ArecordStream
from nyumaya_hotword_plugin.multi_detector import MultiDetector


def light_on():
    print("Turning light on")


def light_off():
    print("Turning light off")


def stop():
    print("Stopping")


def label_stream(models, commands):
    extractor = FeatureExtractor()
    extractor_gain = 1.0

    detector = MultiDetector(timeout=20)

    for graph, labels, sensitivity in models:
        detector.add_detector(graph, labels, sensitivity)

    for command, callback in commands:
        detector.add_command(command, callback)

    bufsize = detector.get_input_data_size()

    audio_stream = ArecordStream()

    audio_stream.start()

    try:
        while True:
            frame = audio_stream.read(bufsize * 2, bufsize * 2)
            if not frame:
                continue
            features = extractor.signal_to_mel(frame, extractor_gain)
            detector.run_frame(features)
    except KeyboardInterrupt:
        print("Terminating")
        audio_stream.stop()


if __name__ == '__main__':
    from os.path import dirname, join

    models_folder = join(dirname(dirname(__file__)), "nyumaya_hotword_plugin",
                         "models")
    hotword_graph = join(models_folder, "hotwords", "marvin_small_0.3.tflite")
    hotword_labels = join(models_folder, "hotwords", "marvin_labels.txt")
    hotword_sensitivity = 0.5

    action_graph = join(models_folder, "commands", "subset_big_0.3.tflite")
    action_labels = join(models_folder, "commands", "subset_labels.txt")
    action_sensitivity = 0.9

    models = [
        (hotword_graph, hotword_labels, hotword_sensitivity),
        (action_graph, action_labels, action_sensitivity)
    ]

    # NOTE low accuracy, on/off are hard to trigger!
    commands = [
        ("marvin,on", light_on),
        ("marvin,off", light_off),
        ("stop", stop)
    ]

    label_stream(models, commands)
