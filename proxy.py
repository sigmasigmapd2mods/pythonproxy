from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    target_url = f"https://{path}"  # Redirecting requests to HTTPS
    query_string = request.query_string.decode("utf-8")
    if query_string:
        target_url += f"?{query_string}"
    
    try:
        # Forward the request to the target URL
        resp = requests.get(target_url, headers=request.headers, stream=True)
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = {key: value for key, value in resp.headers.items() if key.lower() not in excluded_headers}
        
        return Response(resp.content, resp.status_code, headers)
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
