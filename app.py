from flask import Flask, render_template, request, jsonify
import os
import warnings
import torch
from transformers import logging, AutoModelForCausalLM, AutoTokenizer, pipeline

app = Flask(__name__, static_folder="static", template_folder="templates")

# Suppress warnings and logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings("ignore")
logging.set_verbosity_error()

# Load the model and tokenizer
model_name = "TinyLlama/TinyLlama-1.1B-chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Check if GPU is available
device = 0 if torch.cuda.is_available() else -1  # 0 for GPU, -1 for CPU
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=device)

def generate_story(prompt, max_length=120, temperature=0.7):
    response = generator(
        prompt, 
        max_length=max_length, 
        temperature=temperature, 
        num_return_sequences=1,
        top_k=50,  # Faster sampling
        top_p=0.9  # Controlled randomness
    )
    return response[0]['generated_text']

@app.route('/')
def home():
    """Serve the HTML frontend."""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    """Generate AI story based on user input."""
    data = request.json
    prompt = data.get("prompt", "").strip()
    genre = data.get("genre", "").strip().lower()  # Normalize genre input

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # Custom instructions for each genre
    genre_templates = {
        "gangster": "Write a gritty and suspenseful gangster crime story with mob bosses and betrayals: ",
        "horror": "Write a spine-chilling horror story that builds tension and fear: ",
        "psychological-thriller": "Write a mind-twisting psychological thriller filled with unexpected twists: ",
        "thriller": "Write an action-packed thriller with high tension and suspense: ",
        "mystery": "Write a mysterious detective story full of secrets and surprises: ",
        "drama": "Write an emotional and character-driven drama story: ",
        "period action": "Write a historical action-adventure with epic battles and warriors: ",
        "comedy": "Write a funny and entertaining comedy story with witty humor: "
    }

    # Use the predefined template if available; otherwise, fall back to generic format
    input_text = genre_templates.get(genre, f"Write a {genre} story: ") + prompt

    story = generate_story(input_text)

    return jsonify({"story": story})

if __name__ == '__main__':
    app.run()
