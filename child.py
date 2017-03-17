import sys
import zerorpc

print "\n".join(sys.argv)

class HelloRPC(object):
    def hello(self, name):
        return "Hello, %s" % name

s = zerorpc.Server(HelloRPC())
s.bind("tcp://0.0.0.0:4242")
s.run()