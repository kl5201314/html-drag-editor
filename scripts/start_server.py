#!/usr/bin/env python3
"""Start a local HTTP server for the HTML Drag Editor with a save API.

Usage:
    python start_server.py --html /path/to/target.html --port 8765
    python start_server.py --html /path/to/target.html --port 8765 --no-open
"""

import argparse
import http.server
import json
import os
import shutil
import socketserver
import sys
import webbrowser


def create_handler(original_path, exposed_name):
    """Factory that returns a Handler class closing over the save-target info."""

    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_OPTIONS(self):
            self.send_response(204)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.end_headers()

        def do_POST(self):
            if self.path != "/api/save":
                self._json(404, {"ok": False, "error": "not found"})
                return

            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)

            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                self._json(400, {"ok": False, "error": "invalid json"})
                return

            filename = data.get("filename", "")
            # Security: only allow saving to the exact file this server was
            # launched for.  Any other filename is rejected.
            if filename != exposed_name:
                self._json(403, {"ok": False, "error": "forbidden"})
                return

            content = data.get("content", "")
            if not isinstance(content, str) or not content.strip():
                self._json(400, {"ok": False, "error": "empty content"})
                return

            try:
                with open(original_path, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"  [save] Wrote {len(content)} bytes to {original_path}")
                self._json(200, {"ok": True})
            except Exception as e:
                self._json(500, {"ok": False, "error": str(e)})

        # -- helpers -------------------------------------------------------

        def _json(self, code, data):
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

        def end_headers(self):
            self.send_header("Cache-Control", "no-store")
            self.send_header("Access-Control-Allow-Origin", "*")
            super().end_headers()

        def log_message(self, format, *args):
            pass

    return Handler


def main():
    parser = argparse.ArgumentParser(
        description="Start the HTML Drag Editor local server."
    )
    parser.add_argument(
        "--html",
        required=True,
        help="Absolute path to the HTML file to edit.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8765,
        help="Port for the local server (default: 8765).",
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="Do not open the browser automatically.",
    )
    args = parser.parse_args()

    html_path = os.path.abspath(args.html)
    if not os.path.isfile(html_path):
        print(f"Error: file not found: {html_path}", file=sys.stderr)
        return 1

    target_dir = os.path.dirname(html_path)
    target_name = os.path.basename(html_path)

    # Avoid collision with editor.html by renaming the target if necessary.
    exposed_name = target_name
    if target_name.lower() == "editor.html":
        exposed_name = "_target.html"
        shutil.copy2(html_path, os.path.join(target_dir, exposed_name))
        print(f"Target renamed to avoid collision: {exposed_name}")

    # Copy the editor asset next to the target file.
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    editor_src = os.path.join(script_dir, "assets", "editor.html")
    if not os.path.isfile(editor_src):
        print(f"Error: editor asset not found at {editor_src}", file=sys.stderr)
        return 1

    editor_dst = os.path.join(target_dir, "editor.html")
    shutil.copy2(editor_src, editor_dst)
    print(f"Editor deployed to {editor_dst}")

    os.chdir(target_dir)

    Handler = create_handler(html_path, exposed_name)
    url = f"http://localhost:{args.port}/editor.html?file={exposed_name}"

    print(f"\n  Server:  {url}")
    print(f"  File:    {html_path}")
    print(f"  Save to: POST /api/save  (filename={exposed_name})")
    print(f"  Quit:    Ctrl+C\n")

    if not args.no_open:
        webbrowser.open(url)

    try:
        with socketserver.TCPServer(("127.0.0.1", args.port), Handler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except OSError as e:
        print(f"\nError: could not start server on port {args.port}.", file=sys.stderr)
        print(f"  {e}", file=sys.stderr)
        print(f"  Try --port <number>.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
