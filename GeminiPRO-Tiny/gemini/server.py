import google.generativeai as genai
from PIL import Image
import io


genai.configure(api_key='AIzaSyC6NSrRHycXap4eOSS2exAAnYlYojh_Prg')

model = genai.GenerativeModel('gemini-pro-vision')

def answer_question(image, question):
    yield "Encoding image..."

    image_bytes = io.BytesIO()
    image.save(image_bytes, format='JPEG')
    image_bytes = image_bytes.getvalue()

    response = model.generate_content(contents=[question, {'mime_type': 'image/jpeg', 'data': image_bytes}])

    generated_text = response.text
    yield generated_text

gr.Interface(
    title="🕶️ VizuoSense",
    description="""
    This is a repository 
    for the Intelligent Camera for the visually impaired project preferably refer to as VizuoSense.©
    """,
    fn=answer_question,
    inputs=[gr.Image(type="pil"), gr.Textbox(lines=2, label="Question")],
    outputs=gr.TextArea(label="Answer"),
    allow_flagging="never",
    cache_examples=False,
).launch()