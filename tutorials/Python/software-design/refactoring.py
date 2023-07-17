"""
Non-flexible code, works for its initial purpose but stops working once
an extra word is added. Not easily customizable, delimiter has to be changed 
everywhere in the print statement.
"""
word_list = ['hello', 'yes', 'goodbye', 'last']
print(word_list[0] + ', ' + word_list[1] + ', ' + word_list[2] + ', ' + word_list[3])
word_list = ['hello', 'yes', 'goodbye', 'last', 'again', 'middle']
print(word_list[0] + ', ' + word_list[1] + ', ' + word_list[2] + ', ' + word_list[3])

"""
Refactored
"""
word_list = ['hello', 'yes', 'goodbye', 'last', 'again', 'middle']
print(', '.join(word_list))

"""
in a function
"""
def print_words(words: list[str], delimiter: str = ', '):
    print(delimiter.join(words))

print_words(word_list, ' | ')