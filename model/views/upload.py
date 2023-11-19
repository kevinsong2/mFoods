import torch
import torchvision.transforms as transforms
from PIL import Image
from io import BytesIO

from flask import Flask, request, jsonify
from model.train_model import build_model
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
# model = load_model('trained_model.pt', 3)  # Assuming load_model is defined
model = build_model(num_classes=3)
model.load_state_dict(torch.load("trained_model.pt"))

def transform_image(img_stream):
    my_transforms = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])

    # img_stream is a file-like object (BytesIO stream)
    image = Image.open(img_stream).convert('RGB')
    transformed_img = my_transforms(image)
    batch_tensor = transformed_img.unsqueeze(0)
    return batch_tensor
# def transform_image(img):
#     my_transforms = transforms.Compose([
#         transforms.Resize((256, 256)),
#         transforms.ToTensor(),
#         transforms.Normalize((0.5,), (0.5,))
#     ])

#     image = Image.open(img).convert('RGB')
#     transformed_img = my_transforms(image)
#     batch_tensor = transformed_img.unsqueeze(0)
#     return batch_tensor

@app.route('/model/views/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    recipe_ingredients = {
        "cake": ["Flour", "Sugar", "Eggs", "Butter"],
        "spaghetti": ["Pasta", "Tomato Sauce", "Parmesan Cheese", "Olive Oil"],
        "taco": ["Tortillas", "Beef", "Cheese", "Lettuce", "Tomato"]
    }
    print("image opened")
    img_stream = BytesIO(file.read())  # Create a BytesIO stream from the uploaded file
    transformed_image = transform_image(img_stream)
    # image = Image.open(BytesIO(file.read()))
    # transformed_image = transform_image(image)
    prediction = model(transformed_image)

    predicted_label_idx = torch.argmax(prediction, dim=1).item()
    food_mp = {0: "cake", 1: "spaghetti", 2: "taco"}
    output = food_mp[predicted_label_idx]
    ingredients = recipe_ingredients[output]

    return jsonify({'prediction': output, 'ingredients': ingredients})


if __name__ == '__main__':
    app.run(debug=True)
