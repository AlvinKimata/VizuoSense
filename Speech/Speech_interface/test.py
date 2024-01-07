import pyaudio as pa
import json
from vosk import Model, KaldiRecognizer, SetLogLevel
import keyboard
import threading
from text_to_speech import speech_output as speech_output

class SpeechToTextEngine:
    def __init__(self, model_path, model_name, lang, save_textfile_dir):
        self.model_path = model_path
        self.model_name = model_name
        self.lang = lang
        self.save_textfile_dir = save_textfile_dir
        self.stop_flag = threading.Event()
        self.p = None
        self.listen_keyword_detected = threading.Event()

    def configure(self):
        model = Model(model_path=self.model_path, model_name=self.model_name, lang=self.lang)
        SetLogLevel(0)
        self.p = pa.PyAudio()
        mic_index = 3
        stream = self.p.open(format=pa.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4000,
                             input_device_index=mic_index)
        stream.start_stream()

        rec = KaldiRecognizer(model, 16000)
        rec.SetWords(True)
        rec.SetPartialWords(True)

        return stream, rec, self.p

    def listen_for_keywords(self):
        stream, rec, p = self.configure()
        keyword_detected = False

        while not self.stop_flag.is_set() and not keyword_detected:
            data = stream.read(4000, exception_on_overflow=False)
            rec.AcceptWaveform(data)
            partial_result = rec.PartialResult()
            if partial_result:
                partial_text = json.loads(partial_result).get("partial", "")
                print("Partial Result:", partial_text)

                if "listen" in partial_text.lower():
                    response = "Waking up! Listening for input..."
                    speech_output(response)
                    print("listen")
                    keyword_detected = True
                elif "stop" in partial_text.lower():
                    response = "Stop listening detected. Stopping..."
                    speech_output(response)
                    print("stop")
                    keyword_detected = True
                elif "write only mode" in partial_text.lower():
                    response = "Write only mode detected. Switching from speech to writing mode..."
                    speech_output(response)
                    print("write only mode")
                    keyword_detected = True
                elif keyboard.is_pressed('p'):
                    response = ''' KeyboardInterrupt: Stopping real-time listening
                        recognized text being: '''
                    speech_output(response)
                    self.stop_flag.set()


def main():
    model_path = "D:\\vizuosense_mine\\STT\\Resources\\vosk-model-small-en-us-0.15"
    model_name = "vosk-model-small-en-us-0.15"
    language = "small-en-us"
    save_textfile_dir = "D:\\vizuosense_mine\\STT\\Resources\\test.txt"
    stt_engine = SpeechToTextEngine(model_path, model_name, language, save_textfile_dir)
    while True:
        stt_engine.listen_for_keywords()

if __name__ == "__main__":
    main()
