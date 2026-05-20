from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        cookie = str(data.get('cookie', '')).strip()

        match = re.search(r"NetflixId=([^;]+)", cookie)
        if not match:
            return jsonify({"success": False, "error": "NetflixId not found"})

        # Your original working headers
        headers = {
            "User-Agent": "Argo/15.48.1 (iPhone; iOS 15.8.5; Scale/2.00)",
            "Cookie": f"NetflixId={match.group(1)}"
        }

        params = {
            "appVersion": "15.48.1",
            "device_type": "NFAPPL-02-",
            "esn": "NFAPPL-02-IPHONE8%3D1-PXA-02026U9VV5O8AUKEAEO8PUJETCGDD4PQRI9DEB3MDLEMD0EACM4CS78LMD334MN3MQ3NMJ8SU9O9MVGS6BJCURM1PH1MUTGDPF4S4200",
            "idiom": "phone",
            "iosVersion": "15.8.5",
            "isTablet": "false",
            "languages": "en-US",
            "locale": "en-US",
            "maxDeviceWidth": "375",
            "model": "saget",
            "modelType": "IPHONE8-1",
            "odpAware": "true",
            "path": '["account","token","default"]',
            "pathFormat": "graph",
            "pixelDensity": "2.0",
            "progressive": "false",
            "responseFormat": "json",
        }

        response = requests.get(
            "https://ios.prod.ftl.netflix.com/iosui/user/15.48",
            params=params,
            headers=headers,
            timeout=30,
            verify=False
        )

        if response.status_code != 200:
            return jsonify({"success": False, "error": "Netflix error"})

        json_data = response.json()
        token = (((json_data.get("value") or {}).get("account") or {}).get("token") or {}).get("default", {}).get("token")

        if not token:
            return jsonify({"success": False, "error": "No token"})

        return jsonify({"success": True, "token": token})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
