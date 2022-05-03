
# Write team member names here: 


'''
Base class file for Cache
Credit: R. Martin (W&M), A. Jog (W&M), Ramulator (CMU)
'''

import numpy as np
from math import log2
import random


class Cache:
    def __init__(self, cSize, ways=1, bSize=4):
        
        self.cacheSize = cSize  # Bytes
        self.ways = ways        # Default: 1 way (i.e., directly mapped)
        self.blockSize = bSize  # Default: 4 bytes (i.e., 1 word block)
        self.sets = cSize // bSize // ways

        self.blockBits = 0
        self.setBits = 0

        if (self.blockSize != 1):
            self.blockBits = int(log2(self.blockSize))

        if (self.sets != 1):
            self.setBits = int(log2(self.sets))

        self.cache = np.zeros((self.sets, self.ways, self.blockSize), dtype=int)
        self.cache = self.cache - 1

        self.metaCache = np.zeros((self.sets, self.ways), dtype=int)
        self.metaCache = self.metaCache - 1

        self.hit = 0
        self.miss = 0
        self.hitlatency = 1 # cycle
        self.misspenalty = 10 # cycle

    def reset(self):
        self.cache = np.zeros((self.sets, self.ways, self.blockSize), dtype=int)
        self.cache = self.cache - 1

        self.metaCache = np.zeros((self.sets, self.ways), dtype=int)
        self.metaCache = self.metaCache - 1

        self.hit = 0
        self.miss = 0
        
    '''
    Warning: DO NOT EDIT ANYTHING ABOVE THIS LINE
    '''


    '''
    Returns the set number of an address based on the policy discussed in the class
    Do NOT change the function definition and arguments
    '''

    def find_set(self, address):
        start = self.blockBits
        end = start + self.setBits
        return (address >> start) - ((address >> end) << (end - start))

    '''
    Returns the tag of an address based on the policy discussed in the class
    Do NOT change the function definition and arguments
    '''

    def find_tag(self, address):
        start = self.blockBits + self.setBits
        return address >> start

    '''
    Search through cache for address
    return True if found
    otherwise False
    Do NOT change the function definition and arguments
    '''

    def find(self, address):
        found = False
        set = self.find_set(address)
        tag = self.find_tag(address)
        for i in range(0,len(self.metaCache[set])):
            if self.metaCache[set][i] == tag:
                found = True
                block = self.cache[set][i]
                for j in range(0, i):  # Move all blocks to the right. Rightmost block is overwritten
                    self.metaCache[set][j+1] = self.metaCache[set][j]
                    self.cache[set][j+1] = self.cache[set][j]
                self.metaCache[set][0] = tag
                self.cache[set][0] = block
                break
        if found:
            self.hit = self.hit + 1.0
        return found

    '''
    Load data into the cache. 
    Something might need to be evicted from the cache and send back to memory
    Do NOT change the function definition and arguments
    '''

    def load(self, address):
        set = self.find_set(address)
        tag = self.find_tag(address)
        for i in range(1, len(self.metaCache[set])):        #Move all blocks to the right. Rightmost block is overwritten
            self.metaCache[set][i] = self.metaCache[set][i-1]
            self.cache[set][i] = self.cache[set][i-1]
        self.metaCache[set][0] = tag
        for i in range(0, self.blockSize):                  #Insert new block into position 0
            self.cache[set][0][i] = address + i
        print(self.metaCache[set])
        #print(self.cache[set])
