import utils

def palindrome_check(string: str) -> bool:
    '''
    This function takes string and returns where a string is a palindrome or not
    A palindrome is a string that does not change if read from left to right or from right to left
    Assume that empty strings are palindromes
    '''
    #TODO: ADD YOUR CODE HERE
    #the basic idea is to reverse the string and compare with the original one in a for loop 
    rev= string[::-1]
    if string == rev or string == "''":
        return True
    else:
        return False