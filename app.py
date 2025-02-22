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
    prompt = data.get("prompt", "")
    genre = data.get("genre", "")
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    # Combine prompt and genre for better context
    input_text = f"Write a {genre} story: {prompt}"
    story = generate_story(input_text)
    
    return jsonify({"story": story})

if __name__ == '__main__':
    app.run()

