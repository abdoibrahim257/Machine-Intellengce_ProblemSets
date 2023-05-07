from typing import Tuple, List
import utils

'''
    The DecipherResult is the type defintion for a tuple containing:
    - The deciphered text (string).
    - The shift of the cipher (non-negative integer).
        Assume that the shift is always to the right (in the direction from 'a' to 'b' to 'c' and so on).
        So if you return 1, that means that the text was ciphered by shifting it 1 to the right, and that you deciphered the text by shifting it 1 to the left.
    - The number of words in the deciphered text that are not in the dictionary (non-negative integer).
'''
DechiperResult = Tuple[str, int, int]

def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:
    '''
        This function takes the ciphered text (string)  and the dictionary (a list of strings where each string is a word).
        It should return a DechiperResult (see above for more info) with the deciphered text, the cipher shift, and the number of deciphered words that are not in the dictionary. 
    '''
    #TODO: ADD YOUR CODE HERE
    newDic = {}
    for i in dictionary:
        newDic[i] = "lol"

    minCount = float('inf')
    splited = ciphered.split(" ")
    ciph = {}
    for i in range(26):
        tempString = []
        count = 0
        for word in splited:
            z = ""
            for letter in word:
                z  += chr(((ord(letter)-97 - i) % 26)+97)
            if(not newDic.get(z)):
                count +=1
            tempString.append(z)
        tempString = " ".join(tempString)
        if(count < minCount):
            minCount = count
            ciph = (tempString, i , minCount)
    return ciph
