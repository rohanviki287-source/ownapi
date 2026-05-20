from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

API_URL = "https://ios.prod.ftl.netflix.com/iosui/user/15.48"

QUERY_PARAMS = { ... }   # keep your existing QUERY_PARAMS

BASE_HEADERS = { ... }   # keep your existing BASE_HEADERS

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        raw_cookie = str(data.get('cookie', '')).strip()

        match = re.search(r"NetflixId=([^;]+)", raw_cookie)
        if not match:
            return jsonify({"success": False, "error": "NetflixId not found"})

        netflix_id = match.group(1)

        headers = dict(BASE_HEADERS)
        headers["Cookie"] = f"NetflixId={netflix_id}"

        response = requests.get(API_URL, params=QUERY_PARAMS, headers=headers, timeout=30, verify=False)

        if response.status_code != 200:
            return jsonify({"success": False, "error": "Netflix error"})

        json_data = response.json()
        token = (((json_data.get("value") or {}).get("account") or {}).get("token") or {}).get("default", {}).get("token")

        if not token:
            return jsonify({"success": False, "error": "No token generated"})

        base = "https://www.netflix.com"

        return jsonify({
            "success": True,
            "token": token,
            "pc": f"{base}/account?nftoken={token}",
            "phone": f"{base}/unsupported?nftoken={token}",
            "tv": f"{base}/tv9?nftoken={token}"
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    print("NFT Token API Started")
    app.run(host="0.0.0.0", port=5000)
