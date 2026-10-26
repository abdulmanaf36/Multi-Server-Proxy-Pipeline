from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route("/project1", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
@app.route("/project1/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
def project1(path):
    return forward_request("http://127.0.0.1:8000/" + path)

@app.route("/project2", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
@app.route("/project2/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
def project2(path):
    return forward_request("http://127.0.0.1:8081/" + path)

def forward_request(url):
    try:
        response = requests.request(
            method=request.method,
            url=url,
            params=request.args,
            data=request.get_data(),
            headers={
                key: value
                for key, value in request.headers
                if key.lower() not in ("host", "content-length", "connection")
            },
            allow_redirects=False,
            timeout=30
        )

        excluded = {
            "content-encoding",
            "content-length",
            "transfer-encoding",
            "connection"
        }

        headers = [
            (key, value)
            for key, value in response.raw.headers.items()
            if key.lower() not in excluded
        ]

        return Response(
            response.content,
            status=response.status_code,
            headers=headers
        )

    except requests.RequestException as error:
        return {"error": str(error)}, 502

if __name__ == "__main__":
    app.run(port=5000, debug=False)
