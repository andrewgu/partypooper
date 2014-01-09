import os.path
import re
import time
import BaseHTTPServer
#HOST_NAME = 'localhost'
HOST_NAME = ''
PORT_NUMBER = 15567 # Maybe set this to 9000.

MIME_TYPES = {None:"text/html",
    ".html" :"text/html",
    ".js": "text/javascript",
    ".css": "text/css",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".svg": "image/svg+xml"}

# Very restrictive definitions of file resources. Because what do you think this is, Apache?
FILE_RE = re.compile("^[a-z0-9]+(\\.[a-z0-9]+)?$", re.I)
CHECK_RE = re.compile("^\\/(\\?[0-9]+)?$", re.I)

doorOpened = False

def sendPlaintextResponse(s, text):
    s.send_response(200)
    s.send_header("Content-type", "text/plaintext")
    s.end_headers()
    s.wfile.write(text)

def send404(s):
    s.send_response(404)
    s.send_header("Content-type", "text/plaintext")
    s.end_headers()
    s.wfile.write("File not found.")

def getContentTypeFromPath(ext):
    if ext in MIME_TYPES:
        return MIME_TYPES[ext]
    else:
        return "application/octet-stream"

def sendLocalFile(s):
    filepath = os.path.join("app/", s.path[5:])
    print(filepath)
    pathmatch = FILE_RE.match(s.path[5:])
    if pathmatch != None and os.path.isfile(filepath):
        with open(filepath, "rb") as f:
            s.send_response(200)
            s.send_header("Content-type", getContentTypeFromPath(pathmatch.group(1)))
            s.end_headers()
            s.wfile.write(f.read())
    else:
        send404(s)
    
class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(s):
        global doorOpened
        if s.path == "/opened":
            doorOpened = True
            sendPlaintextResponse(s, "Acknowledged. Opened.")
        elif s.path == "/closed":
            doorOpened = False
            sendPlaintextResponse(s, "Acknowledged. Closed.")
        else:
            send404(s)
    
    def do_GET(s):
        global doorOpened
        if s.path == "/opened":
            doorOpened = True
            sendPlaintextResponse(s, "Acknowledged. Opened.")
        elif s.path == "/closed":
            doorOpened = False
            sendPlaintextResponse(s, "Acknowledged. Closed.")
        elif CHECK_RE.match(s.path) != None:
            if doorOpened:
                sendPlaintextResponse(s, "opened")
            else:
                sendPlaintextResponse(s, "closed")
        elif s.path.startswith("/app/") and len(s.path) > 5 and not ("/" in s.path[5:] or "\\" in s.path[5:]):
            sendLocalFile(s)
        else:
            send404(s)
            

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print (time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print (time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))