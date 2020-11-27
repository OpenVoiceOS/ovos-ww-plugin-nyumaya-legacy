from ctypes import *
from os.path import join, dirname
import platform
import sys


def _load_labels(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f]


def _get_lib():
    system = platform.system()
    if system == "Linux":
        machine = platform.machine()
        if machine == "x86_64":
            return join(dirname(__file__), "lib", "linux", "libnyumaya.so")
        elif machine == "armv6l":
            return join(dirname(__file__), "lib", "armv6l", "libnyumaya.so")
        elif machine == "armv7l":
            return join(dirname(__file__), "lib", "armv7l", "libnyumaya.so")
        else:
            raise RuntimeError("Machine not supported")
    elif system == "Windows":
        raise RuntimeError("Windows is currently not supported")

    else:
        raise RuntimeError("Your OS is currently not supported")


class AudioRecognition:
    def __init__(self, model, labels=None):

        self._lib = cdll.LoadLibrary(_get_lib())

        self._lib.create_audio_recognition.argtypes = [c_char_p]
        self._lib.create_audio_recognition.restype = c_void_p

        self._lib.GetVersionString.argtypes = [c_void_p]
        self._lib.GetVersionString.restype = c_char_p

        self._lib.GetInputDataSize.argtypes = [c_void_p]
        self._lib.GetInputDataSize.restype = c_size_t

        self._lib.SetSensitivity.argtypes = [c_void_p, c_float]
        self._lib.SetSensitivity.restype = None

        self._lib.RunDetection.argtypes = [c_void_p, POINTER(c_uint8), c_int]
        self._lib.RunDetection.restype = c_int

        self._lib.RunRawDetection.argtypes = [c_void_p, POINTER(c_uint8),
                                              c_int]
        self._lib.RunRawDetection.restype = POINTER(c_uint8)

        self.model = self._lib.create_audio_recognition(model.encode('ascii'))

        self.check_version()

        if labels:
            self.labels_list = _load_labels(labels)
        else:
            self.labels_list = None

    def check_version(self):
        if sys.version_info[0] < 3:
            major, minor, rev = self.version.split('.')
        else:
            version_string = self.version[2:]
            version_string = version_string[:-1]
            major, minor, rev = version_string.split('.')

        if major != "0" and minor != "3":
            print("Your library version is not compatible with this API")

    def run_detection(self, data):
        datalen = int(len(data))
        pcm = c_uint8 * datalen
        pcmdata = pcm.from_buffer_copy(data)
        prediction = self._lib.RunDetection(self.model, pcmdata, datalen)
        return prediction

    def run_raw_detection(self, data):
        datalen = int(len(data))
        pcm = c_uint8 * datalen
        pcmdata = pcm.from_buffer_copy(data)
        prediction = self._lib.RunRawDetection(self.model, pcmdata, datalen)
        re = [prediction[i] for i in range(2)]
        return re

    def get_prediction_label(self, index):
        if self.labels_list:
            return self.labels_list[index]
        raise ValueError("Labels not loaded")

    def set_sensitivity(self, sens):
        self._lib.SetSensitivity(self.model, sens)

    @property
    def version(self):
        return str(self._lib.GetVersionString(self.model))

    def get_input_data_size(self):
        return self._lib.GetInputDataSize(self.model)


class FeatureExtractor:

    def __init__(self, nfft=512, melcount=40, sample_rate=16000,
                 lowerf=20, upperf=8000, window_len=0.03, shift=0.01):
        self.melcount = melcount
        self.shift = sample_rate * shift
        self.gain = 1

        self._lib = cdll.LoadLibrary(_get_lib())

        self._lib.create_feature_extractor.argtypes = [
            c_int, c_int, c_int, c_int, c_int, c_float, c_float]
        self._lib.create_feature_extractor.restype = c_void_p

        self._lib.get_melcount.argtypes = [c_void_p]
        self._lib.get_melcount.restype = c_int

        self._lib.signal_to_mel.argtypes = [
            c_void_p, POINTER(c_int16), c_int, POINTER(c_uint8), c_float]
        self._lib.signal_to_mel.restype = c_int

        self.feature_extractor = self._lib.create_feature_extractor(
            nfft, melcount, sample_rate, lowerf, upperf, window_len, shift)

    # Takes audio data in the form of bytes which are converted to int16
    def signal_to_mel(self, data, gain=1):
        datalen = int(len(data) / 2)
        pcm = c_int16 * datalen
        pcmdata = pcm.from_buffer_copy(data)

        number_of_frames = int(datalen / self.shift)
        melsize = self.melcount * number_of_frames

        result = (c_uint8 * melsize)()

        reslen = self._lib.signal_to_mel(self.feature_extractor, pcmdata,
                                         datalen,
                                         result, gain)

        if reslen != melsize:
            print("Bad: melsize mismatch")
            print("Expected: " + str(melsize))
            print("Got: " + str(reslen))

        return bytearray(result)

    def set_gain(self, gain):
        self.gain = gain

    def get_melcount(self):
        return self._lib.get_melcount(self.feature_extractor)

    def remove_DC(self, val):
        self._lib.remove_DC(self.feature_extractor, val)
