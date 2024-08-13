import requests
import io
from PIL import Image
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def run_model_and_download(prompt, output_quality, local_filename):
    """
    Run the model using the Hugging Face Inference API and save the output image locally.

    Args:
        prompt (str): The prompt to pass to the model.
        output_quality (float): Not used in this version, but kept for compatibility.
        local_filename (str): The local filename to save the generated image.
    """
    # Get the Hugging Face API token from environment variables
    api_token = os.getenv('HF_API_TOKEN')

    if not api_token:
        raise ValueError("HF_API_TOKEN not found in environment variables")

    # Define the API URL and headers
    API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
    headers = {"Authorization": f"Bearer {api_token}"}

    def query(payload):
        # Send the POST request to the Hugging Face API
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.content

    # Generate the image with the provided prompt
    image_bytes = query({
        "inputs": prompt,
    })

    # Open the image using PIL and save it locally
    image = Image.open(io.BytesIO(image_bytes))
    image.save(local_filename)
    print(f"Image saved as {local_filename}")
