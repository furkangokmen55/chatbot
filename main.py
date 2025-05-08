from dotenv import load_dotenv
import gradio as gr
load_dotenv()

from graph.graph import app

#if __name__ == "__main__":
#    print(app.invoke(input={"question": "Merhaba."}))


if __name__ == "__main__":
    while True:
        user_input = input("> ")
        if user_input.lower() == "çıkış":
            print("Programdan çıkılıyor.")
            break
        
        response = app.invoke(input={"question": user_input})
        
        # Sadece 'generation' cevabını al
        generation_response = response.get("generation", "Cevap bulunamadı.")
        
        print(generation_response, end="|")
"""

# Gradio arayüzü için fonksiyon
def gradio_arayuz(user_input):
    if user_input.lower() == "çıkış":
        return "Programdan çıkılıyor."
    
    response = app.invoke(input={"question": user_input})
    
    # Sadece 'generation' cevabını al
    generation_response = response.get("generation", "Cevap bulunamadı.")
    
    return generation_response

# Gradio arayüzünü başlatma
iface = gr.Interface(
    fn=gradio_arayuz,
    inputs=gr.Textbox(label="Sorunuzu buraya yazın", placeholder="Sorunuz..."),
    outputs="text",
    title="AI Chatbot",
    description="Yapay zeka tabanlı bir sohbet asistanı. Sorularınızı buradan sorabilirsiniz."
)

# Gradio arayüzünü başlat
iface.launch()
"""