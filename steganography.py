# author: Ugonna Ezeokoli
# date: Feb 20, 2023
# file: steganography.py a Python program that implements a stategy for decoding and encoding a message
# input: user responses (strings)
# output: prints result of the message in binary and text form

# steganography
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from math import ceil
from codec import Codec, CaesarCypher # HuffmanCodes

class Steganography():
    
    def __init__(self):
        self.text = ''
        self.binary = ''
        self.delimiter = '#'
        self.codec = None

    def encode(self, filein, fileout, message, codec):
        image = cv2.imread(filein)
        # print(image) # for debugging
        
        # calculate available bytes
        max_bytes = image.shape[0] * image.shape[1] * 3 // 8
        print("Maximum bytes available:", max_bytes)

        # convert into binary
        if codec == 'binary':
            self.codec = Codec() 
        elif codec == 'caesar':
            self.codec = CaesarCypher()
        elif codec == 'huffman':
            self.codec = HuffmanCodes()
        binary = self.codec.encode(message+self.delimiter)
        
        # check if possible to encode the message
        num_bytes = ceil(len(binary)//8) + 1 
        if  num_bytes > max_bytes:
            print("Error: Insufficient bytes!")
        else:
            print("Bytes to encode:", num_bytes) 
            self.text = message
            self.binary = binary
            # your code goes here
            # you may create an additional method that modifies the image array
            index = 0
            done = False
            for row in image:
                if done:
                    break
                for pixel in row:
                    # This will check each pixel and change the pixel to match last bit of encoded message
                    if int(pixel[0] % 2) != int(binary[index]):
                        if int(pixel[0]) == 255:    # if at 255 already, will go one down instead
                            pixel[0] -= 1
                        else:
                            pixel[0] += 1
                    index += 1     
                    if index == len(binary):
                        done = True
                        break
                    if int(pixel[1] % 2) != int(binary[index]):
                        if int(pixel[1]) == 255:
                            pixel[1] -= 1
                        else:
                            pixel[1] += 1
                    index += 1
                    if index == len(binary):
                        done = True
                        break
                    if int(pixel[2] % 2) != int(binary[index]):
                        if int(pixel[2]) == 255:
                            pixel[2] = int(pixel[2]) - 1
                        else:
                            pixel[2] = int(pixel[2]) + 1
                    index += 1
                    if index == len(binary):
                        done = True
                        break
            cv2.imwrite(fileout, image)
                   
    def decode(self, filein, codec):
        image = cv2.imread(filein)
        #print(image) # for debugging      
        flag = True
        huff = False #Finds a different way to check delimeter
        
        # convert into text
        if codec == 'binary':
            self.codec = Codec() 
            delim_len = 8
        elif codec == 'caesar':
            self.codec = CaesarCypher()
            delim_len = 8
        elif codec == 'huffman':
            self.codec = HuffmanCodes()
            print(self.codec.bi_delim)
            huff = True
            if self.codec == None or self.codec.name != 'huffman':
                print("A Huffman tree is not set!")
                flag = False
        if flag:
            # your code goes here
            # you may create an additional method that extract bits from the image array
            binary_data = ""
            delim_found = False
            for row in image:
                if delim_found:
                    break
                for pixel in row:
                    # if pixel point is even then adds 0 bit and 1 bit if point is odd
                    if pixel[0] % 2 == 0:
                        binary_data = binary_data + "0"
                    else:
                        binary_data = binary_data + "1"
                    delim_found = self.check_delimeter(binary_data,self.codec, huff)
                    # if delimeter found, loop ends
                    if delim_found:
                        break
                    if pixel[1] % 2 == 0:
                        binary_data = binary_data + "0"
                    else:
                        binary_data = binary_data + "1"
                    delim_found = self.check_delimeter(binary_data,self.codec, huff)
                    if delim_found:
                        break
                    if pixel[2] % 2 == 0:
                        binary_data = binary_data + "0"
                    else:
                        binary_data = binary_data + "1"
                    delim_found = self.check_delimeter(binary_data,self.codec, huff)
                    if delim_found:
                        break

            # update the data attributes:
            self.text = self.codec.decode(binary_data)
            self.binary = binary_data              
    
    # This function will check the last 8 bits and return if delimeter is found
    def check_delimeter(self, data,codec, huff):
        if huff:
            if len(data) % len(self.codec.bi_delim) == 0:
                if data[-len(self.codec.bi_delim):] == self.codec.bi_delim:
                    return True
            else:
                return False
        else:
            if len(data) % 8 == 0:
                if data[-8:] == codec.encode("#"):
                    return True
            else:
                return False

    def print(self):
        if self.text == '':
            print("The message is not set.")
        else:
            print("Text message:", self.text)
            print("Binary message:", self.binary)          

    def show(self, filename):
        plt.imshow(mpimg.imread(filename))
        plt.show()

if __name__ == '__main__':
    
    s = Steganography()

    s.encode('fractal.jpg', 'fractal.png', 'hello', 'binary')
    # NOTE: binary should have a delimiter and text should not have a delimiter
    assert s.text == 'hello'
    assert s.binary == '011010000110010101101100011011000110111100100011'

    s.decode('fractal.png', 'binary')
    assert s.text == 'hello'
    assert s.binary == '011010000110010101101100011011000110111100100011'
    print('Everything works!!!')
   
