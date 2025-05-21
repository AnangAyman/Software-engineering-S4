from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from models import db, User  # Import the database and User model
import random,json
from tertiary import get_initials, get_random_question

auth_bp = Blueprint('auth', __name__)  # Define the Blueprint

@auth_bp.route('/')
def home():
    return render_template('landingpage.html', user=session.get('user'))

# ----------------------------------- AUTHENTICATION ------------------------------------------------

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(request.form) #! For debugging delete later
        age = request.form.get('age')

        name = request.form.get('name')
        if name == "":
            name = "Anonymous Wanderer"

        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(email=email).first():
            error_message = "Email already exists."
            return render_template('SignUp.html', error=error_message)

        new_user = User(age=age, name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('SignUp.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form) #! Debugging delete later
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user'] = email
            session['user_id'] = user.id 
            return redirect(url_for('auth.dashboard'))
        else:
            error_message =  "Invalid credentials."
            return render_template('login.html', error=error_message)
    return render_template('login.html')

@auth_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    user_id = session.get('user_id')
    print(user_id)
    
    if not user_id:
        return redirect(url_for('auth.login'))

    user = User.query.get(user_id)
    full_name = user.name

    first_name,initials = get_initials(full_name)

    return render_template("Dashboard.html", 
                           full_name=full_name, 
                           first_name=first_name, 
                           initials=initials)

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.home'))

# ----------------------------------- GAME PAGE ------------------------------------------------

with open('questions.json') as f:
    questions = json.load(f)

with open('lessons.json') as f:
    lessons = json.load(f)

with open('ml_questions.json') as f:
    ml_questions = json.load(f)

@auth_bp.route('/ml_game', methods=['GET', 'POST'])
def ml_game():
    return render_template("ML_game.html", user=session.get('user'), lessons=lessons)

@auth_bp.route('/video_learning')
def video_learning():
    return render_template("videolearning.html", user=session.get('user'), lessons=lessons)

@auth_bp.route('/gamepage')
def gamepage():
    return render_template("gamepage.html", user=session.get('user'), lessons=lessons)


@auth_bp.route('/get-question')
def get_question():
    question = get_random_question(questions)

    # Randomize the choices
    choices = question['choices']
    random_choices = random.sample(choices, len(choices))  # Shuffle choices

    # Prepare the response
    response = {
        'question': question['question'],
        'choices': random_choices,
        'answer': question['answer'],  # Keep the correct answer
        'image': question['image']
    }

    return jsonify(response)

@auth_bp.route('/get-question-ml')
def get_question_ml():
    question = get_random_question(ml_questions)

    # Prepare the response
    response = {
        'question': question['question'],
        'answer': question['answer'],  # Keep the correct answer
    }

    return jsonify(response)

@auth_bp.route('/check-answer', methods=['POST'])
def check_answer():
    data = request.json
    selected = data.get('selected')
    correct = data.get('correct')
    return jsonify({"result": selected == correct})


# # ----------------------------------- CNN-LSTM MODEL ------------------------------------------------
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import io
import tensorflow as tf

# Load your CNN-LSTM model once at startup
model = load_model('models/Best Model.h5')

# Define your class labels in order
classes = [chr(i) for i in range(ord('A'), ord('Z') + 1)]


def preprocess_image(image: Image.Image, target_size=(224, 224)) -> np.ndarray:
    """
    Prepares an image for LSTM model prediction.
    Returns array shaped (1, 1, 224, 224, 3)
    """
    # 1. Resize and convert to array
    img = image.resize(target_size)
    arr = np.array(img)
    
    # 2. MobileNetV2 preprocessing (normalizes to [-1, 1])
    arr = tf.keras.applications.mobilenet_v2.preprocess_input(arr)
    
    # 3. Add dimensions:
    #    - First expand to (1, 224, 224, 3) for batch
    #    - Then expand to (1, 1, 224, 224, 3) for sequence
    arr = np.expand_dims(arr, axis=0)  # Batch dim
    arr = np.expand_dims(arr, axis=1)  # Sequence dim
    
    return arr

def decode_prediction(pred: np.ndarray) -> str:
    idx = np.argmax(pred, axis=1)[0]
    return classes[idx]

@auth_bp.route('/capture')
def capture_page():
    return render_template('pose_capture.html')

@auth_bp.route('/predict', methods=['POST'])
def predict():
    # Receive image blob
    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No image provided'}), 400

    # Load into PIL
    image = Image.open(io.BytesIO(file.read())).convert('RGB')

    # Preprocess for model
    input_tensor = preprocess_image(image)

    # Run model inference
    pred = model.predict(input_tensor)
    print(pred)
    result = decode_prediction(pred)

    return jsonify({'result': result})
