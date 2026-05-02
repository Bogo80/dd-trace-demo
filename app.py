import os
from ddtrace import tracer, config, patch_all

# In Kubernetes, DD_AGENT_HOST is injected via downward API (status.hostIP)
dd_agent_host = os.environ.get("DD_AGENT_HOST", "datadog-agent")

tracer.configure(hostname=dd_agent_host)

config.service = "dd-demo"
config.env = "dev"
config.version = "1.0.0"

patch_all()

from flask import Flask, jsonify
import time
import random

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"message": "hello from traced app"})

@app.route("/process")
def process():
    with tracer.trace("process.work", service="dd-demo", resource="heavy-computation"):
        time.sleep(random.uniform(0.05, 0.2))
    return jsonify({"status": "done"})

@app.route("/error")
def error():
    raise ValueError("intentional error for tracing demo")

@app.errorhandler(Exception)
def handle_error(e):
    return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
