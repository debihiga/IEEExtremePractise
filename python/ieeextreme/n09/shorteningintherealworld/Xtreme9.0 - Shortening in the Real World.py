#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import io

def readline(reader):
    return reader.readline().replace("\n","")

def getEncodedUTF8(src):
    encoded = []
    for c in src:
        encoded.append(ord(c))
    return encoded

"""
1) An xor cipher is applied to the target URL, 
using the base URL of your company as a repeating key. 
Here we perform a bitwise exclusive-or between each byte of the target URL and the base URL. 

If the target URL is shorter than the base URL of your company, 
you would truncate the base URL so that the lengths are equal. 

If the base URL of your company is shorter than the target URL, 
you would repeat the base URL as many times as needed to make the lengths equal.
"""
def getXorCiphered(target_url, base_url):
    base_url_corrected = []
    if len(target_url)<len(base_url):
        # Truncate base url
        base_url_corrected = base_url[:len(target_url)]
    elif len(base_url)<len(target_url):
        # Repeat base url
        i = 0
        while(len(base_url_corrected)!=len(target_url)):
            base_url_corrected.append(base_url[i])
            i += 1
            if not i<len(base_url):
                i = 0
    else:
       base_url_corrected = base_url
        
    ciphered_url = []
    for i in range(len(target_url)):
        ciphered_url.append(hex(target_url[i]^base_url_corrected[i]))
    #print(ciphered_url)
    return ciphered_url

"""
2) Take the last 8 bytes of the output from step 1, 
and convert this to the corresponding unsigned integer. 
(See the example below for more details.)
"""
def getLast8Bytes2Int(url):
    value_hex = url[len(url)-8:]
    value_str = ""
    for h in value_hex:
        value_str += h[2:].zfill(2)
    #print(value_str)
    return int(value_str, 16)

"""
3) Encode this unsigned integer using Base62 encoding. 
In this encoding, you convert the integer to a base 62 number, 
where the digits 0-9 represent values 0-9, 
lowercase letters a-z represent values 10-35, 
and capital letters A-Z represent values 36-61.
"""
def getBase62Encoded(num):
    return Base62Encode(num)



BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def Base62Encode(num, alphabet=BASE62):
    """Encode a positive number in Base X

    Arguments:
    - `num`: The number to encode
    - `alphabet`: The alphabet to use for encoding
    """
    if num == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        num, rem = divmod(num, base)
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)

def Base62Decode(string, alphabet=BASE62):
    """Decode a Base X encoded string into the number

    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1

    return num

def main(argv):

    reader = io.open(sys.stdin.fileno())

    base_url = readline(reader)
    base_url_encoded = getEncodedUTF8(base_url)
    #print(base_url_encoded)

    n = int(readline(reader))

    encoded_urls = []

    for i in range(n):

        target_url = readline(reader)
        #print(target_url)

        # 1) Process URL using UTF-8 encoding.
        target_url_encoded = getEncodedUTF8(target_url)
        #print(target_url_encoded)

        # 2) Apply exclusive or cipher.
        target_url_ciphered = getXorCiphered(target_url_encoded, base_url_encoded)

        # 3) Get last 8 bytes to int.
        bytes = getLast8Bytes2Int(target_url_ciphered)
        #print(bytes)

        # Encode Base 62
        encoded = getBase62Encoded(bytes)
        #print(encoded)

        encoded_url = base_url+"/"+encoded
        encoded_urls.append(encoded_url)

        """
        
        Number in base 62:	Btazwa9mke
        Number in base 10:	161046954426247172

        """
    for encoded_url in encoded_urls:
        print(encoded_url)

if __name__ == "__main__":
    main(sys.argv)