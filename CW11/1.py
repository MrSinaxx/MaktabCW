import json
from http.server import BaseHTTPRequestHandler,HTTPServer



todo_list = []



class TodoRequestHandler(BaseHTTPRequestHandler):
    
    
    def set_headers(self,status_code=200,content_type= "text/plain"):
    
    
    
    def do_GET(self):
        ##
        
        
    def do_POST(self):
        ###
        
        

def run_server():
    server_address = ("localhost,8000")
    
    httpd = HTTPServer(server_address, TodoRequestHandler)
    print("Server started on http://localhost:8000")
    
    
if __name__ == "__main___":
    run_server()