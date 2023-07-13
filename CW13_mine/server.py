import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class User:
    def __init__(self, id, name, username, password):
        self.id = id
        self.name = name
        self.username = username
        self.password = password


class Message:
    def __init__(self, id, from_user, to_user, content, subject):
        self.id = id
        self.from_user = from_user
        self.to_user = to_user
        self.content = content
        self.subject = subject


class HTTPManagerRequestHandler(BaseHTTPRequestHandler):
    users = {}
    messages = {}
    current_user = None

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(body)

        if self.path == '/signup':
            self.handle_signup(data)
        elif self.path == '/login':
            self.handle_login(data)
        elif self.path == '/send_message':
            self.handle_send_message(data)
        elif self.path == '/view_inbox':
            self.handle_view_inbox()
        elif self.path == '/view_sent_messages':
            self.handle_view_sent_messages()
        elif self.path == '/mark_as_seen':
            self.handle_mark_as_seen(data)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def handle_signup(self, data):
        user_id = len(self.users) + 1
        name = data['name']
        username = data['username']
        password = data['password']
        user = User(user_id, name, username, password)
        self.users[username] = user
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Signup successful')

    def handle_login(self, data):
        username = data['username']
        password = data['password']

        if username in self.users and self.users[username].password == password:
            self.current_user = self.users[username]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Login successful')
        else:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'Unauthorized')

    def handle_send_message(self, data):
        if self.current_user is None:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'Unauthorized')
            return

        to_user = data['to_user']
        content = data['content']
        subject = data['subject']

        if to_user not in self.users:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'To user not found')
            return

        message_id = len(self.messages) + 1
        message = Message(message_id, self.current_user.username, to_user, content, subject)
        self.messages[message_id] = message

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Message sent successfully')

    def handle_view_inbox(self):
        if self.current_user is None:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'Unauthorized')
            return

        inbox = [msg for msg in self.messages.values() if msg.to_user == self.current_user.username]

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps([msg.__dict__ for msg in inbox]).encode('utf-8'))

    def handle_view_sent_messages(self):
        if self.current_user is None:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'Unauthorized')
            return

        sent_messages = [msg for msg in self.messages.values() if msg.from_user == self.current_user.username]

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps([msg.__dict__ for msg in sent_messages]).encode('utf-8'))

    def handle_mark_as_seen(self, data):
        if self.current_user is None:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'Unauthorized')
            return

        message_id = data['message_id']

        if message_id not in self.messages:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Message not found')
            return

        message = self.messages[message_id]

        if message.to_user != self.current_user.username:
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'Unauthorized')
            return

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Message marked as seen')


def run_server():
    host = 'localhost'
    port = 8000
    server = HTTPServer((host, port), HTTPManagerRequestHandler)
    print(f'Server running on {host}:{port}')
    server.serve_forever()


if __name__ == '__main__':
    run_server()
