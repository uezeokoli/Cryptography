# author: Ugonna Ezeokoli
# date: Feb 20, 2023
# file: codec.py a Python program that implements coding and encoding a message
# input: parameters of the function take input from 
# output: the encoded or decoded form of a message

# codecs
import numpy as np

class Codec():
    
    def __init__(self):
        self.name = 'binary'
        self.delimiter = '#' 

    # convert text or numbers into binary form    
    def encode(self, text):
        if type(text) == str:
            return ''.join([format(ord(i), "08b") for i in text])
        else:
            print('Format error')

    # convert binary data into text
    def decode(self, data):
        binary = []        
        for i in range(0,len(data),8):
            byte = data[i: i+8]
            if byte == self.encode(self.delimiter): # you need to find the correct binary form for the delimiter
                break
            binary.append(byte)
        text = ''
        for byte in binary:
            text += chr(int(byte,2))       
        return text 
    

class CaesarCypher(Codec):

    def __init__(self, shift=3):
        self.name = 'caesar'
        self.delimiter = '#'  
        self.shift = shift    
        self.chars = 256      # total number of characters

    # convert text into binary form
    # your code should be similar to the corresponding code used for Codec
    def encode(self, text):
        data = ''
        # your code goes here
        # index = (ord(character) + self.shift) % 256
        if type(text) == str:
            data = ''.join([format((ord(i) + self.shift) % 256, "08b") for i in text])
        else:
            print('Format error')
        return data
    
    # convert binary data into text
    # your code should be similar to the corresponding code used for Codec
    def decode(self, data):
        text = ''
        # your code goes here
        binary = []        
        for i in range(0,len(data),8):
            byte = data[i: i+8]
            if byte == self.encode(self.delimiter): # you need to find the correct binary form for the delimiter
                break
            binary.append(byte)
        for byte in binary:
            text += chr(int(byte,2)-self.shift)       
        return text

# a helper class used for class HuffmanCodes that implements a Huffman tree
class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.left = left
        self.right = right
        self.freq = freq
        self.symbol = symbol
        self.code = ''
        
# class HuffmanCodes(Codec):
    
#     def __init__(self):
#         self.nodes = None
#         self.name = 'huffman'
#         self.delimiter = "#"
#         self.bi_delim = ''
#         self.data = ""
#         self.chars = ''

#     # make a Huffman Tree    
#     def make_tree(self, data):
#         # make nodes
#         nodes = []
#         for char, freq in data.items():
#             nodes.append(Node(freq, char))
            
#         # assemble the nodes into a tree
#         while len(nodes) > 1:
#             # sort the current nodes by frequency
#             nodes = sorted(nodes, key=lambda x: x.freq)

#             # pick two nodes with the lowest frequencies
#             left = nodes[0]
#             right = nodes[1]

#             # assign codes
#             left.code = '0'
#             right.code = '1'

#             # combine the nodes into a tree
#             root = Node(left.freq+right.freq, left.symbol+right.symbol,
#                         left, right)

#             # remove the two nodes and add their parent to the list of nodes
#             nodes.remove(left)
#             nodes.remove(right)
#             nodes.append(root)
#         self.nodes = nodes
#         return nodes

#     # traverse a Huffman tree
#     def traverse_tree(self, node, val):
#         next_val = val + node.code
#         # data = ""
#         if(node.left):
#             self.traverse_tree(node.left, next_val)
#         if(node.right):
#             self.traverse_tree(node.right, next_val)
#         if(not node.left and not node.right):
#             # print(f"{node.symbol}->{next_val}") # this is for debugging
#             if "#" == node.symbol:
#                 self.bi_delim = next_val
#             for val in self.chars:
#                 if node.symbol == val:
#                     self.data = self.data.replace(val,next_val)
#             # you need to update this part of the code
#             # or rearrange it so it suits your needs

#     # convert text into binary form
#     def encode(self, text):
#         data = ''
#         # your code goes here
#         self.data = text
#         data_dic = {}
#         self.chars = set(text)
#         for val in self.chars:
#             data_dic[val] = text.count(val)            
#         # you need to make a tree
#         nodes = self.make_tree(data_dic)
#         self.traverse_tree(nodes[0],data)
#         data = self.data


#         return data

#     # convert binary data into text
#     def decode(self, data):
#         text = ''
#         current_node = self.nodes[0] # start at the root of the tree
#         for bit in data:
#             if bit == '0': # if the bit is 0, move to the left 
#                 current_node = current_node.left
#             elif bit == '1': # if the bit is 1, move to the right
#                 current_node = current_node.right
#             if not current_node.left and not current_node.right: # if leaf node reached, add character to decoded text and start again from the root
#                 if current_node.symbol == self.delimiter: #Checks for the delimiter and returns text when found
#                     return text
#                 text += current_node.symbol
#                 current_node = self.nodes[0]

# driver program for codec classes
if __name__ == '__main__':
    text = 'hello' 
    #text = 'Casino Royale 10:30 Order martini' 
    print('Original:', text)
    
    c = Codec()
    binary = c.encode(text + c.delimiter)
    # NOTE: binary should have a delimiter and text should not have a delimiter
    print('Binary:', binary) # should print '011010000110010101101100011011000110111100100011'
    data = c.decode(binary)  
    print('Text:', data)     # should print 'hello'
    
    cc = CaesarCypher()
    binary = cc.encode(text + cc.delimiter)
    # NOTE: binary should have a delimiter and text should not have a delimiter
    print('Binary:', binary)
    data = cc.decode(binary) 
    print('Text:', data)     # should print 'hello'
     
    # h = HuffmanCodes()
    # binary = h.encode(text + h.delimiter)
    # # NOTE: binary should have a delimiter and text should not have a delimiter
    # print('Binary:', binary)
    # data = h.decode(binary)
    # print('Text:', data)     # should print 'hello'

