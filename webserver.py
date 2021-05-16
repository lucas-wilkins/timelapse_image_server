
from http.server import CGIHTTPRequestHandler
from socketserver import TCPServer
import argparse




parser = argparse.ArgumentParser()
parser.add_argument("-p", "--timelapse_pid", help="timelapse process to report on", type=int, default=None)
parser.add_argument("--port", help="port to run connection on", type=int, default=80)
args = parser.parse_args()

class EsotericHandler(CGIHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        kwargs["directory"] = "web"
        super().__init__(*args, **kwargs)

    def end_headers(self):
        self.no_cache_options()
        super().end_headers()

    def no_cache_options(self):
        if self.path.endswith("-nocache.png") or "status.txt" in self.path:
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.send_header("Pragma", "no-cache")
            self.send_header("Expires", "0")



class EsotericServer(TCPServer):
    def __init__(self, *args, **kwargs):
        self.server_name = "timelapse_server"
        self.server_port = args[0][1]
        super().__init__(*args, **kwargs)

with EsotericServer(("", args.port), EsotericHandler) as httpd:
    print("serving at port", args.port)
    httpd.serve_forever()




