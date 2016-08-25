import zmq
from zmq.eventloop import ioloop, zmqstream
import urwid
from gviewer import AsyncDataStore, GViewer, BaseDisplayer, Text, Group, View


ioloop.install()

CHANNEL = "tcp://127.0.0.1:5581"


class Displayer(BaseDisplayer):
    def summary(self, message):
        return message[0]

    def get_views(self):
        return [("View", self.detail)]

    def detail(self, message):
        return View([Group("Summary", [Text(message[0])])])


def print_message(message):
    print message


def main():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(CHANNEL)
    socket.setsockopt(zmq.SUBSCRIBE, "")
    zmq_stream = zmqstream.ZMQStream(socket)

    data_store = AsyncDataStore(zmq_stream.on_recv)
    viewer = GViewer(data_store, Displayer(),
                     event_loop=urwid.TornadoEventLoop(ioloop.IOLoop.instance()))
    viewer.start()


if __name__ == "__main__":
    main()
