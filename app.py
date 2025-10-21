#!/usr/bin/env python3
"""
Launcher: starts a local HTTP server and opens the included HTML in the default browser.
Serves files from the same folder where the exe/script is run.
"""
import http.server
import socketserver
import webbrowser
import threading
import socket
import sys
import os
from contextlib import closing

HTML_FILE = "ULTIMATE_FARM_BP.html"

def find_free_port(host="127.0.0.1"):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind((host, 0))
        return s.getsockname()[1]

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return

def run_server(port, directory):
    os.chdir(directory)
    handler = QuietHandler
    with socketserver.TCPServer(("127.0.0.1", port), handler) as httpd:
        print(f"Serving {directory} at http://127.0.0.1:{port}/")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass

def main():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    html_path = os.path.join(base_dir, HTML_FILE)
    if not os.path.exists(html_path):
        print("Error: HTML file not found:", HTML_FILE)
        sys.exit(1)

    port = find_free_port()
    t = threading.Thread(target=run_server, args=(port, base_dir), daemon=True)
    t.start()

    url = f"http://127.0.0.1:{port}/{HTML_FILE}"
    try:
        webbrowser.open(url, new=1)
    except Exception:
        print("Open this URL manually:", url)

    try:
        print("Press Ctrl+C to stop.")
        while True:
            t.join(1)
    except KeyboardInterrupt:
        print("Shutting down...")

if __name__ == "__main__":
    main()
