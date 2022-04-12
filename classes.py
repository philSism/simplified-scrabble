import random
import os
from itertools import permutations


class SakClass:

    def __init__(self):

        self.letters = ['Α', 'Α', 'Α', 'Α', 'Α', 'Α', 'Α', 'Α', 'Α', 'Α', 'Α', 'Α',
                        'Ο', 'Ο', 'Ο', 'Ο', 'Ο', 'Ο', 'Ο', 'Ο', 'Ο',
                        'Ε', 'Ε', 'Ε', 'Ε', 'Ε', 'Ε', 'Ε', 'Ε',
                        'Ι', 'Ι', 'Ι', 'Ι', 'Ι', 'Ι', 'Ι', 'Ι',
                        'Τ', 'Τ', 'Τ', 'Τ', 'Τ', 'Τ', 'Τ', 'Τ',
                        'Η', 'Η', 'Η', 'Η', 'Η', 'Η', 'Η',
                        'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ', 'Σ',
                        'Ν', 'Ν', 'Ν', 'Ν', 'Ν', 'Ν', 'Ν',
                        'Ρ', 'Ρ', 'Ρ', 'Ρ', 'Ρ',
                        'Κ', 'Κ', 'Κ', 'Κ', 'Π', 'Π', 'Π', 'Π', 'Υ', 'Υ', 'Υ', 'Υ',
                        'Λ', 'Λ', 'Λ', 'Μ', 'Μ', 'Μ', 'Ω', 'Ω', 'Ω',
                        'Γ', 'Γ', 'Δ', 'Δ', 'Β', 'Φ', 'Χ', 'Ζ', 'Θ', 'Ξ', 'Ψ']

        self.points = {'Α': 1, 'Ο': 1, 'Ε': 1, 'Ι': 1, 'Τ': 1, 'Η': 1, 'Σ': 1, 'Ν': 1, 'Ρ': 2, 'Κ': 2, 'Π': 2, 'Υ': 2,
                       'Λ': 3, 'Μ': 3, 'Ω': 3, 'Γ': 4, 'Δ': 4, 'Β': 8, 'Φ': 8, 'Χ': 8, 'Ζ': 10, 'Θ': 10, 'Ξ': 10, 'Ψ': 10}

    def get_letters(self, number_of_letters):

        new_letters = []
        self.randomize_sak()
        letter_list_size = len(self.letters)

        if letter_list_size > number_of_letters:
            for i in range(number_of_letters):
                new_letters.append(self.letters.pop())
        elif letter_list_size <= number_of_letters:
            for i in range(letter_list_size):
                new_letters.append(self.letters.pop())

        return new_letters

    def randomize_sak(self):

        random.shuffle(self.letters)

    def put_back_letters(self, returning_letters):

        for i in range(7):
            self.letters.append(returning_letters[i])

    def check_empty(self):

        if len(self.letters) == 0:
            return True
        else:
            return False


class Player:

    def __init__(self, name):

        self.name = name
        self.points = 0
        self.round_letters = []
        self.number_of_moves = 0
        self.game_end = False

    def fill_letters(self, sak):

        self.round_letters += sak.get_letters(7 - len(self.round_letters))

    def discard_letters(self, sak):

        sak.put_back_letters(self.round_letters)
        self.round_letters = sak.get_letters(7)

    def remove_used_letters(self, word):

        for letter in word:
            for i in range(len(self.round_letters)):
                if self.round_letters[i] == letter:
                    del self.round_letters[i]
                    break

    def check_letters(self, word):

        found = False
        check_list = permutations(self.round_letters, len(word))

        for line in check_list:
            check_word = ''.join(line)
            if word == check_word:
                found = True

        return found

    def check_end(self):

        return self.game_end

    def get_name(self):

        return self.name

    def get_points(self):

        return self.points

    def get_moves(self):

        return self.number_of_moves


class Human(Player):

    def play(self, sak, catalog):

        self.fill_letters(sak)

        if len(self.round_letters) < 7:
            print("---------------------")
            print("Δεν υπάρχουν αρκετά γράμματα στο σακουλάκι για αντικατάσταση!")
            self.game_end = True
        else:
            print("---------------------")
            print("Στο σακουλάκι: ", len(sak.letters), " γράμματα - Παίζει-> ", self.name, ":")

            message = "Διαθέσιμα γράμματα: "
            for i in range(6):
                message += ''.join(self.round_letters[i])
                message += ","
                message += str(sak.points[self.round_letters[i]])
                message += " - "
            message += ''.join(self.round_letters[6])
            message += ","
            message += str(sak.points[self.round_letters[6]])

            print(message)

            word = input("Λέξη (πατήστε p για αλλαγή γραμμάτων - πατήστε q αν δεν βρίσκετε άλλη λέξη): ").upper()
            while (not self.check_letters(word) or not catalog.check_word(word)) and word != "P" and word != "Q":
                word = input("Μη αποδεκτή λέξη - Παρακαλώ δοκιμάστε άλλη: ").upper()

            if word == "P":
                self.discard_letters(sak)
                print("---------------------")
                message = "Διαθέσιμα γράμματα: "
                for i in range(6):
                    message += ''.join(self.round_letters[i])
                    message += ","
                    message += str(sak.points[self.round_letters[i]])
                    message += " - "
                message += ''.join(self.round_letters[6])
                message += ","
                message += str(sak.points[self.round_letters[6]])
                print(message)
            elif word == "Q":
                self.game_end = True
            else:
                self.points += catalog.get_points(word)
                print("Αποδεκτή λέξη - Βαθμοί :", catalog.get_points(word), " - Σκορ: ", self.points)
                self.remove_used_letters(word)

        self.number_of_moves += 1
        print("---------------------")
        input("Enter για συνέχεια")


