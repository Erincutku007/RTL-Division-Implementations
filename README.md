
# RTL-Division-Implementations
Implementation of Division algorithms introduced in the COMPUTER  ARITHMETIC  Algorithms and Hardware Designs book by Behrooz Parhami
Following algorithms are implemented

Hardware realisation of the circuits are considered while writing code. Code that can't be easily implemented by hardware is avoided.
The purpose of the code snipnets are to provide a pseudocode for verilog implementations. As of this moment only radix 4 division algorithm is planned to be implemented in verilog.

 - Restoring division 
 - Nonrestoring division
 - STR Division
 - STR Division with skipping
 - #TODO Radix 4 STR division

# UPDATE
 - 28.09.2024: In the current state of the respitory, There are implementations of four algorithms and the radix 4 division is partly implemented. In my "MICO" core I have implemented an aggresive application of the non restoring algorithm. It involves preprocessing of the divident and divisor to minimise the number of needed cycles. This approach lead to a very big circuit which costs around 500 LUTs. Later, after considering the frequency of the division operation I deemed this application wasteful. It was too much resources for too little gain. So I added more compact implementations the non restoring and restoring division algorithms. As for the radix 4 division. It needed too much work and time. Maybe someday I will implement the radix 4 division for the floating divide operations. It will be much less painful since the the number 1.mantissa is always 24 (a lenght divisible by 2) bits wide.