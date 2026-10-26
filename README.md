# Flask Path Proxy

A lightweight reverse proxy written in Python/Flask that routes requests to multiple local services based on a URL path prefix — so several projects can share a single port.

```
http://localhost:5000/project1/...  ──►  http://127.0.0.1:8000/...
http://localhost:5000/project2/...  ──►  http://127.0.0.1:8081/...
```

## Features

- Path-prefix routing to multiple backend services
- Supports `GET`, `POST`, `PUT`, `DELETE`, `PATCH` and `OPTIONS`
- Forwards query strings, request bodies and headers
- Passes through status codes and response headers (redirects are not followed)
- Returns `502 Bad Gateway` with a JSON error if a backend is unreachable
- 30-second upstream timeout

## Requirements

- Python 3.8+

## Installation

```bash
git clone https://github.com/<your-username>/flask-path-proxy.git
cd flask-path-proxy

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

## Usage

1. Start your backend services (e.g. one on port `8000`, another on `8081`).
2. Run the proxy:

   ```bash
   python proxy.py
   ```

3. Send requests through the proxy:

   ```bash
   curl http://localhost:5000/project1/api/users
   # forwarded to http://127.0.0.1:8000/api/users

   curl -X POST http://localhost:5000/project2/login -d '{"user":"demo"}' -H "Content-Type: application/json"
   # forwarded to http://127.0.0.1:8081/login
   ```

## Configuration

Routes are defined in [`proxy.py`](proxy.py). To add another backend, copy one of the existing route blocks and change the prefix and target:

```python
@app.route("/project3", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
@app.route("/project3/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
def project3(path):
    return forward_request("http://127.0.0.1:9000/" + path)
```

The proxy listens on port `5000` by default; change it in the `app.run(...)` call at the bottom of the file.

## Limitations

- Uses Flask's built-in development server — for production, run it behind a WSGI server such as Gunicorn (`gunicorn -b 0.0.0.0:5000 proxy:app`).
- Responses are buffered in memory, so it is not suited to streaming or very large downloads.
- WebSockets are not supported.
- Backends that generate absolute links (e.g. `/static/app.js`) may need to be configured with the proxy prefix as their base path.

## License

[MIT](LICENSE)
