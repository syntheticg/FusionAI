import os
import importlib
from flask import Flask, request, jsonify
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

# fungsi untuk memuat model dari folder models
def load_model(model_name):
    try:
        module_path = f"models.{model_name}"
        return importlib.import_module(module_path)
    except ModuleNotFoundError:
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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))  # gunakan port default railway
    app.run(host='0.0.0.0', port=port)
