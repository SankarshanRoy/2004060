from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Test servers URLs
TEST_SERVERS = [
    "http://20.244.56.144/numbers/primes",
    "http://20.244.56.144/numbers/fibo",
    "http://20.244.56.144/numbers/odd",
    "http://20.244.56.144/numbers/rand"
]

# Endpoint to retrieve numbers from given URLs
@app.route('/numbers', methods=['GET'])
def get_numbers():
    urls = request.args.getlist('url')

    if not urls:
        return jsonify(error='No URLs provided'), 400

    result = []

    for url in urls:
        if url in TEST_SERVERS:
            try:
                response = requests.get(url)
                response.raise_for_status()  
                response_data = response.json()
                result.extend(response_data['numbers'])
            except requests.exceptions.RequestException as e:
                return jsonify(error=f"Failed to fetch data from {url}: {e}"), 500
            except Exception as e:
                return jsonify(error=f"Invalid JSON response from {url}: {e}"), 500
        else:
            return jsonify(error=f"Invalid URL: {url}"), 400

    return jsonify(numbers=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
