# law.py
# ----------------------------------------------------------------------
# Author: 		Desmond Qiu
# Version:		1.2
# Date:			12/8/2019 -
#                 Started
#               13/8/2019 -
#                 Add Word class and import datetime
#               14/8/2019 -
#                 Draft revise function
#                 Change Menu() to PrintMenu()
#                 Add number of items found when loading
#               15/8/2019 -
#                 Remove PrintMenu() and add sorting algorithm for revise
#                 Update SearchWord() to SearchSimilar() which searches
#                 for similar words and display the results
#               16/8/2019 - 
#                 Added SaveCurrentWork and LoadHistory
#               17/8/2019 - 
#                 Added SearchSimilar
#               18/8/2019 - 
#                 Amended OptionOne and OptionTwo
#               19/8/2019 - 
#                 Finalised OptionOne and OptionTwo
# ----------------------------------------------------------------------
# imports
import datetime

# ----------------------------------------------------------------------
# global variables
# file name to read
filen = 'history.txt'
# dictionary
mydict = {}

# ----------------------------------------------------------------------
# class Word
# This class is designed to represent each word. It contains setters
# and display methods to modify and handle each instances of the class.
class Word(object):
    # ------------------------------------------------------------------
    # Constructor
    def __init__(self):
        self.word = 'DEFAULT'  # the word
        self.sentences = []  # list of sentences related to the word
        self.lastRevised = '0-0-0 00:00:00'  # last revised datetime
        # for word
        self.count = 0  # the number of times that word was revised

    # ------------------------------------------------------------------
    # Appends the list of sentences
    def SetSentence(self, sentence):
        self.sentences.append(sentence)

    # ------------------------------------------------------------------
    # For development purposes, checking of each values
    def ShowValues(self):
        print(self.word, end='; ')
        print(self.count, end='; ')
        print(self.lastRevised, end='; ')
        for s in self.sentences:
            print(s, end='; ')
        print('\n')

    # ------------------------------------------------------------------
    # Prints the short version of the word object
    def ToShort(self):
        print(f'Word: {self.word}')
        print(f'Examples: ')
        index = 1
        for s in self.sentences:
            print(f'  {index}. {s}')
            index += 1

    # ------------------------------------------------------------------
    # Prints the long version of the word object
    def ToLong(self):
        print(f'Word: {self.word}')
        print(f'No of revisions made: {self.count}')
        print(f'Last revised on: {self.lastRevised}')
        print(f'Examples: ')
        index = 1
        for s in self.sentences:
            print(f'  {index}. {s}')
            index += 1


# End of class
# ----------------------------------------------------------------------
# Description: 	Gets an option from the user
# Input: 		n - The number of available options
# Return: 		The option selected by the user
def ReadOption(n):
    while True:
        try:
            op = int(input('Enter option:'))
            if op > 0 and op <= n:
                break
            else:
                print('Option entered is not valid')
        except ValueError:
            print('No blanks and numbers only')
    return op


# ----------------------------------------------------------------------
# Description: 	Gets the word from the user
# Input: 		None
# Return: 		w - The word to be added
def ReadWord():
    while True:
        w = input('Enter word:')
        w = clear(w)
        if w == '':
            print('Cannot enter blank')
        elif ' ' in w:
            print('Enter 1 word only')
        else:
            import re
            w = re.sub(r'[^A-Za-z]+', '', w)
            break
    return w


# ----------------------------------------------------------------------
# Description: 	Gets the sentence from the user
# Input: 		None
# Return: 		s - The sentence
def ReadSentence():
    while True:
        s = input('Enter example sentence:')
        s = clear(s)
        if s == '' or s == ' ':
            print('Cannot enter blank')
        else:
            break
    return s


# ----------------------------------------------------------------------
# Description: 	Gets yes or no input from user
# Input: 		None
# Return: 		ans - The sentence
def ReadYesNo():
    while True:
        ans = input('Enter y or n:')
        ans = clear(ans)
        if ans == 'Y':
            break
        elif ans == 'N':
            break
        else:
            print('Enter y or n only')
            
    return ans


