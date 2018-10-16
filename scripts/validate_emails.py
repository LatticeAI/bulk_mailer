from validate_email import validate_email
import argparse
from queue import Queue

import threading
import time

class parseThread(threading.Thread):
    def __init__(self, email, q, group=None, target=None, name="thread", args=(), kwargs=None, verbose=None):
        super(parseThread,self).__init__()

        self.group  = group
        self.target = target
        self.name   = name

        self.email = email
        self.q     = q

    def run(self):

        is_valid = validate_email(self.email, verify=True)
        self.q.put( (self.email,is_valid) )
        print("{} {}".format(self.email,is_valid))

        return

parser = argparse.ArgumentParser()
parser.add_argument('-in_file')
parser.add_argument('-out_file')

args = parser.parse_args()

emails = open(args.in_file).readlines()
emails = [e.replace('\n','') for e in emails]

threads = []
q = Queue(maxsize=len(emails))

for e in emails:
    print("starting {}".format(e))
    t = parseThread(e,q)
    t.start()
    threads.append(t)

for t in threads:
    t.join()

f = open(args.out_file,'w')
f.write("email, validity\n")

print("writing emails...")
while not q.empty():

    e, is_valid = q.get()
    print("{} {}".format(e,is_valid))
    if is_valid:
        f.write("{}, {}\n".format(e,'valid'))
    else:
        f.write("{}, {}\n".format(e,'not valid'))

f.close()
