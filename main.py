import threading
import subprocess


def run_continuous_printing():
    subprocess.run(["python", "master.py"])


def run_websocket_server():
    subprocess.run(["python", "server.py"])


def flaskhttpserver():
    subprocess.run(["python", "web.py"])


if __name__ == "__main__":
    # Create threads for each script
    t1 = threading.Thread(target=run_continuous_printing)
    t2 = threading.Thread(target=run_websocket_server)
    t3 = threading.Thread(target=flaskhttpserver)

    # Start the threads
    t1.start()
    t2.start()
    t3.start()

    # Wait for the threads to finish (which they won't, since they run indefinitely)
    t1.join()
    t2.join()
    t3.join()
