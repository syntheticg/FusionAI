import os
import importlib
from flask import Flask, request, jsonify
import base64
from io import BytesIO
from PIL import Image
from g4f.cookies import set_cookies_dir
import g4f.debug

app = Flask(__name__)

# aktifkan debug log g4f
g4f.debug.logging = True

# atur dan baca cookies dari folder har_and_cookies
cookies_dir = os.path.join(os.path.dirname(__file__), "har_and_cookies")

# buat folder jika belum ada
if not os.path.exists(cookies_dir):
    os.makedirs(cookies_dir)

# atur direktori cookies
set_cookies_dir(cookies_dir)
print(f"Cookies directory set to: {cookies_dir}")

# fungsi untuk memuat model dari folder models atau models/visionmodels
def load_model(model_name, is_vision=False):
    try:
        module_path = f"models.visionmodels.{model_name}" if is_vision else f"models.{model_name}"
        return importlib.import_module(module_path)
    except ModuleNotFoundError:
        return None

# konversi base64 image menjadi objek PIL image
def image_base64_to_pil(image_base64):
    try:
        if image_base64.startswith('data:image/jpeg;base64,'):
            image_base64 = image_base64.replace('data:image/jpeg;base64,', '')
        elif image_base64.startswith('data:image/png;base64,'):
            image_base64 = image_base64.replace('data:image/png;base64,', '')
        
        image_data = base64.b64decode(image_base64)
        return Image.open(BytesIO(image_data))
    except Exception:
        return None

# endpoint untuk model teks
@app.route('/models/<model_name>', methods=['GET'])
def text_model_endpoint(model_name):
    model_module = load_model(model_name)
    
    if model_module is None:
        return jsonify({"error": "model not found"}), 404

    prompt = request.args.get('prompt', '')

    # cek apakah model menggunakan g4f
    if hasattr(model_module, "generate_response"):
        response = model_module.generate_response(prompt)
    else:
        response = {"error": "invalid model implementation"}

    return jsonify(response)

# endpoint untuk model vision
@app.route('/models/visionmodels/<model_name>', methods=['POST'])
def vision_model_endpoint(model_name):
    prompt = request.json.get('prompt', '')
    image_base64 = request.json.get('image_base64', '')

    model_module = load_model(model_name, is_vision=True)
    
    if model_module is None:
        return jsonify({"error": "model not found"}), 404

    if image_base64:
        image = image_base64_to_pil(image_base64)
        if not image:
            return jsonify({"error": "invalid image data"}), 400
    else:
        image = None

    # cek apakah model mendukung `generate_response`
    if hasattr(model_module, "generate_response"):
        response = model_module.generate_response(prompt, image_base64)
    else:
        response = {"error": "invalid model implementation"}

    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))  # gunakan port default railway
    app.run(host='0.0.0.0', port=port)
