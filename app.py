from flask import Flask, request, send_file
import requests
import tempfile
import os

app = Flask(__name__)

@app.route("/download")
def download():
    url = request.args.get("url")
    if not url:
        return "Missing 'url' parameter", 400

    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()

        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            for chunk in response.iter_content(chunk_size=8192):
                tmp_file.write(chunk)
            tmp_path = tmp_file.name

        return send_file(tmp_path, as_attachment=True, download_name=os.path.basename(url))

    except requests.RequestException as e:
        return f"Failed to download: {e}", 500

    finally:
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.remove(tmp_path)

@app.route("/")
def home():
    return "Download server is up. Use /download?url=..."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
