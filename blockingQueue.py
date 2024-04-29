#!/usr/bin/env python

import queue
import threading


class blockingQueue:
    def __init__(self, size: int):
        self.size = size
        self.empty = threading.Semaphore(self.size) # initialize to size
        self.full = threading.Semaphore(0) # initialize to 0

        self.conventionalQ = queue.Queue(self.size)
        self.qLock = threading.Lock()
        
    def put(self, item):
        self.empty.acquire() # decrements empty
        self.qLock.acquire()
        self.conventionalQ.put(item)
        self.qLock.release()
        self.full.release() # increments full

    def get(self):
        self.full.acquire() # decrements full
        self.qLock.acquire()
        item = self.conventionalQ.get()
        self.qLock.release()
        self.empty.release() # decrements empty

        return item
        
    
