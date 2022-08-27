import numpy as np
import string
import re
from functools import partial
from collections import defaultdict

paragraphs_re = re.compile('(.*?)(\n{2,}|$)', re.DOTALL)

def rec_dd(depth=0):
    if depth == 2:
        return 0
    return defaultdict(partial(rec_dd, depth + 1))


class MarkovModel:
    def __init__(self):                 # create empty default dictionaries
        self.initial = {}               # start of a phrase (first word)
        self.first_order = rec_dd()
        self.second_order = rec_dd()


    @staticmethod
    def remove_punctuation(s):
        return s.translate(str.maketrans('','',string.punctuation))

    def train(self, training_data):
        unwanted_chars = set({})
        for char in training_data:
            if char.lower() not in "abcdefghijklmnopqrstuvwxyzßäöü\n ":
                unwanted_chars.add(char)

        for c in unwanted_chars:
            training_data = training_data.replace(c, "")
        
        paragraphs = paragraphs_re.findall(training_data)

        for match in paragraphs: # input_file["quotes"]:  # traverse poems, populate dictionary
            paragraph = match[0].strip()
            if len(paragraph) == 0:
                continue
            for row in paragraph.split('\n'):
                tokens = self.remove_punctuation(row.rstrip().lower()).split()  # turns every line into list of words

                T = len(tokens)
                for i in range(T):
                    t = tokens[i]
                    if i == 0:
                        self.initial[t] = self.initial.get(t, 0.) + 1     # if t does not exist in dict, it gets created (assigned value 0, immediately added 1)
                    else:
                        t_1 = tokens[i - 1]

                        if i == T - 1:  # checking if end of sentence (starts counting at 0, thus T-1)
                            if 'END' not in self.second_order[(t_1, t)]:
                                self.second_order[(t_1, t)]['END'] = 0
                            self.second_order[(t_1, t)]['END'] += 1

                        if i == 1:  # when given only the first word
                            self.first_order[t_1][t] += 1

                        else:
                            t_2 = tokens[i - 2]

                            if t not in self.second_order[(t_1, t)]:
                                self.second_order[(t_2, t_1)][t] = 0
                            self.second_order[(t_2, t_1)][t] += 1

        # normalize the distributions (turning counts into percentage of total)
        initial_total = sum(self.initial.values())
        for t, c in self.initial.items():
            self.initial[t] = c / initial_total  # maximum likelihood estimate

        for t, c in self.first_order.items():  # new in ver2
            first_order_subtotal = sum(c.values())
            for sub_t, sub_c, in c.items():
                self.first_order[t][sub_t] = sub_c / first_order_subtotal

        for t, c in self.second_order.items():  # new in ver2
            second_order_subtotal = sum(c.values())
            for sub_t, sub_c, in c.items():
                self.second_order[t][sub_t] = sub_c / second_order_subtotal

    @staticmethod
    def sample_word(d): # sample a word given a dict of probabilities
        p0 = np.random.random()  # randomly chooses number (just once) between 0 and 1
        cumulative = 0
        for t, p in d.items():     # token and corresponding probability
            cumulative += p    # adds probability of each token
            if cumulative > p0:    # originally if p0 < cumulative
                return t
        assert False  # should never get here

    def generate(self):
        res = ""
        for i in range(4):  # generate 4 lines at a time
            if i != 0:
                res += "\n"
            sentence = []

            # sample initital word
            w0 = self.sample_word(self.initial)
            sentence.append(w0)

            # sample second word
            w1 = self.sample_word(self.first_order[w0])
            sentence.append(w1)

        # second-order transitions until END
            while True:
                w2 = self.sample_word(self.second_order[(w0, w1)])
                if w2 == 'END':
                    break  # goes to next line
                sentence.append(w2)
                w0 = w1
                w1 = w2
            res += " ".join(sentence)
        return res

def generate(training_data):
    test_poem = MarkovModel()
    test_poem.train(training_data)
    return test_poem.generate()
