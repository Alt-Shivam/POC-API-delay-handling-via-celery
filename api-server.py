from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def delayed_response():
    time.sleep(10)
    return jsonify({"message": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)
