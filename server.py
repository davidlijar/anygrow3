# server.py
import socketio
import eventlet


sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ):
    print("Client connected:", sid)
    # Start sending "hello world" message continuously once client is connected
    eventlet.spawn(send_hello_world, sid)


@sio.event
def message(sid, data):

    print("Message from", sid, ":", data)
    if data == "ON" or data == "MOOD" or data == "OFF":
        sio.emit("ledState", data)
    else:
        sio.emit("msgFromSerial", {"sensor_data": data})


def send_hello_world(sid):
    while True:
        sio.emit("hello", {"message": "Hello, world!"}, room=sid)
        eventlet.sleep(1)  # Send message every second


@sio.event
def disconnect(sid):
    print("Client disconnected:", sid)


if __name__ == "__main__":

    eventlet.wsgi.server(eventlet.listen(("10.2.24.16", 8000)), app)
