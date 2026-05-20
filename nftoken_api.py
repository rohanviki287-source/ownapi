from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

API_URL = "https://ios.prod.ftl.netflix.com/iosui/user/15.48"

QUERY_PARAMS = { ... }   # (same as before - I kept it short here for space)
# Paste the full QUERY_PARAMS and BASE_HEADERS from your original script here
# (I can send the full version if you want, but for now use the one you already have)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        raw_cookie = str(data.get('cookie', '')).strip()

        match = re.search(r"NetflixId=([^;]+)", raw_cookie)
        if not match:
            return jsonify({"success": False, "error": "NetflixId not found"}), 400

        netflix_id = match.group(1)

        headers = { ... }   # Use your original BASE_HEADERS here

        response = requests.get(API_URL, params=QUERY_PARAMS, headers=headers, timeout=30, verify=False)

        if response.status_code != 200:
            return jsonify({"success": False, "error": "Request failed"}), 400

        json_data = response.json()
        token = (((json_data.get("value") or {}).get("account") or {}).get("token") or {}).get("default", {}).get("token")

        if not token:
            return jsonify({"success": False, "error": "Failed to generate token"}), 400

        base = "https://www.netflix.com"
        return jsonify({
            "success": True,
            "nftoken": token,
            "links": {
                "pc": f"{base}/account?nftoken={token}",
                "phone": f"{base}/unsupported?nftoken={token}",
                "tv": f"{base}/tv9?nftoken={token}"
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)