
import sys
import io
import string

save_input_in_memory = False
# Better not to store input in memory and use reader.
results = []

def getABCDic():
    abc_dic = {}
    for character in list(string.ascii_lowercase):
        abc_dic[character] = 0
    return abc_dic

#abc_dic = getABCDic()

def main(argv):

    lines = []
    reader = None
    if save_input_in_memory:
        for line in sys.stdin:
            lines.insert(0, line)
    else:
        reader = io.open(sys.stdin.fileno())

    n_testcases = 0

    # T: Number of test cases.
    # 1<=T<=100
    if save_input_in_memory:
        T = int(lines.pop())
    else:
        T = int(reader.readline())
    #print(T)


    while n_testcases<T:

        n_words = 0
        n_dictionary_strings = 0

        if save_input_in_memory:
            D, S = getDnS(lines.pop())
        else:
            D, S = getDnS(reader.readline())
        #print(D)
        #print(S)

        if save_input_in_memory:
            words, abc_max = getWords(lines, D)
        else:
            words, abc_max = getWords(reader, D)
        #print(words)

        for i in range(S):
            if save_input_in_memory:
                potential_dictionary_string = lines.pop().replace("\n","")
            else:
                potential_dictionary_string = reader.readline().replace("\n","")
            # 1<=len(dictionary_string)<=40,000
            analyzePotentialDictionaryString(potential_dictionary_string, abc_max)

        n_testcases = n_testcases + 1

    for result in results:
        print(result)

def getDnS(line):
    #line = reader.readline()
    numbers = line.split(" ")
    # D: number of words in a dictionary
    # 1 <= D
    D = int(numbers[0])
    # S: number of potential dictionary strings to be checked
    # S <= 100
    S = int(numbers[1])
    return D, S

def getWords(lines, n_words):
    words = []
    abc = getABCDic()
    for i in range(n_words):
        if save_input_in_memory:
            words.append(lines.pop().replace("\n",""))
        else:
            words.append(lines.readline().replace("\n",""))
        for character, value in abc.items():
            n_occurence_in_word = words[i].count(character)
            if abc[character] < n_occurence_in_word:
                abc[character] = n_occurence_in_word
    return words, abc

    """
def analyzePotentialDictionaryString(potential_dictionary_string, words):


    global abc_dic

    #print(abc_dic)

    occurences_in_dic = abc_dic.copy()
    missing = abc_dic.copy()
    max_usages = abc_dic.copy()

    while 0<len(potential_dictionary_string):

        character = potential_dictionary_string[0]
        occurences_in_dic[character] = potential_dictionary_string.count(character)
        potential_dictionary_string = potential_dictionary_string.replace(character, "")

    #print(occurences_in_dic)

    for word in words:

        #print(word)
        while 0<len(word):

            character = word[0]
            n_occurences_in_word = word.count(character)
            n_occurences_in_dic = occurences_in_dic[character]

            if n_occurences_in_dic < n_occurences_in_word:
                n_missing = n_occurences_in_word - n_occurences_in_dic
                if missing[character]<n_missing:
                    missing[character] = n_missing

            elif max_usages[character] < n_occurences_in_word:
                max_usages[character] = n_occurences_in_word

            word = word.replace(character, "")

    n_total_missing = 0
    for character, n_missing in missing.items():
        n_total_missing = n_total_missing + n_missing

    are_extra_characters = False
    for character, n_usages in max_usages.items():
        if n_usages < occurences_in_dic[character]:
            are_extra_characters = True
            break

    if 0<n_total_missing:
        print("No " + str(n_total_missing))
    elif are_extra_characters:
        print("Yes No")
    else:
        print("Yes Yes")
    """

    """
def analyzePotentialDictionaryString(potential_dictionary_string, words):
    global abc_dic

    # print(abc_dic)

    occurences_in_dic = abc_dic.copy()
    missing = abc_dic.copy()
    max_usages = abc_dic.copy()
    potential_dictionary_list = list(potential_dictionary_string)

    while 0 < len(potential_dictionary_list):
        character = potential_dictionary_list[0]
        occurences_in_dic[character] = potential_dictionary_list.count(character)
        while potential_dictionary_list.count(character) > 0:
            potential_dictionary_list.remove(character)

    # print(occurences_in_dic)

    for word in words:

        # print(word)
        while 0 < len(word):

            character = word[0]
            n_occurences_in_word = word.count(character)
            n_occurences_in_dic = occurences_in_dic[character]

            if n_occurences_in_dic < n_occurences_in_word:
                n_missing = n_occurences_in_word - n_occurences_in_dic
                if missing[character] < n_missing:
                    missing[character] = n_missing

            elif max_usages[character] < n_occurences_in_word:
                max_usages[character] = n_occurences_in_word

            word = word.replace(character, "")

    n_total_missing = 0
    for character, n_missing in missing.items():
        n_total_missing = n_total_missing + n_missing

    are_extra_characters = False
    for character, n_usages in max_usages.items():
        if n_usages < occurences_in_dic[character]:
            are_extra_characters = True
            break

    if 0 < n_total_missing:
        print("No " + str(n_total_missing))
    elif are_extra_characters:
        print("Yes No")
    else:
        print("Yes Yes")

    """

"""
def count(string, c):
    count = 0
    for character in string:
        if character in c:
            count += 1
    return count
"""
def analyzePotentialDictionaryString(potential_dictionary_string, abc_max):

    n_total_missing = 0
    are_extra_characters = False

    #potential_dictionary_string = ''.join(sorted(potential_dictionary_string))

    for character in list(string.ascii_lowercase):

        n_occurences_in_potential_dictionary_string = potential_dictionary_string.count(character)
        #n_occurences_in_potential_dictionary_string = count(potential_dictionary_string, character)
        # Timeouts
        #potential_dictionary_string = potential_dictionary_string.replace(character, "")
        # Timeouts with replacing (even when sorting before)
        #potential_dictionary_string = potential_dictionary_string.translate(str.maketrans('', '',character))
        # RunTime Error maketrans

        n_max_occurences_in_words = abc_max[character]

        if n_occurences_in_potential_dictionary_string<n_max_occurences_in_words:
            n_total_missing = n_total_missing + (n_max_occurences_in_words-n_occurences_in_potential_dictionary_string)
        #if potential_dictionary_string=="penleantopan":
        #    print(n_total_missing)
        #    print(n_max_occurences_in_words)
        #    print(n_occurences_in_potential_dictionary_string)

        if n_total_missing==0:
            if n_max_occurences_in_words<n_occurences_in_potential_dictionary_string:
                are_extra_characters = True
                #break
                # Cant. Need to figure out if it is not dictionary string first.

    if 0 < n_total_missing:
        results.append("No " + str(n_total_missing))
    elif are_extra_characters:
        results.append("Yes No")
    else:
        results.append("Yes Yes")

"""
To qualify as a Dictionary String, 
all the letters needed to explicitly form each word of the dictionary 
must be present in the string. 
You cannot reuse letters. 

Thus, the string aab is not a Dictionary String 
for a dictionary containing the word aaa since this word needs 3 a's 
whereas the candidate Dictionary String has only two a's.

String without any extra characters is a Perfect Dictionary String.

anteplop is Dictionary String and Perfect Dicstionary String of:
    ant
    top
    open
    apple
    lean
    
penleantopan
    ant 
    
"""

if __name__ == "__main__":
    main(sys.argv)