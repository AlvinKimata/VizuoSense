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
        self.listening_timeout_threshold = 5

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

    def listen_for_keywords(self, stream, rec,p):
        keyword_detected = False
        partial_text1 = ""
        # response = f'''Welcome to the voice commands enabled input.
        # Available commands are:'''
        # for key, value in self.keywords.items():
        #     response += f'\n{key}: {value}'
        # speech_output(response)
#        while not self.stop_flag.is_set() and not keyword_detected:
        while not keyword_detected:
            actual_partial_text = ""
            list_time = 5 #This is the time for listening for keywords
            response = 'You can Speak to issue you voice command input.'
            speech_output(response)
            start_time = datetime.datetime.now()
            while True:
                data = stream.read(4000, exception_on_overflow=False)
                rec.AcceptWaveform(data)
                partial_result = rec.PartialResult()
                partial_text = json.loads(partial_result).get("partial", "")
                current_time = datetime.datetime.now()
                elapsed_time = current_time - start_time
                actual_partial_text =  partial_text.replace(partial_text1, "")
                if elapsed_time.seconds > list_time:
                        # response = "time out"
                        # speech_output(response)
                    break
                elif any(keyword in actual_partial_text.lower() for keyword in self.keywords.keys()):
                    break
            actual_partial_text =  partial_text.replace(partial_text1, "")
            if "listen" in actual_partial_text.lower():
                response = "Waking up! Listening for input..."
                speech_output(response)
                self.listen_keyword_detected.set()
                keyword_detected = True
                return "listen"
            elif "stop" in actual_partial_text.lower():
                response = "Stop listening detected. Stopping..."
                speech_output(response)
                keyword_detected = True
                self.stop_flag.set()
                return "stop"
            elif "write only mode" in actual_partial_text.lower():
                response = "Write only mode detected. Switching from speech to writing mode..."
                speech_output(response)
                keyword_detected = True
                return "write only mode"
            elif "time" in actual_partial_text.lower():
                current_datetime = datetime.datetime.now()
                formatted_date = current_datetime.strftime("%Y-%m-%d")
                formatted_time = current_datetime.strftime("%I:%M %p")
                response = f"The current date is {formatted_date} and the time is {formatted_time}"
                speech_output(response)
                keyword_detected = False
            else:
                response = "No keyword was detected."
                speech_output(response)
                keyword_detected = False
            partial_text1 = partial_text

    def listen_for_speech_prompt(self, stream, rec, p):
        partial_text1 = ""
        recognized_text = ""
        recognized_text1 = ""
        current_prompt = ""
        in_silence = False
        # Initialize timeout_start before the loop
        timeout_start = datetime.datetime.now()
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            rec.AcceptWaveform(data)
            partial_result = rec.PartialResult()
            # Prompt the user to talk
            clear_output(wait=True)
            if partial_result:
                #print("Start status of in silence:",in_silence)
                partial_text = json.loads(partial_result).get("partial", "")
                received_txt = partial_text.replace(partial_text1, "")
                #print(f"Start:{received_txt}:end")
                recognized_text += partial_text.replace(partial_text1, "")
                current_prompt = recognized_text.replace(recognized_text1,"")
                print("Partial Result:", recognized_text)
                #if "   " in current_prompt and not in_silence:
                #Determine when a speaker is done communicating
                if received_txt == "" and in_silence == False:
                    timeout_start = datetime.datetime.now()
#                    print("in silence set to true, datetime is:", timeout_start)
                    in_silence = True
                elif received_txt != "":
                    in_silence = False
                #print("After if statement for checking is text is empty. insilence status: ",in_silence)
                current_time = datetime.datetime.now()
                elapsed_time = current_time - timeout_start
                if elapsed_time.seconds > self.listening_timeout_threshold and in_silence == True:
                    print("YOU STOPPED TALKING, THE WHOLE RECOGNIZED TEXT: ", recognized_text)
                    print("YOU STOPPED TALKING, THE CURRENT PROMPT TEXT: ", current_prompt)
                    timeout_start = datetime.datetime.now()
                    current_prompt = ""
                    recognized_text1 = recognized_text
                    in_silence = False
                    
                    print("Listening for speech prompt now")
                if keyboard.is_pressed('p'):
                    response = f'KeyboardInterrupt: Stopping real-time listening\nRecognized text being: {recognized_text}'
                    clear_output(wait=True)
                    print(response)
                    self.stop_flag.set()
            partial_text1 = partial_text
            # Take recognized text to the preprocessor

            # Take sentence from the preprocessor to the Gemini pro tiny

            # Take output from Gemini to TTS

            # Prompt for more text input and continue in the loop

    def real_time_listen(self):
        stream, rec,p = self.configure()

        # Create threads for simultaneous tasks
        keyword_thread = threading.Thread(target=self.listen_for_keywords, args=(stream, rec,p))
        speech_prompt_thread = threading.Thread(target=self.listen_for_speech_prompt, args=(stream, rec,p))

        try:
            keyword_thread.start()
            speech_prompt_thread.start()

            keyword_thread.join()  # Wait for the keyword thread to finish
            speech_prompt_thread.join()  # Wait for the speech prompt thread to finish

        except KeyboardInterrupt:
            response = "KeyboardInterrupt: Stopping real-time listening"
            speech_output(response)

        finally:
            self.stop_flag.set()  # Set the stop flag to signal threads to stop
            keyword_thread.join()  # Wait for the keyword thread to finish
            speech_prompt_thread.join()  # Wait for the speech prompt thread to finish

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
