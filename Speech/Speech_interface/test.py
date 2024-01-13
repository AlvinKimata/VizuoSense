import pyaudio as pa
import keyboard
import json
import subprocess
import threading
import datetime
from vosk import Model, KaldiRecognizer, SetLogLevel
from text_to_speech import speech_output

class SpeechToTextEngine:
    def __init__(self, model_path, model_name, lang, save_textfile_dir):
        self.model_path = model_path
        self.model_name = model_name
        self.lang = lang
        self.save_textfile_dir = save_textfile_dir
        self.stop_flag = threading.Event()
        self.p = None
        self.listen_keyword_detected = threading.Event()
        self.keywords = {"listen": "to start listening for voice input", "stop":"to stop listening for voice input", "write only mode":"to switch from speech to writing mode","time":"to get the current time"}

    def configure(self):
        model = Model(model_path=self.model_path, model_name=self.model_name, lang=self.lang)
        SetLogLevel(0)
        self.p = pa.PyAudio()
        mic_index = 3
        stream = self.p.open(format=pa.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000,
                             input_device_index=mic_index)
        stream.start_stream()

        rec = KaldiRecognizer(model, 16000)
        rec.SetWords(True)
        rec.SetPartialWords(True)

        return stream, rec, self.p

    def listen_for_speech_prompt(self, stream, rec,p):
        recognized_text = ""
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            rec.AcceptWaveform(data)
            partial_result = rec.PartialResult()

            #Prompt the user to talk
            #Start the listening logic
            print("Listening for speech prompt now")
            if partial_result:
                partial_text = json.loads(partial_result).get("partial", "")
                recognized_text += partial_text
                print("Partial Result:", recognized_text)
                if keyboard.is_pressed('p'):
                    response = ''' KeyboardInterrupt: Stopping real-time listening
                        recognized text being: '''
                    speech_output(response)
                    self.stop_flag.set()
                    return recognized_text
            #define logic ya kuambia the recognizer that tumemaliza to speek

            #take recognized text to the preprocessor

            #Take sentence from the preprocesssor to the Gemini pro tiny

            #Take output from Gemini to TTS

            #Prompt for more text input and continue in the loop

    def real_time_listen(self):
        stream, rec,p = self.configure()

        try:
            self.listen_for_speech_prompt(stream, rec,p)
        except KeyboardInterrupt:
            response = "KeyboardInterrupt: Stopping real-time listening"
            speech_output(response)

        finally:
            stream.stop_stream()
            stream.close()
            self.p.terminate()

def main():
    model_path = "D:\\vizuosense_mine\\STT\\Resources\\vosk-model-small-en-us-0.15"
    model_name = "vosk-model-small-en-us-0.15"
    language = "small-en-us"
    save_textfile_dir = "D:\\vizuosense_mine\\STT\\Resources\\test.txt"
    stt_engine = SpeechToTextEngine(model_path, model_name, language, save_textfile_dir)
    stt_engine.real_time_listen()

if __name__ == "__main__":
    main()
