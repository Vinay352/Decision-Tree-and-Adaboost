import pickle
import sys

english_articles = ["a", "the", "an"]

english_pronouns = ["he", "his", "him", "himself", "she", "her",
                    "herself", "hers", "I", "me", "my", "mine",
                    "myself", "you", "your", "yours", "yourself",
                    "it", "its", "itself", "we", "us", "our", "ours",
                    "ourselves", "they", "them", "their", "theirs",
                    "themselves"]

english_auxillary_verbs = ["am", "is", "are", "was", "were", "being",
                           "been", "be", "has", "have", "had", "did",
                           "shall", "will", "should", "would", "may", "might",
                           "must", "can", "could", "does", "do", "need",
                           "ought to", "dare", "going to", "be able to", "have to", "had better",
                           "going", "have", "ought", "be able"]

# english_prepositions = ["aboard", "about", "above", "across", "after", "against",
#                         "along", "alongside", "amid", "amidst", "among", "amongst",
#                         "anti", "around", "as", "astride", "at", "atop", "according to", "ahead of", "along with", "apart from", "as for", "aside from"]


english_conjunctions = ["and", "but", "for", "nor", "or", "so", "yet"]


english_words_not_in_dutch = ["an", "the", "he", "his", "him", "himself",
                              "she", "her", "herself", "me", "my",
                              "mine", "myself", "you", "your", "yours",
                              "yourself", "it", "its", "itself", "us",
                              "our", "ours", "ourselves", "they", "them",
                              "their", "theirs", "themselves", "and",
                              "but", "for", "nor", "or", "so", "yet",
                              "am", "are", "were", "being",
                              "been", "be", "has", "have", "did",
                              "shall", "will", "should", "would", "may", "might",
                              "must", "can", "could", "does", "need",
                              "ought to", "dare", "going to", "be able to", "have to", "had better",
                              "going", "have", "ought", "be able"]

features_list = ["Does_it_contain_english_articles", "Does_it_contain_english_pronouns",
                     "Does_it_contain_english_auxillary_verbs", "Does_it_contain_english_conjunctions",
                     "Does_it_contain_english_words_not_in_dutch", "Predict_english_or_not"]



class Decision_Node:
    def __init__(self, question, left, right):
        self.question = question
        self.satisfy = left
        self.notSatisfy = right


class CreateQuestionNode:
    def __init__(self, feature, booleanVar):
        self.feature = feature
        if booleanVar == "True":
            self.trueOrFalse = "True"
        elif booleanVar == "False":
            self.trueOrFalse = "False"

    def __repr__(self):
        return features_list[self.feature] + " " + " -> " + str(self.trueOrFalse)



def differentOccurencesMappedToFrequency(data):
    differentOccurences = {}
    i = 0

    trueIndexFound = False
    firstTimeTrue = False

    falseIndexFound = False
    firstTimeFalse = False

    yetDiscovered = set()

    while i < len(data):
        temp = data[i]
        index = temp[-1]

        if index == "True":

            if "True" not in yetDiscovered:
                differentOccurences["True"] = 0
                differentOccurences["True"] += 1

            elif "True" in yetDiscovered:
                differentOccurences["True"] += 1

            yetDiscovered.add("True")

        elif index == "False":

            if "False" not in yetDiscovered:
                differentOccurences["False"] = 0
                differentOccurences["False"] += 1

            elif "False" in yetDiscovered:
                differentOccurences["False"] += 1

            yetDiscovered.add("False")

        i += 1

    return differentOccurences

class Leaf:
    def __init__(self, rows):
        self.predictions = differentOccurencesMappedToFrequency(rows)



def predictDT(table, current):

    if isinstance(current, Leaf):
        dictionary = current.predictions
        temp = dictionary.keys()
        return temp

    ask = current.question

    test = table[ask.feature]
    var = True if (test == ask.trueOrFalse) else False

    left = current.satisfy
    right = current.notSatisfy

    if var:
        tempDict = predictDT(table, left)
        return tempDict
    else:
        tempDict = predictDT(table, right)
        return tempDict


# print()
# print()
# print()
#

#
# print()
# print()


def create_table_for_test(file_path):
    table = []

    with open(file_path) as f:
        file = f.readlines()

        for line in file:
            # modify the below line till range(0, 5)
            tempList = ["False" for i in range(0, 5)]

            words = line.split(" ")

            for i in words:
                for j in english_articles:
                    if i.strip().lower() == j.strip().lower():
                        tempList[0] = "True"

            for i in words:
                for j in english_pronouns:
                    if i.strip().lower() == j.strip().lower():
                        tempList[1] = "True"

            for i in words:
                for j in english_auxillary_verbs:
                    if i.strip().lower() == j.strip().lower():
                        tempList[2] = "True"

            for i in words:
                for j in english_conjunctions:
                    if i.strip().lower() == j.strip().lower():
                        tempList[3] = "True"

            for i in words:
                for j in english_words_not_in_dutch:
                    if i.strip().lower() == j.strip().lower():
                        tempList[4] = "True"

            # if any(ext in temp[1] for ext in english_articles):
            #     tempList[0] = True
            #
            # if any(ext in temp[1] for ext in english_pronouns):
            #     tempList[1] = True
            #
            # if any(ext in temp[1] for ext in english_auxillary_verbs):
            #     tempList[2] = True
            #
            # if any(ext in temp[1] for ext in english_conjunctions):
            #     tempList[3] = True
            #
            # if any(ext in temp[1] for ext in english_words_not_in_dutch):
            #     tempList[4] = True

            table.append(tempList)

        # for i in table:
        #     print(i)

        return table

def main():
    testTable = create_table_for_test(sys.argv[2])

    with open(sys.argv[1], 'rb') as f:
        classifierTreeForTesting = pickle.load(f)

    for row in testTable:
        tempDict = predictDT(row, classifierTreeForTesting)
        temp = str(tempDict)
        if "False" in temp:
            print("nl")
        else:
            print("en")


if __name__ == "__main__":
    main()