# ----------------------------------------------------------------------
# Description:  Cleans the input string, removes any white spaces and
#               capitalises the first character of the string.
# Input: 		s - The input string (word or sentence)
# Return: 		s - The cleaned string (word or sentence)
def clear(s=''):
    s = s.lower()
    # s = s.replace(',', '')
    s = s.strip()  # lstrip() or rstrip() or strip()
    s = s.capitalize()  # cap first letter
    return s


# ----------------------------------------------------------------------
# Description: 	Inserts a word and sentence into the dictionary. Method
#               will check if word exists then inserts the sentence into
#               existing list.
# Input: 		None
# Return: 		None
def CallOptionOne():
    # print('You selected option 1')
    # get input from user
    word = ReadWord()
    isExist = mydict.get(word)

    if isExist:  # if word exist
        tmp_w = mydict[word]
        # display existing example sentences
        print('')
        tmp_w.ToShort()
        print('')
        print("Word already exist")
        print('Do you want to add an example sentence?')
        ans = ReadYesNo()
        # ask for yes or no
        # if yes
        if ans == 'Y':
            print('Yes received')
            # get new sentence from user
            sentence = ReadSentence()
            # append the exiting list
            tmp_w.SetSentence(sentence)
            print('New sentence added successfully')
        # if no
        elif ans == 'N':
            print('No received')
        
        dt = (
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        tmp_w.lastRevised = dt
        mydict[word] = tmp_w
    else:
        # get new sentence from user
        sentence = ReadSentence()
        # create word object
        wObj = Word()
        wObj.word = word
        wObj.SetSentence(sentence)
        dt = (
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        wObj.lastRevised = dt
        # insert into dictionary as new word
        mydict[word] = wObj
        print('New word added successfully')
    
    print('Returning to menu')


# ----------------------------------------------------------------------
# Description:  This method contains additional actions which inclues
#               generating sorted list or searching for words
# Input: 		o - The seleted option
# Return: 		None
def CallOptionTwo(o=0):
    if o == 3:
        SearchSimilar()
        return  # skip the rest

    li_sorted = []
    for obj in mydict.values():
        li_sorted.append({'word': obj.word, 'count': obj.count,
                          'lastRevised': obj.lastRevised, 'sentences': obj.sentences})

    print(f'{len(li_sorted)} result(s) found')
    print('-' * 50)
    index = 1  # for indexing
    # sort depends on option seleted
    if o == 1:
        # by recent revised
        li_sorted.sort(reverse=True, key=recent)
        # for each dictionary in sorted list
        for d in li_sorted:
            tmp_w = d['word']
            tmp_dt = d['lastRevised']
            print(f'{index}. {tmp_w} (Revised on {tmp_dt})')
            index += 1
    elif o == 2:
        # by number of revisions made
        li_sorted.sort(reverse=True, key=most)
        # for each dictionary in sorted list
        for d in li_sorted:
            tmp_w = d['word']
            tmp_c = d['count']
            print(f'{index}. {tmp_w} (Revised {tmp_c} times)')
            index += 1

    li_sorted.clear()  # release memory
    print('-' * 50)

    # get input from user
    print('Which word would you like to revise?')
    word = ReadWord()
    isExist = mydict.get(word)
    print('-' * 50)
    if isExist:  # if word exist
        tmp_w = mydict[word]
        # display existing example sentences
        tmp_w.ToShort()
        # update last revised and count
        tmp_w.count += 1
        dt = (
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        tmp_w.lastRevised = dt
    else:
        print(f'{word} does not exist')
    print('-' * 50)

# ----------------------------------------------------------------------
# Description: 	For sorting usage, see CallOptionTwo()
# Input: 		None
# Return: 		None
def recent(obj):
    return obj['lastRevised']


# ----------------------------------------------------------------------
# Description: 	For sorting usage, see CallOptionTwo()
# Input: 		None
# Return: 		None
def most(obj):
    return obj['count']


# ----------------------------------------------------------------------
# Description: 	Searches the dictionary for similar items according to
#               the keyword entered. Any items found will be complied
#               into a list and display to the user.
# Input: 		None
# Return: 		None
def SearchSimilar():
    keyword = ''
    print('What would you like to search for?')
    while True:
        keyword = input('Enter Keyword:')
        keyword = clear(keyword)
        if keyword == '':
            print('Cannot enter blank')
        else:
            break

    print('-' * 50)
    li = []
    index = 1
    # for each word in dictionary
    for w in mydict.values():
        # if keyword found in word
        if keyword.lower() in str(w.word).lower():
            # add to list
            li.append(w)
            # change last revised datetime and increment count
            #w.count += 1
            #w.lastRevised = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            # display short string of the data
            print(f'{index}. {w.word}')
            index += 1
    
    # if list is empty
    if len(li) == 0:
        print('No result(s) found')
    elif len(li) == 1:
        tmp_w = li[0]
        print('-' * 50)
        tmp_w.ToShort()
        tmp_w.count += 1
        dt = (
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        tmp_w.lastRevised = dt
    else:
        print('-' * 50)
        # get input from user
        print('Which word would you like to revise?')
        word = ReadWord()
        print('-' * 50)
        isExist = mydict.get(word)
        if isExist:  # if word exist
            tmp_w = mydict[word]
            # display existing example sentences
            tmp_w.ToShort()
            # update last revised and count
            tmp_w.count += 1
            dt = (
                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            tmp_w.lastRevised = dt
        else:
            print(f'{word} does not exist')

    print('-' * 50)
    li.clear()  # release memory


# ----------------------------------------------------------------------
# Description: 	Save the current state of the dictionary into a file
# Input: 		outFile - The file to write to
# Return: 		None
def SaveCurrentWork(outFile):
    delimiter = '|'
    # write file
    for key in mydict:  # for each word in dictionary
        # concatenate or build the string with line
        line = str(mydict[key].word) + delimiter
        line += str(mydict[key].count) + delimiter
        line += str(mydict[key].lastRevised) + delimiter
        # get last index to add '\n'
        i = 0
        lastIndex = len(mydict[key].sentences) - 1
        while i <= lastIndex:
            line += mydict[key].sentences[i]
            if i == lastIndex:  # if last item in list
                line += '\n'
            else:
                line += delimiter
            i += 1
        outFile.write(line)
    outFile.close()  # always close when not in use


# ----------------------------------------------------------------------
# Description: 	Loads the existing history text file and extracts the
#               the data into the main dictonary.
# Input: 		inFile - The file to read from
# Return: 		None
def LoadHistory(inFile):
    # read file
    print('Word Reviser v1.0')
    print(f'Loading from {filen}')
    if inFile:  # if not null
        items = 0
        while True:
            line = inFile.readline()
            line = line.replace('\n', '')
            if line:  # if not empty or null
                items += 1
                token = line.split('|')
                if len(token) > 0:
                    word = token[0]
                    count = int(token[1])
                    dt = token[2]

                    wObj = Word()
                    wObj.word = word
                    wObj.count = count
                    wObj.lastRevised = dt
                    i = 3
                    while i < len(token):
                        wObj.SetSentence(token[i])
                        i += 1
                    # put into mydict
                    mydict[word] = wObj
            else:
                break
        inFile.close()  # always close when not in use
        print(f'Load completed')
    else:
        print('No history found')


# ----------------------------------------------------------------------
# Start of program
try:
    # load the file
    LoadHistory(open(filen, 'r'))
except IOError:
    print(f'{filen} does not exist')
    print('Creating new copy')
except ValueError:
    print(f'{filen} is not compatible')
    print('Please remove file first before continuing')
    print('Program terminating')
    quit()

while True:
    # print menu and get input from user
    print('\nWhat would you like to do?')
    print('  1 - Add new word')
    print('  2 - Revise a word')
    print('  3 - Quit')
    option = ReadOption(3)
    if option == 1:  # if user selects option 1
        CallOptionOne()
    elif option == 2:  # if user selects option 2
        if len(mydict) == 0:
            print('No words to revise')
            print('Add a new word to start revising!')
        else:
            print('How would you like to revise?')
            print('  1 - Display recently revised')
            print('  2 - Display most revised')
            print('  3 - Search by keyword')
            op = ReadOption(3)
            CallOptionTwo(op)
    elif option == 3:  # option to allow user to
        # terminate program and save work
        print('Program terminating')
        print('Have a nice day!')
        break

    SaveCurrentWork(open(filen, 'w'))  # save current work

# after user terminates
try:
    SaveCurrentWork(open(filen, 'w'))
except IOError:
    print(f'Unable to save work to {filen}')
# ----------------------------------------------------------------------
