from http.server import HTTPServer, CGIHTTPRequestHandler

def log(message):
    print(f"[ {message} ]")

SERVER_ADDRESS = ("127.0.0.1", 5555)

log("Starting a CGI server")


httpd = HTTPServer(SERVER_ADDRESS, CGIHTTPRequestHandler)
httpd.serve_forever()