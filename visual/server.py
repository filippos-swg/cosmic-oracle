from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import os

PORT = 8000

if __name__ == "__main__":
    # Serve files from the visual/ folder
    os.chdir(os.path.dirname(__file__))

    print(f"Serving visual/ at: http://localhost:{PORT}/")
    print(f"Try JSON: http://localhost:{PORT}/oracle.json")
    ThreadingHTTPServer(("localhost", PORT), SimpleHTTPRequestHandler).serve_forever()