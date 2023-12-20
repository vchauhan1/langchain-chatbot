from flask import Flask, render_template
from flask_socketio import SocketIO
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import SystemMessage, HumanMessage
from langchain.memory import ChatMessageHistory
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

history = ChatMessageHistory()

@app.route('/chat')
def index():
    return render_template('index.html')

def generate_response(user_input):
    history.add_message(HumanMessage(content=user_input))
    messages = history.messages
    chat = ChatOpenAI()
    
    for chunk in chat.stream(messages):
        socketio.sleep(0)
        response_content = chunk.content
        socketio.emit('receive_message', {'data': chunk.content})
        time.sleep(0.5)

    history.add_message(SystemMessage(content=response_content))


@socketio.on('send_message')
def handle_message(json):
    user_input = json['message']
    socketio.start_background_task(generate_response, user_input)

if __name__ == '__main__':
    socketio.run(app, debug=True)


