
from flask import Flask, redirect
import redis
import os

app = Flask(__name__)
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
redis_client = redis.from_url(redis_url)

# Dictionary to store local URLs (for testing)
local_urls = {}

@app.route('/<code>')
def redirect_url(code):
    try:
        original_url = redis_client.get(f"url:{code}")
        if original_url:
            # Increment access counter
            redis_client.incr(f"stats:{code}")
            # Increment score in sorted set
            redis_client.zincrby("popular_urls", 1, code)
            return redirect(original_url.decode())
    except redis.exceptions.ConnectionError:
        return "Erro de conexão com Redis", 500
    return "URL não encontrada ou expirada", 404

@app.route('/local/<code>')
def redirect_local_url(code):
    if code in local_urls:
        local_urls[code]['visits'] += 1
        return redirect(local_urls[code]['url'])
    return "URL local não encontrada", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
