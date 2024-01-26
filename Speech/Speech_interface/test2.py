import cv2
import time
import google.generativeai as genai
import pyttsx3
import logging as log

genai.configure(api_key="AIzaSyAtGqtsQ1zItev6Ur2NVMl0Jup8UN-_sTY")


class BlindAssistanceSystem:
    def __init__(self, model, prompt_interval=20):
        self.model = model
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

    blind_system = BlindAssistanceSystem(model)
    blind_system.capture_and_generate()
