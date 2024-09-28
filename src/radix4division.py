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
def redundant_to_standart_binary_base4(number):
    res_reversed = reversed(number) #this is needed because enumerate starts indexing the list from the
    result = 0
    for i in enumerate(res_reversed):#This step transforms the results from redundant radix 2 base
    #to binary radix 2 base.
    #example conversion:
    #-1 1 1 = (-1)*4 + 1*2 + 1*1 = -1. Pay attention to the powers of two.
        power,val = i
        power = 4**power
        result += val*power
    return result

def nonrestoring_divide(a,b):
    #since we are using an redundant representation we have to
    #store the values in a list. Refer to the book for the redundant binary representation to
    #binary representation transformation.
    res = []
    remainders = []
    
    a_bin_raw = convert_to_binary(a)
    b_bin_raw = convert_to_binary(b)
    
    a_zeros = (leading_zeros(abs(a)))
    b_zeros = (leading_zeros(abs(b)))
    
    a_shifted = a << (a_zeros - 3)
    b_shifted = b << (b_zeros - 3)
    
    if (b_zeros%2 == 1):
        b_shifted >>= 1
        b_zeros += 1
    if (a_zeros%2 == 1):
        a_shifted >>= 1
        a_zeros += 1
    
    a_bin = convert_to_binary(a_shifted)
    b_bin = convert_to_binary(b_shifted)

    #number of iterations needed for the algorithm
    lenght = int((32-a_zeros)/2) - int((32-b_zeros)/2) +1
    
    #si0 equals to a itself.
    s_i = a_shifted
    #b_shifted_binary = convert_to_binary(b_shifted)
    
    b_sign = 0 if ( (b & (1<<31)) ==0 ) else 1
    a_sign = 0 if ( (a & (1<<31)) ==0 ) else 1
    
    b_3bits = b_bin[3:6]
    
    del(a_bin_raw)
    del(b_bin_raw)
    
    for i in range(lenght+1):
        s_i_binary = convert_to_binary(s_i)
        shamt = (a_zeros - 1) + 2*i
        remainders.append(s_i >> shamt) 
        
        s_i_sign = 0 if ( (s_i & (1<<31)) ==0 ) else 1 #Redo the si sign just for a good measure
        s_i_3_mag_bits = s_i_binary[1:4] #magnatute bits are needed for mapping of the p-d plot.
        
        #sign bit carries the sign data. I will work with abs values so I can use the same functions
        #for positive and negative s_i values.
        if s_i_sign == 1:
            abs_int_s_i_3_mag_bits = -int(s_i_3_mag_bits,2)
            s_i_3_mag_bits = convert_to_binary(abs_int_s_i_3_mag_bits)[-3:]
        
        #My IDE does not support python case statements(match) so I will use if conditions
        if s_i_sign == 0:
            if (s_i_3_mag_bits == "000"):
                res.append(0)
            elif(s_i_3_mag_bits == "001"):
                res.append(1)
                s_i -= b_shifted
            elif( (s_i_3_mag_bits == "010") or ( (s_i_3_mag_bits == "011") and (b_3bits[1] == '1') )):
                res.append(2)
                s_i -= 2*b_shifted
            elif( (s_i_3_mag_bits[0] == '1') or ( (s_i_3_mag_bits == "011") and (b_3bits[1] == '0') )):
                res.append(3)
                s_i -= 3*b_shifted
        else:
            #same conditions, but now actions are performed with inversed signs.
            if (s_i_3_mag_bits == "000"):
                res.append(0)
            elif(s_i_3_mag_bits == "001"):
                res.append(-1)
                s_i += b_shifted
            elif( (s_i_3_mag_bits == "010") or ( (s_i_3_mag_bits == "011") and (b_3bits[1] == '1') )):
                res.append(-2)
                s_i += 2*b_shifted
            elif( (s_i_3_mag_bits[0] == '1') or ( (s_i_3_mag_bits == "011") and (b_3bits[1] == '0') )):
                res.append(-3)
                s_i += 3*b_shifted
        s_i_binary = convert_to_binary(s_i)
        if (res[0] != 0) and (i == lenght-1):
            break
        else:
            s_i <<=2
            
    s_i_sign = 0 if ( (s_i & (1<<31)) ==0 ) else 1 #Redo the si sign just for a good measure
    
    result_sign_flag = 0 if ( s_i_sign == a_sign ) else 1 #raise the flag if sign(a) != sign(s_i)
    
    result = redundant_to_standart_binary_base4(res)#This step can be implemented on the fly
    #I tried to write the code in a way that can be easily realised with hardware.
    #radix conversion can be implemented with a FSM on the fly.
    if result_sign_flag:
        result += 1 if b_sign else -1 #reduce one to compansate
    return result,remainders

a = 73
b = 68
result,remainders = nonrestoring_divide(a,b)
print("sonuc %d olmaliydi ama %d bulundu" % (int(a/b),result))

'''
for index in range(1000):
    print(index)
    a = random.randint(1, 100)
    b = random.randint(1, 100)
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