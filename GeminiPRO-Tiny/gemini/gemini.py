import cv2
import time
import google.generativeai as genai
import pyttsx3
import logging as log

genai.configure(api_key='')

class TextToSpeechEngine:
    def __init__(self, rate):
        self.rate = rate
        self.engine = pyttsx3.init()

    def tts(self, text):
        self.engine.setProperty('rate', self.rate)
        log.info(text)
        log.info(self.engine.getProperty('rate'))
        self.engine.say(text)
        self.engine.runAndWait()

class BlindAssistanceSystem:
    def __init__(self, model, tts_engine, prompt_interval=20):
        self.model = model
        self.tts_engine = tts_engine
        self.prompt_interval = prompt_interval
        self.blind_assistance_prompt = (
            "you are a Navigation assistant for a visual impaired person. What is the optimal way forward the person should take to avoid collision, only state the object you see if it is in the way of the person."
        )

    def capture_and_generate(self):
        while True:
            frame = self.capture_frame()
            if frame is not None:
                response = self.model.generate_content(
                    contents=[self.blind_assistance_prompt, {'mime_type': 'image/jpeg', 'data': cv2.imencode('.jpg', frame)[1].tobytes()}]
                )

                generated_text = response.text
                print(response.prompt_feedback)
                print(f"Generated Text: {generated_text}")
                
                self.tts_engine.tts(generated_text)
                time.sleep(self.prompt_interval)

    def capture_frame(self):
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            log.error("Error: Unable to capture frame from the camera.")
        return frame

if __name__ == "__main__":
    model = genai.GenerativeModel('gemini-pro-vision')
    tts_engine = TextToSpeechEngine(rate=150)

    blind_system = BlindAssistanceSystem(model, tts_engine)
    blind_system.capture_and_generate()
