import dictionary
import random

class Opener:
    def __init__(self):
        self.resultfile = open("result.txt", "a")
        self.ansfile = open("pastans.txt", "r")

        self.anslist = []
        for i in self.ansfile:
            self.anslist.append(i.split(" ")[0].lower())
        self.wordlist = dictionary.words + self.anslist

    # letters in first guess
    def revealed(self, wordle, guess):
        revealed = 0
        dup = []
        for i in wordle:
            if (i in guess):
                if (guess.count(i) > 1 and i not in dup):
                    revealed += wordle.count(i)
                    dup.append(i)
                elif (guess.count(i) == 1):
                    revealed += 1
        return float(revealed)


    # check if word has correct positions
    def checkPos(self, word, lettersInWord, notInPosition, notInWord):
        for i in range(5):
            if (word[i] in notInWord):
                return False
            if (lettersInWord[i] != ' '):
                if (lettersInWord[i] != word[i]):
                    return False
            if (word[i] in notInPosition[i]):
                return False
        return True

    def weight(self, wordListCopy, wordsUsed):
        weight = []
        currentWord = wordsUsed[len(wordsUsed) - 1]

        #optimization 1
        if (len(wordListCopy) >= 100):
            for word in wordListCopy:
                maxi = max(len(set(word)-set(currentWord)), len(set(currentWord)-set(word)))
                weight.append(maxi)
            return wordListCopy[weight.index(max(weight))]
        else:
            rand = random.choice(wordListCopy)
            #duplicates in dictionary
            if (rand == 'FALSE'):
                while (rand == 'FALSE'):
                    rand = random.choice(wordListCopy)
                return rand
            else:
                return rand

    def allguesses(self, wordle, guess):
        lst = [False] * 5
        lettersInCorrectPosition = [' '] * 5
        notInPosition = [[],[],[],[],[]]
        notInWord = []
        wordsUsed = [guess]

        #starting guess
        for i in range(5):
            if (guess[i] == wordle[i]):
                lst[i] = True
                lettersInCorrectPosition[i] = guess[i]
            elif (guess[i] in wordle):
                notInPosition[i].append(guess[i])
            else:
                notInWord.append(guess[i])

        #random guesses
        wordListCopy = self.wordlist[:]

        while (not all(lst)):
            for word in self.wordlist:
                if (word in wordListCopy and not self.checkPos(word, lettersInCorrectPosition, notInPosition, notInWord)):
                    wordListCopy.remove(word)

            randomword = self.weight(wordListCopy, wordsUsed)
            wordsUsed.append(randomword)

            for i in range(5):
                if (randomword[i] == wordle[i]):
                    lst[i] = True
                    lettersInCorrectPosition[i] = randomword[i]
                elif (randomword[i] in wordle):
                    notInPosition[i].append(guess[i])
                else:
                    notInWord.append(randomword[i])

        return len(wordsUsed)



    def firstguess(self, wordle, guess):
        lettersInCorrectPosition = [' '] * 5
        notInPosition = [[], [], [], [], []]
        notInWord = []
        wordsUsed = [guess]

        for i in range(5):
            if (guess[i] == wordle[i]):
                lettersInCorrectPosition[i] = guess[i]
            elif (guess[i] in wordle):
                notInPosition[i].append(guess[i])
            else:
                notInWord.append(guess[i])

        wordListCopy = self.wordlist[:]

        for word in self.wordlist:
            if (word in wordListCopy and not self.checkPos(word, lettersInCorrectPosition, notInPosition, notInWord)):
                wordListCopy.remove(word)

        return ((len(self.wordlist) - len(wordListCopy)) / float(len(self.wordlist))) * 100


    # word / avg score / words reduced / avg letters revealed / percentage solved
    def loop(self):
        length = len(self.anslist)
        openers = ["salet", "crate", "mourn"]

        for word in openers:
            avgSolve = 0.0
            avgFirstGuess = 0.0
            avgRevealed = 0.0
            solved = 0.0
            for wordle in self.anslist:
                solve = self.allguesses(wordle, word)
                if (solve <= 6):
                    solved += 1
                avgSolve += solve
                avgFirstGuess += self.firstguess(wordle, word)
                avgRevealed += self.revealed(wordle, word)

            self.resultfile.write(str(word) + ' '
                                  + str(avgSolve/length) + ' '
                                  + str(avgFirstGuess/length) + ' '
                                  + str(avgRevealed/length) + ' '
                                  + str(solved/length) + '/n')
a = Opener()
a.loop()