class Computer(Player):

    def play(self, sak, catalog, scenario):

        self.fill_letters(sak)

        if len(self.round_letters) < 7:
            print("---------------------")
            print("Δεν υπάρχουν αρκετά γράμματα στο σακουλάκι για αντικατάσταση!")
            self.game_end = True
        else:
            print("---------------------")
            print("Στο σακουλάκι: ", len(sak.letters), " γράμματα - Παίζει-> ", self.name, ":")

            message = "Διαθέσιμα γράμματα: "
            for i in range(6):
                message += ''.join(self.round_letters[i])
                message += ","
                message += str(sak.points[self.round_letters[i]])
                message += " - "
            message += ''.join(self.round_letters[6])
            message += ","
            message += str(sak.points[self.round_letters[6]])

            word = None
            if scenario == 1:
                word_found = False
                i = 2
                while i <= len(self.round_letters) and not word_found:
                    word_list = permutations(self.round_letters, i)
                    for line in word_list:
                        possible_word = ''.join(line)
                        if catalog.check_word(possible_word):
                            word_found = True
                            word = possible_word
                            break
                    i += 1

                if not word:
                    if sak.check_empty():
                        self.game_end = True
                        print("Αδύνατη η εύρεση νέας λέξης!")
                    else:
                        self.discard_letters(sak)
                        print("---------------------")
                        message = "Διαθέσιμα γράμματα: "
                        for i in range(6):
                            message += ''.join(self.round_letters[i])
                            message += ","
                            message += str(sak.points[self.round_letters[i]])
                            message += " - "
                        message += ''.join(self.round_letters[6])
                        message += ","
                        message += str(sak.points[self.round_letters[6]])
                        print(message)
                else:
                    self.points += catalog.get_points(word)
                    print("Λέξη ", self.name, ": ", word, ", Βαθμοί: ", catalog.get_points(word), " - Σκορ: ",
                          self.points)
                    self.remove_used_letters(word)
            elif scenario == 2:
                word_found = False
                i = len(self.round_letters)
                while i >= 2 and not word_found:
                    word_list = permutations(self.round_letters, i)
                    for line in word_list:
                        possible_word = ''.join(line)
                        if catalog.check_word(possible_word):
                            word_found = True
                            word = possible_word
                            break
                    i -= 1

                if not word:
                    if sak.check_empty():
                        self.game_end = True
                        print("Αδύνατη η εύρεση νέας λέξης!")
                    else:
                        self.discard_letters(sak)
                        print("---------------------")
                        message = "Διαθέσιμα γράμματα: "
                        for i in range(6):
                            message += ''.join(self.round_letters[i])
                            message += ","
                            message += str(sak.points[self.round_letters[i]])
                            message += " - "
                        message += ''.join(self.round_letters[6])
                        message += ","
                        message += str(sak.points[self.round_letters[6]])
                        print(message)
                else:
                    self.points += catalog.get_points(word)
                    print("Λέξη ", self.name, ": ", word, ", Βαθμοί: ", catalog.get_points(word), " - Σκορ: ",
                          self.points)
                    self.remove_used_letters(word)
            else:
                max_value = 0
                for i in range(2, len(self.round_letters) + 1):
                    word_list = permutations(self.round_letters, i)
                    for line in word_list:
                        possible_word = ''.join(line)
                        possible_value = catalog.word_points(possible_word, sak)
                        if catalog.check_word(possible_word) and possible_value > max_value:
                            word = possible_word
                            max_value = possible_value

                if not word:
                    if sak.check_empty():
                        self.game_end = True
                        print("Αδύνατη η εύρεση νέας λέξης!")
                    else:
                        self.discard_letters(sak)
                        print("---------------------")
                        message = "Διαθέσιμα γράμματα: "
                        for i in range(6):
                            message += ''.join(self.round_letters[i])
                            message += ","
                            message += str(sak.points[self.round_letters[i]])
                            message += " - "
                        message += ''.join(self.round_letters[6])
                        message += ","
                        message += str(sak.points[self.round_letters[6]])
                        print(message)
                else:
                    self.points += catalog.get_points(word)
                    print("Λέξη ", self.name, ": ", word, ", Βαθμοί: ", catalog.get_points(word), " - Σκορ: ",
                          self.points)
                    self.remove_used_letters(word)

        self.number_of_moves += 1
        input("Enter για συνέχεια")


