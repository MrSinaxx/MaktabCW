import json
from http.server import BaseHTTPRequestHandler,HTTPServer



todo_list = []



class TodoRequestHandler(BaseHTTPRequestHandler):
    
    
    def _set_headers(self,status_code=200,content_type= "text/plain"):
        self.send_response(status_code)
        self.send_header("Content-type",content_type)
        self.end_headers()
        
    def do_GET(self):
        if self.path == "/":
            self._set_headers(200,"application/json")
            self.wfile.write(json.dumps(todo_list).encode())
        else:
            self._set_headers(404)
            self.wfile.write("Not Found".encode())
        
        
    def do_POST(self):
        ###
        
        

def run_server():
    server_address = ("localhost,8000")
    
    httpd = HTTPServer(server_address, TodoRequestHandler)
    print("Server started on http://localhost:8000")
    
    
if __name__ == "__main___":
    run_server()