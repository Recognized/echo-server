import os
import http.server
import socketserver

CRASH = os.environ.get("CRASH", "").strip().lower() == "true"
if CRASH:
    raise RuntimeError("CRASH=true — crashing immediately!")

PORT = 38917
_raw_error_code = os.environ.get("ERROR_CODE", "").strip()
ERROR_CODE = None
if _raw_error_code:
    try:
        ERROR_CODE = int(_raw_error_code)
    except ValueError:
        print(f"WARNING: ERROR_CODE='{_raw_error_code}' is not a valid integer, ignoring")


class ErrorHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if ERROR_CODE is not None:
            self.send_error(ERROR_CODE, f"Forced error {ERROR_CODE}")
        else:
            super().do_GET()

    def do_POST(self):
        if ERROR_CODE is not None:
            self.send_error(ERROR_CODE, f"Forced error {ERROR_CODE}")
        else:
            self.send_error(501, "Not Implemented")


socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("0.0.0.0", PORT), ErrorHandler) as httpd:
    print(f"Serving on port {PORT}")
    if ERROR_CODE:
        print(f"ERROR_CODE={ERROR_CODE} — all requests will return HTTP {ERROR_CODE}")
    httpd.serve_forever()
