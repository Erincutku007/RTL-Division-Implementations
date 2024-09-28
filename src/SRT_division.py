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

def SRT_divide(a,b):
    res = []
    remainders = []
    
    a_zeros = (leading_zeros(abs(a)))
    b_zeros = (leading_zeros(abs(b)))
    
    a_shifted = a << (a_zeros - 1) #leaving 1 bit padding for sign bit
    b_shifted = b << (b_zeros - 1) #leaving 1 bit padding for sign bit
    
    #number of iterations needed for the algorithm
    lenght = (31-a_zeros) - (31-b_zeros) + 1
    
    #si0 equals to a itself.
    s_i = a_shifted
    #b_shifted_binary = convert_to_binary(b_shifted)
    
    
    for i in range(lenght):
        s_i_binary = convert_to_binary(s_i)
        shamt = (a_zeros - 1) + i
        remainders.append(s_i >> shamt) #since we are using an redundant representation we have to
        #store the values in a list. Refer to the book for the redundant binary representation to
        #binary representation transformation.
        
        s_i_sign = 0 if ( (s_i & (1<<31)) ==0 ) else 1
        
        first_two_bits = s_i_binary[0:2]
        
        g_e_one_over_two = (first_two_bits == "01") #Check if the s_i is greater or equal to 1/2
        l_minus_one_over_two = (first_two_bits == "10") #Check if the s_i is less than -1/2
        
        s_i_within_range = not(g_e_one_over_two or l_minus_one_over_two)
        
        #This part of the division will need a priotiy encoder circuit and shift register with
        #variable shamt
        
        leading_zeros_amt = leading_zeros(s_i)
        
        if s_i_within_range:
            res.append(0)
        else:
            if g_e_one_over_two:
                res.append(1)
                s_i -= b_shifted
            else:
                res.append(-1)
                s_i += b_shifted
        s_i_binary = convert_to_binary(s_i)
        
        if i == lenght:
            break
        else:
            s_i <<=1
    s_i_sign = 0 if ( (s_i & (1<<31)) ==0 ) else 1 #Redo the si sign just for a good measure
    
    
    result = redundant_to_standart_binary(res)#This step can be implemented on the fly
    #I tried to write the code in a way that can be easily realised with hardware.
    #radix conversion can be implemented with a FSM on the fly.
    if s_i_sign:
        result -= 1 #reduce one to compansate
    return result,remainders
'''
a = 23423
b = 215
result,remainders = SRT_divide(a,b)
print("sonuc %d olmaliydi ama %d bulundu" % (int(a/b),result))
'''

for index in range(10000):
    a = random.randint(1, 10000)
    b = random.randint(1, 1000)
    result,remainders = SRT_divide(a,b)
    if result != int(a/b):
        print("sonuc %d olmaliydi ama %d bulundu" % (a//b,result))
        break
print("sorunsuz calisti")

'''
result,res = SRT_divide(a,b)
print(','.join(str(x) for x in res))
print("elde edilen sonuc = "+ str(result) + " beklenen sonuc = " + str(a//b))
'''