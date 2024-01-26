import gradio as gr
import google.generativeai as genai
import pyttsx3
import gradio as gr

# Used to securely store your API key
genai.configure(api_key='')

class TextToSpeechEngine:
    def __init__(self, rate):
        self.rate = rate
        self.engine = pyttsx3.init()

    def tts(self, text):
        self.engine.setProperty('rate', self.rate)
        self.engine.say(text)
        self.engine.runAndWait()

class BlindAssistanceSystem:
    def __init__(self, model, tts_engine, user_prompt):
        self.model = model
        self.user_prompt = user_prompt
        self.tts_engine = tts_engine
        self.blind_assistance_prompt = (
            "You are a navigation asistant. Describe the surroundings briefly and suggest the optimal way forward for a visually impaired person."
        )

        self.prompt = self.blind_assistance_prompt + self.user_prompt

    def generate_text_and_tts(self, image):
        frame = np.array(image)
        response = self.model.generate_content(
            contents=[self.prompt, {'mime_type': 'image/jpeg', 'data': cv2.imencode('.jpg', frame)[1].tobytes()}]
        )
        generated_text = response.text
        print(f"Generated Text: {generated_text}")

        # Text-to-Speech
        self.tts_engine.tts(generated_text)

    def send_message():
        pass
        # #Append a new prompt to the chat history.
        # response = chat.send_message("In one sentence, explain how a computer works to a young child.")
        # to_markdown(response.text)

def gr_interface(model, tts_engine, text_input):
    blind_system = BlindAssistanceSystem(model, tts_engine, text_input)
    pass


 

    # iface = gr.Interface(
    #     fn=blind_system.generate_text_and_tts,
    #     inputs="image",
    #     outputs=None,
    #     live=True,
    # )

    # iface.launch(share=True)

if __name__ == "__main__":
    model = genai.GenerativeModel('gemini-pro-vision')
    chat = model.start_chat(history=[])
    print(f"Chat is: {chat}")
    tts_engine = TextToSpeechEngine(rate=150)

    with gr.Blocks() as app:
        gr.Markdown("Gemini multimodal assistant \n")

        #Row for text input.
        with gr.Row():
            text_input = gr.TextArea(label = 'text input')
            image_input = gr.Image(label = "Drop image here")
        
        text_button = gr.Button("Submit")
        text_button.click() #Perform text input pipeline.

        with gr.Row("Model output"):
            text_input = gr.TextArea(label = "Model output")

    app.launch(share = False)


    # gr_interface(model, tts_engine)