class Game:

    def __init__(self):

        self.scenario = 3
        self.sak = SakClass()
        self.catalog = Catalog(self.sak)
        self.statistics = Statistics()

    def round_init(self, name):

        self.sak = SakClass()
        self.human = Human(name)
        self.computer = Computer('Computer')

    def settings(self):

        print("---------------------")
        print("Επιλογή σεναρίου Computer")
        print("1: Min")
        print("2: Max")
        print("3: Smart")
        print("---------------------")

        choice = input("Επιλογή: ")
        if choice != '1' and choice != '2' and choice != '3':
            while choice != '1' and choice != '2' and choice != '3':
                choice = input("Μη αναγνωρίσιμη επιλογή - Παρακαλώ επιλέξτε ξανά: ")

        if choice == '1':
            self.scenario = 1
            print("---------------------")
            print("Το σενάριο άλλαξε σε Min")
        elif choice == '2':
            self.scenario = 2
            print("---------------------")
            print("Το σενάριο άλλαξε σε Max")
        elif choice == '3':
            self.scenario = 3
            print("---------------------")
            print("Το σενάριο άλλαξε σε Smart")

    def run(self):

        computer_end_check = self.computer.game_end
        while True:
            self.human.play(self.sak, self.catalog)
            human_end_check = self.human.game_end

            if human_end_check or computer_end_check:
               break

            self.computer.play(self.sak, self.catalog, self.scenario)
            computer_end_check = self.computer.game_end

            if human_end_check or computer_end_check:
                break

        print("---------------------")
        print("Τελική βαθμολογία: ", self.human.get_name(), " - ", self.human.get_points(), "πόντοι, ", self.computer.get_name(), " - ", self.computer.get_points(), "πόντοι")

        if self.human.get_points() > self.computer.get_points():
            print("Νικητής: ", self.human.get_name())
        elif self.human.get_points() == self.computer.get_points():
            print("Ισοπαλία!")
        else:
            print("Νικητής: ", self.computer.get_name())

        self.statistics.write_file(self.human, self.computer)

    def end(self):

        print("Τέλος παιχνιδιού!")
        input("Enter για συνέχεια")

    def game_stats(self):

        print("---------------------")
        print("Στατιστικά")

        try:
            stats = self.statistics.read_file()
            i = 1
            for game_record in stats:
                if int(game_record[1]) > int(game_record[4]):
                    winner = game_record[0]
                elif int(game_record[1]) < int(game_record[4]):
                    winner = game_record[3]
                else:
                    winner = 'Ισοπαλία'
                print("Παιχνίδι ", i, ": Νικητής-> ", winner)
                print("Αναλυτικά: ", game_record[0], " - ", game_record[1], "πόντοι - ", game_record[2], "κινήσεις, ",
                      game_record[3], " - ", game_record[4], "πόντοι - ", game_record[5], "κινήσεις")
                i += 1

            print("---------------------")
            print("q: Επιστροφή στο αρχικό μενού")
            print("clear: Εκκαθάριση των στατιστικών")

            choice = input("Επιλογή: ")
            if choice != 'q' and choice != 'clear':
                while choice != 'q' and choice != 'clear':
                    choice = input("Μη αναγνωρίσιμη επιλογή - Παρακαλώ επιλέξτε ξανά: ")

            if choice == 'clear':
                os.remove("statistics.txt")
                input("Έγινε εκκαθάριση των στατιστικών. Enter για συνέχεια")
        except:
            print("Δεν υπάρχουν διαθέσιμα στατιστικά!")
            input("Enter για συνέχεια")


class Catalog:

    def __init__(self, sak):
        self.catalog = {}
        self.create_catalog(sak)

    def create_catalog(self, sak):

        textfile = open('greek7.txt', encoding='utf-8-sig', mode='r')

        for line in textfile:
            word = line.rstrip("\n")
            self.catalog[word] = self.word_points(word, sak)

        textfile.close()

    def word_points(self, word, sak):

        value = 0

        for i in range(0,len(word)):
            value += sak.points[word[i]]

        return value

    def check_word(self, possible_word):

        if possible_word in self.catalog:
            return True
        else:
            return False

    def get_points(self, word):

        return self.catalog.get(word)


class Statistics:

    def read_file(self):

        f = open("statistics.txt", "r")

        content = f.readlines()
        content = [x.strip() for x in content]
        stats = [None] * len(content)
        i = 0
        for line in content:
            stats[i] = line.split(',')
            i += 1

        f.close()
        return stats

    def write_file(self, human, computer):

        with open("statistics.txt", "a+") as f:
            f.seek(0)
            data = f.read(100)
            if len(data) > 0:
                f.write("\n")

            list = ''.join(human.get_name())
            list += ","
            list += str(human.get_points())
            list += ","
            list += str(human.get_moves())
            list += ","
            list += ''.join(computer.get_name())
            list += ","
            list += str(computer.get_points())
            list += ","
            list += str(computer.get_moves())
            f.write(list)