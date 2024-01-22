import os
import gradio as gr
import cv2
import google.generativeai as genai


genai.configure(api_key='AIzaSyAtGqtsQ1zItev6Ur2NVMl0Jup8UN-_sTY')

# Initialize the Gemini Multimodal model
model = genai.GenerativeModel('gemini-pro-vision')

# Function to process image and prompt
def process_input(image, prompt, chatbot, txt):
    try:
        # Convert the image to bytes
        image_bytes = cv2.imencode('.jpg', image)[1].tobytes()

        # Make a direct call to the Gemini Multimodal model
        response = model.generate_content(contents=[prompt, {'mime_type': 'image/jpeg', 'data': image_bytes}])

        # Extract generated text if response is successful
        if response.success:
            generated_text = response.text
            print(f"Generated Text: {generated_text}")

            # Add the multimodal output to the chat
            history = chatbot.history + [(generated_text, None)]
            chatbot.history = history

            # Clear the text input
            txt.value = ""

        # Yield both chatbot.history and txt
        yield chatbot.history, txt

    except Exception as e:
        print(f"Error in process_input: {e}")

        # Yield only chatbot.history and an empty txt
        yield chatbot.history, gr.Textbox(value="", interactive=False)

# Function to handle text input
def add_text(history, text):
    history = history + [(text, None)]
    return history, gr.Textbox(value="", interactive=False)

# Function to handle file upload
def add_file(history, file):
    history = history + [((file.name,), None)]
    return history

# Create the Gradio interface
with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        [],
        elem_id="chatbot",
        bubble_full_width=False,
        avatar_images=(None, (os.path.join(os.path.dirname(__file__), "avatar.png"))),
    )

    with gr.Row():
        txt = gr.Textbox(
            scale=4,
            show_label=False,
            placeholder="Enter text and press enter, or upload an image",
            container=False,
        )
        btn = gr.UploadButton("📁", file_types=["image", "video", "audio"])

    # Handle text input and chat responses
    txt_msg = txt.submit(lambda x: add_text(x, chatbot, txt), [chatbot, txt], queue=False).then(
        lambda x: x, None, [chatbot, txt], queue=False
    )

# Handle file upload, make direct call to Gemini Multimodal, and update chat
    file_msg = btn.upload(lambda x: process_input(x, 'your_prompt', chatbot, txt), [chatbot, btn], [chatbot, txt], queue=False).then(
        lambda x: x, None, [chatbot, txt], queue=False
    )


demo.queue()

# Launch the Gradio interface
if __name__ == "__main__":
    demo.launch(share=True)