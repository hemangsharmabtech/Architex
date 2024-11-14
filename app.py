from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from tensorflow.keras.models import load_model
import numpy as np
import base64
import csv
from io import BytesIO
from PIL import Image
import os

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Load the generator model
generator = load_model('models/generator_model.h5', compile=False)

# Path to the CSV file where user data is stored
csv_file = 'users.csv'

@app.route('/')
def index():
    return render_template('index.html')  # Changed to index.html

@app.route('/floor_plan')
def floor_plan():
    return render_template('floor_plan.html')

# Signup route to handle user registration
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Save the new user to CSV
        try:
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([name, email, password])
        except Exception as e:
            print(f"Error writing to CSV: {e}")

        # Redirect to the index page
        return redirect(url_for('floor_plan'))  # Corrected the URL for the index route
    
    return render_template('signup.html')  # Ensure this file is in the templates folder

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()  # Get the JSON data sent from fetch
        email = data.get('email')
        password = data.get('password')

        # Check if user exists in the CSV file
        with open(csv_file, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row if there is one
            for row in reader:
                if row[1] == email and row[2] == password:
                    # Credentials match, return success response
                    return jsonify({"message": "Login successful"}), 200

        # If no match is found, return error message
        return jsonify({"message": "Invalid credentials. Please try again or sign up first."}), 400

    return render_template('login.html')


@app.route("/generate-image", methods=["POST"])
def generate_image():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')

        # Generate the image as before
        input_shape = (868,)  # Adjust to match your model's expected input shape
        input_vector = np.random.rand(1, *input_shape)  # Generate random input

        generated_image_array = generator.predict(input_vector)[0]  # Generate the image

        # Scale the output image to the range [0, 255]
        generated_image_array = (generated_image_array * 255).astype(np.uint8)

        # Convert to a PIL image
        if generated_image_array.shape[-1] == 1:
            generated_image_array = np.squeeze(generated_image_array, axis=-1)  # Remove single channel
            image = Image.fromarray(generated_image_array, 'L')  # Grayscale mode
        else:
            image = Image.fromarray(generated_image_array, 'RGB')  # RGB mode for color images

        # Resize the image to a larger size (e.g., 512x512)
        target_size = (200, 200)  # Specify your desired image size
        image = image.resize(target_size, Image.Resampling.BICUBIC)  # Resize with BICUBIC filter

        # Convert the image to base64 for HTML display
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return jsonify({"image": img_str})

    except Exception as e:
        print("Error during image generation:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
