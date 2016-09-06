import zmq
import time


CHANNEL = "tcp://*:5581"


def main():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind(CHANNEL)
    index = 0
    while True:
        index += 1
        socket.send_string(u"Message {0}".format(index))
        print "Message Sent"
        time.sleep(0.2)


if __name__ == "__main__":
    main()
