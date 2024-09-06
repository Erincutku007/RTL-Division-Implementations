# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 12:54:25 2024

@author: erincutku
"""
import random
#decimal integer to binary conversion, taken from
#https://www.geeksforgeeks.org/python-program-to-convert-a-number-into-32-bit-binary-format/
#not needed in the algorithm, it was used while debugging the code.
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
def redundant_to_standart_binary(number):
    res_reversed = reversed(number) #this is needed because enumerate starts indexing the list from the
    result = 0
    for i in enumerate(res_reversed):#This step transforms the results from redundant radix 2 base
    #to binary radix 2 base.
    #example conversion:
    #-1 1 1 = (-1)*4 + 1*2 + 1*1 = -1. Pay attention to the powers of two.
        power,val = i
        power = 2**power
        result += val*power
    return result

def nonrestoring_divide(a,b):
    res = []
    remainders = []
    
    a_zeros = (leading_zeros(abs(a)))
    b_zeros = (leading_zeros(abs(b)))
    
    #leave two 0's at the MSB bit and allign everytihng to the 29'th bit of the register
    #since there will changes of sign in the s_i we we need to keep the sign even after left shift
    #ie if s_i is 011... after left shift we will get 11... which is negative.
    a_shifted = a << (a_zeros - 2) #leaving 1 bit padding for sign bit
    b_shifted = b << (b_zeros - 2) #leaving 1 bit padding for sign bit
    
    #number of iterations needed for the algorithm
    lenght = (31-a_zeros) - (31-b_zeros) + 1
    
    #si0 equals to a itself.
    s_i = a_shifted
    #b_shifted_binary = convert_to_binary(b_shifted)
    
    b_sign = 0 if ( (b & (1<<31)) ==0 ) else 1
    a_sign = 0 if ( (a & (1<<31)) ==0 ) else 1
    
    for i in range(lenght):
        #s_i_binary = convert_to_binary(s_i)
        shamt = (a_zeros - 2) + i
        remainders.append(s_i >> shamt) #since we are using an redundant representation we have to
        #store the values in a list. Refer to the book for the redundant binary representation to
        #binary representation transformation.
        
        s_i_sign = 0 if ( (s_i & (1<<31)) ==0 ) else 1
        
        if s_i_sign == b_sign:
            res.append(1)
            s_i -= b_shifted
        else:
            res.append(-1)
            s_i += b_shifted
        #s_i_binary = convert_to_binary(s_i)
        if i == lenght:
            break
        else:
            s_i <<=1
    s_i_sign = 0 if ( (s_i & (1<<31)) ==0 ) else 1 #Redo the si sign just for a good measure
    
    result_sign_flag = 0 if ( s_i_sign == a_sign ) else 1 #raise the flag if sign(a) != sign(s_i)
    
    result = redundant_to_standart_binary(res)#This step can be implemented on the fly
    #I tried to write the code in a way that can be easily realised with hardware.
    #radix conversion can be implemented with a FSM on the fly.
    if result_sign_flag:
        result += 1 if b_sign else -1 #reduce one to compansate
    return result,remainders
'''
a = 650
b = -83
result,remainders = nonrestoring_divide(a,b)
print("sonuc %d olmaliydi ama %d bulundu" % (int(a/b),result))
'''
'''
for index in range(1000):
    print(index)
    a = random.randint(1, 10000)
    b = -random.randint(1, 1000)
    result,remainders = nonrestoring_divide(a,b)
    if result != int(a/b):
        print("sonuc %d olmaliydi ama %d bulundu" % (a//b,result))
        break
print("sorunsuz calisti")
'''
'''
result,remainders = nonrestoring_divide(a,b)
print(','.join(str(x) for x in res))
print("elde edilen sonuc = "+ str(result) + " beklenen sonuc = " + str(a//b))
'''