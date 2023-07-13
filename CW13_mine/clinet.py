import requests
import json

base_url = 'http://localhost:8000'


def signup():
    name = input('Enter your name: ')
    username = input('Enter a username: ')
    password = input('Enter a password: ')

    data = {
        'name': name,
        'username': username,
        'password': password
    }

    response = requests.post(f'{base_url}/signup', json=data)
    print(response.text)


def login():
    username = input('Enter your username: ')
    password = input('Enter your password: ')

    data = {
        'username': username,
        'password': password
    }

    response = requests.post(f'{base_url}/login', json=data)
    print(response.text)


def send_message():
    to_user = input('Enter the username of the recipient: ')
    subject = input('Enter the message subject: ')
    content = input('Enter the message content: ')

    data = {
        'to_user': to_user,
        'subject': subject,
        'content': content
    }

    response = requests.post(f'{base_url}/send_message', json=data)
    print(response.text)


def view_inbox():
    response = requests.post(f'{base_url}/view_inbox')
    if response.status_code == 200:
        messages = json.loads(response.text)
        for msg in messages:
            print(f'From: {msg["from_user"]} | Subject: {msg["subject"]} | Content: {msg["content"]}')
    else:
        print(response.text)


def view_sent_messages():
    response = requests.post(f'{base_url}/view_sent_messages')
    if response.status_code == 200:
        messages = json.loads(response.text)
        for msg in messages:
            print(f'To: {msg["to_user"]} | Subject: {msg["subject"]} | Content: {msg["content"]}')
    else:
        print(response.text)


def mark_as_seen():
    message_id = input('Enter the ID of the message to mark as seen: ')

    data = {
        'message_id': message_id
    }

    response = requests.post(f'{base_url}/mark_as_seen', json=data)
    print(response.text)


def menu():
    print('HTTP Manager Client')
    print('1. Signup')
    print('2. Login')
    print('3. Send Message')
    print('4. View Inbox')
    print('5. View Sent Messages')
    print('6. Mark Message as Seen')
    print('0. Exit')


def main():
    while True:
        menu()
        choice = input('Enter your choice: ')

        if choice == '1':
            signup()
        elif choice == '2':
            login()
        elif choice == '3':
            send_message()
        elif choice == '4':
            view_inbox()
        elif choice == '5':
            view_sent_messages()
        elif choice == '6':
            mark_as_seen()
        elif choice == '0':
            break
        else:
            print('Invalid choice. Please try again.')


if __name__ == '__main__':
    main()
