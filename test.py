from libnyumaya import AudioRecognition, FeatureExtractor
import time
from datetime import datetime
from record import AudiostreamSource


def label_stream(labels, graph, sensitivity):
    audio_stream = AudiostreamSource()

    extractor = FeatureExtractor()
    extactor_gain = 1.0

    detector = AudioRecognition(graph, labels)
    detector.SetSensitivity(sensitivity)

    bufsize = detector.GetInputDataSize()

    print("Audio Recognition Version: " + detector.GetVersionString())

    audio_stream.start()
    try:
        while True:
            frame = audio_stream.read(bufsize * 2, bufsize * 2)
            if not frame:
                time.sleep(0.01)
                continue

            features = extractor.signal_to_mel(frame, extactor_gain)

            prediction = detector.RunDetection(features)

            if prediction:
                now = datetime.now().strftime("%d.%b %Y %H:%M:%S")
                print(detector.GetPredictionLabel(prediction) + " " + now)

    except KeyboardInterrupt:
        print("Terminating")
        audio_stream.stop()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--graph', type=str,
        default='./models/Hotword/alexa_small_0.3.tflite',
        help='Model to use for identification.')

    parser.add_argument(
        '--labels', type=str,
        default='./models/Hotword/alexa_labels.txt',
        help='Path to file containing labels.')

    parser.add_argument(
        '--sens', type=float,
        default='0.5',
        help='Sensitivity for detection. A lower value means more sensitivity, for example,'
             '0.1 will lead to less false positives, but will also be harder to trigger.'
             '0.9 will make it easier to trigger, but lead to more false positives')

    FLAGS, unparsed = parser.parse_known_args()

    label_stream(FLAGS.labels, FLAGS.graph, FLAGS.sens)
