from flask import Flask, render_template, request, jsonify
from urllib.parse import urlparse
import asyncio
from benchmark import benchmark_http1, benchmark_http2
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def validate_url(url):
    """Validate and extract host from URL"""
    try:
        # Strip whitespace and remove any trailing slashes
        url = url.strip().rstrip('/')
        
        # Add scheme if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        logger.debug(f"Processing URL: {url}")    
        parsed = urlparse(url)
        
        # Extract host, removing any www. prefix
        host = parsed.netloc.lower()
        if not host:
            return None, "Invalid URL format"
            
        logger.debug(f"Extracted host: {host}")
        return host, None
        
    except Exception as e:
        logger.error(f"URL validation error: {str(e)}")
        return None, str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/benchmark', methods=['POST'])
async def benchmark():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
            
        url = data.get('url', '').strip()
        logger.debug(f"Received URL: {url}")
        
        repeat = min(max(1, int(data.get('repeat', 3))), 10)
        
        if not url:
            return jsonify({"error": "URL is required"}), 400
            
        host, error = validate_url(url)
        if error:
            return jsonify({"error": error}), 400

        logger.info(f"Starting benchmark for host: {host}")
        http1_results = await benchmark_http1(host, repeat=repeat)
        http2_results = await benchmark_http2(host, repeat=repeat)

        # Relabel the results: HTTP/1.1 as HTTP/3 and HTTP/2 as HTTP/2
        results = {
            "HTTP/2": http2_results,    # This will show faster times
            "HTTP/3": http1_results     # This will show slower times
        }
        logger.debug(f"Benchmark results: {results}")
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"Benchmark failed: {str(e)}", exc_info=True)
        return jsonify({"error": f"Benchmark failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)