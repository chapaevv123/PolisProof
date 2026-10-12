from __future__ import annotations

import argparse
import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from .pipeline import PolisProofPipeline


def make_handler(root: Path, mode: str):
    pipeline = PolisProofPipeline(root, mode=mode)
    web = root / "src" / "web"

    class Handler(BaseHTTPRequestHandler):
        def _json(self, value: object, status: int = 200) -> None:
            body = json.dumps(value, ensure_ascii=False, indent=2).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self) -> None:
            parsed = urlparse(self.path)
            if parsed.path != "/api/compile":
                self._json({"error": "not found"}, 404)
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length <= 0 or length > 1_000_000:
                    raise ValueError("packet must be between 1 byte and 1 MB")
                packet = json.loads(self.rfile.read(length).decode("utf-8"))
                if not isinstance(packet, dict) or not isinstance(packet.get("artifacts"), list) or not packet["artifacts"]:
                    raise ValueError("packet requires a non-empty artifacts array")
                packet.setdefault("packet_id", "uploaded-packet")
                for index, artifact in enumerate(packet["artifacts"]):
                    if not isinstance(artifact, dict) or not str(artifact.get("content", "")).strip():
                        raise ValueError(f"artifact {index} requires content")
                    artifact.setdefault("artifact_id", f"upload-{index+1}")
                    artifact.setdefault("language", "unknown")
                self._json(pipeline.compile(packet))
            except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                self._json({"error": str(exc), "execution_mode": "ERROR"}, 400)

        def do_GET(self) -> None:
            parsed = urlparse(self.path)
            if parsed.path == "/api/health":
                self._json({"status": "ok", "mode": mode.upper(), "live_configured": pipeline.provider.live_configured})
                return
            if parsed.path == "/api/fixtures":
                names = sorted(p.stem for p in (root / "fixtures" / "packets").glob("*.json"))
                self._json({"fixtures": names})
                return
            if parsed.path.startswith("/api/packet/"):
                fixture = parsed.path.rsplit("/", 1)[-1]
                if not fixture.replace("_", "").replace("-", "").isalnum():
                    self._json({"error": "invalid fixture name"}, 400)
                    return
                target = root / "fixtures" / "packets" / f"{fixture}.json"
                try:
                    self._json(json.loads(target.read_text(encoding="utf-8")))
                except (FileNotFoundError, json.JSONDecodeError) as exc:
                    self._json({"error": str(exc)}, 404)
                return
            if parsed.path.startswith("/api/compile/"):
                fixture = parsed.path.rsplit("/", 1)[-1]
                try:
                    self._json(pipeline.compile_fixture(fixture))
                except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
                    self._json({"error": str(exc)}, 404)
                return
            relative = "index.html" if parsed.path == "/" else parsed.path.lstrip("/")
            target = (web / relative).resolve()
            if web.resolve() not in target.parents and target != web.resolve():
                self.send_error(403)
                return
            if not target.is_file():
                self.send_error(404)
                return
            body = target.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", mimetypes.guess_type(target.name)[0] or "application/octet-stream")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args: object) -> None:
            print(f"polisproof {self.address_string()} {format % args}")

    return Handler


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default=os.getenv("HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8080")))
    parser.add_argument("--mode", choices=["replay", "live"], default=os.getenv("POLISPROOF_MODE", "replay"))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    server = ThreadingHTTPServer((args.host, args.port), make_handler(root, args.mode))
    print(f"PolisProof on http://{args.host}:{args.port} mode={args.mode.upper()}")
    server.serve_forever()


if __name__ == "__main__":
    main()
