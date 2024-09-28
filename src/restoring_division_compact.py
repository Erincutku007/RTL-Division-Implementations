# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 12:54:25 2024

@author: erincutku
"""
import random
#decimal integer to binary conversion, taken from
#https://www.geeksforgeeks.org/python-program-to-convert-a-number-into-32-bit-binary-format/
#not needed in the algorithm, it was used whie debugging the code.
def convert_to_binary(number):
    binary_32_bit = ""
    for _ in range(32):
        binary_32_bit = str(number & 1) + binary_32_bit
        number >>= 1
    return binary_32_bit

#finds the number of leading zeros in a integer's binary representation
def leading_zeros(binary):
    index = 0
    for i in range(31,-1,-1):
        mask = 1<<i
        if (mask & binary) == 0:
            index += 1
            mask >>1
        else:
            return index
    return 0
        
a = random.randint(0, 10000)
b = random.randint(0, 50)
def restoring_divide_compact(a,b):
    res = 0
    remainders = []
    
    b_zeros = leading_zeros(b)
    
    #leave 0 at the MSB bit and allign everytihng to the 30'th bit of the register
    b_shifted = b << (b_zeros - 1) #leaving 1 bit padding for sign bit
    
    #number of iterations needed for the algorithm
    lenght = b_zeros
    
    #si0 equals to a itself.
    s_i = a
    for i in range(lenght):
        #trial subtraction
        s_i_temp = s_i - b_shifted
        #this is redundant, I wanted to extract the sign bit, which is the MSB of the register.
        #At the same time I wanted to keep the sign bit in radix 2 to stick to binary implementation.
        sign = 0 if ( (s_i_temp & (1<<31)) ==0 ) else 1
        #if sign is 0 the result is positive.
        if sign==0:
            res += 1
            s_i = s_i_temp
        #break at the needed width 
        if i == lenght-1:
            return res,remainders
        else:
            s_i <<=1
            res <<=1
res,remainders = restoring_divide_compact(a,b)
print("elde edilen sonuc = "+ str(res) + " beklenen sonuc = " + str(a//b))