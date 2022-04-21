# CHECK FOR UpperCase as well
# or BETTER bring the whole sentence to lowercase and then check

import pickle
import sys
import math

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


def create_table(file_path):
    table = []

    with open(file_path) as f:
        file = f.readlines()

        for line in file:
            # modify the below line till range(0, 5)
            tempList = ["False" for i in range(0, 6)]

            # remove the 3 lines below when testing
            temp = line.split("|")
            if temp[0] == "en":
                tempList[5] = "True"

            words = temp[1].split(" ")
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


class CreateQuestionNode:
    def __init__(self, feature, booleanVar):
        self.feature = feature
        if booleanVar == "True":
            self.trueOrFalse = "True"
        elif booleanVar == "False":
            self.trueOrFalse = "False"




def differentOccurencesMappedToFrequency(data):
    differentOccurences = {}
    i = 0

    trueIndexFound = False
    firstTimeTrue = False

    falseIndexFound = False
    firstTimeFalse = False

    yetDiscovered = set()

    while i < len(data):
        if len(data[i]) != 0:
            temp = data[i]
            # print()
            # print(data)
            # print(temp)
            # print()
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


def calculateEntropy(rows):
    counts = differentOccurencesMappedToFrequency(rows)

    # print(counts)

    if "True" in counts.keys():
        trueCount = counts["True"]
    else:
        trueCount = 0

    if "False" in counts.keys():
        falseCount = counts["False"]
    else:
        falseCount = 0

    if trueCount == 0 and falseCount == 0:
        return 0

    p = float( trueCount / ( trueCount + falseCount ) )

    if p == 0 or p == 1:
        return 0

    return - p * math.log2(p) - (1 - p) * math.log2(1 - p)




def calculateInfoGain(left, right, current_uncertainty):
    l = len(left)
    r = len(right)
    p = float(l / (l + r))
    return current_uncertainty - p * math.log2(p) - (1 - p) * math.log2(1 - p)


def checkConditionIfEmptyLists(satisfy_question, not_satisfy_questions):
    ret = False
    if len(satisfy_question) == 0:
        ret = True
    if len(not_satisfy_questions) == 0:
        ret = True

    return ret


def initialzieFeatures(data):
    gain = 0
    question = None
    datasetEntropy = calculateEntropy(data)

    return gain, question, datasetEntropy


def checkMaxGain(gain, best_gain, best_question, question):
    if gain == max(gain, best_gain):
        return gain, question
    else:
        return best_gain, best_question



def splitTheDataOnBestChoice(data):
    bestGain,bestQuestion,datasetEntropy = initialzieFeatures(data)

    for i in range(len(data[0]) - 1):

        for j in ["True","False"]:

            question = CreateQuestionNode(i, j)

            satisfy = []
            not_satisfy = []

            i2 = 0
            while i2 < len(data):
                temp = data[i2]
                test = temp[question.feature]
                var = True if (test == question.trueOrFalse) else False
                if var:
                    satisfy.append(temp)
                else:
                    not_satisfy.append(temp)
                i2 += 1

            satisfy_question = satisfy
            not_satisfy_questions = not_satisfy

            if not checkConditionIfEmptyLists(satisfy_question, not_satisfy_questions):
                gain = calculateInfoGain(satisfy_question, not_satisfy_questions, datasetEntropy)
                bestGain, bestQuestion = checkMaxGain(gain, bestGain, bestQuestion, question)


    return bestGain, bestQuestion


class Leaf:
    def __init__(self, rows):
        self.predictions = differentOccurencesMappedToFrequency(rows)


class Decision_Node:
    def __init__(self, question, left, right):
        self.question = question
        self.satisfy = left
        self.notSatisfy = right


def decisionTreeGenerate(table, minSize, maxDepth, depth):

    completeTableGain, question = splitTheDataOnBestChoice(table)

    if completeTableGain == 0:
        node = Leaf(table)
        return node

    satisfy = []
    not_satisfy = []

    i2 = 0
    while i2 < len(table):
        temp = table[i2]
        test = temp[question.feature]
        var = True if (test == question.trueOrFalse) else False
        if var:
            satisfy.append(temp)
        else:
            not_satisfy.append(temp)
        i2 += 1

    satisfyQuestion = satisfy
    notSatisfyQuestion = not_satisfy


    # one = 0
    # for i in satisfyQuestion:
    #
    #     if len(i) > question.feature:
    #         satisfy[one].pop(question.feature)
    #
    #     one += 1
    #
    # satisfyQuestion = satisfy
    #
    #
    # one = 0
    # for i in notSatisfyQuestion:
    #
    #     if len(i) > question.feature:
    #         not_satisfy[one].pop(question.feature)
    #
    #     one += 1
    #
    # notSatisfyQuestion = not_satisfy

    if not satisfyQuestion or not notSatisfyQuestion:
        return Leaf(table)

    if depth >= maxDepth:
        return Decision_Node(question, Leaf(satisfyQuestion), Leaf(notSatisfyQuestion))


    if len(satisfyQuestion) <= minSize:
        leftTreeSatisfyQuestion = Leaf(satisfyQuestion)
    else:
        leftTreeSatisfyQuestion = decisionTreeGenerate(satisfyQuestion, minSize, maxDepth, depth + 1)


    if len(notSatisfyQuestion) <= minSize:
        rightTreeNotSatisfyQuestion = Leaf(satisfyQuestion)
    else:
        rightTreeNotSatisfyQuestion = decisionTreeGenerate(notSatisfyQuestion, minSize, maxDepth, depth + 1)


    finalSetNode = Decision_Node(question, leftTreeSatisfyQuestion, rightTreeNotSatisfyQuestion)

    return finalSetNode




def predictWhichOne(table, current):

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
        tempDict = predictWhichOne(table, left)
        return tempDict
    else:
        tempDict = predictWhichOne(table, right)
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
            tempList = ["False" for i in range(0, 6)]

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




def adaboost_function(data, roundsOfBoosting):
    listOfAlphas = []

    listOfWeakClassifier = []

    noOfBoostingRounds = roundsOfBoosting

    listOfTrainingErrors = []

    weights = []

    for i in range(0, len(data)):
        weights.append(1 / len(data))

    # print(weights)

    iteration = 0
    while iteration < noOfBoostingRounds:

        weakClassifier = decisionTreeGenerate(data, 1, 1, 1)

        testDataWithoutLastColumn = data

        dataWithOnlyLastColumn = []

        totalSize = len(data)
        tupleLength = len(data[0])

        breakContinue = False

        for i in range( totalSize ):
            if tupleLength == 0:
                breakContinue = True
                break

            # print()
            # print(i)
            # print(tupleLength - 1)
            # print(testDataWithoutLastColumn)
            # print()
            dataWithOnlyLastColumn.append( testDataWithoutLastColumn[i][tupleLength - 1] )
            testDataWithoutLastColumn[i].pop( tupleLength - 1 )

        if breakContinue:
            iteration += 1
            continue

        prediction = []

        for row in testDataWithoutLastColumn:
            weakClassifierResultDict = predictWhichOne(testDataWithoutLastColumn, weakClassifier)
            weakClassifierPrediction = str(weakClassifierResultDict)
            if "False" in weakClassifierPrediction:
                prediction.append("False")
                # print("nl")
            else:
                prediction.append("True")
                # print("en")

        listOfWeakClassifier.append(weakClassifier)





        # Compute error

        notEqualCounter = 0
        incorrectWeightSum = 0

        for check in range( len( dataWithOnlyLastColumn ) ):
            if dataWithOnlyLastColumn[check] != prediction[check]:
                notEqualCounter += 1
                incorrectWeightSum += weights[check]

        totalSum = 0
        for i in range(0, len(data)):
            totalSum += weights[i]


        error = incorrectWeightSum / totalSum
        listOfTrainingErrors.append(error)




        # Compute alpha

        # print(error)

        if error == 0 or error == 1:
            alphaWeight = 0
        else:
            alphaWeight = math.log( (1 - error) / error )
        listOfAlphas.append(alphaWeight)





        # Update weight

        for check in range(len(dataWithOnlyLastColumn)):
            if dataWithOnlyLastColumn[check] != prediction[check]:
                weights[check] = weights[check] * math.exp(alphaWeight * notEqualCounter)



        iteration += 1

    return listOfAlphas, listOfWeakClassifier, listOfTrainingErrors



def main():

    table = create_table(sys.argv[1])

    if sys.argv[3] == "dt":
        minSize = 1
        maxDepth = 5
        depth = 1
        classifierTree = decisionTreeGenerate(table, minSize, maxDepth, depth)
        with open(sys.argv[2], 'wb') as files:
            pickle.dump(classifierTree, files)
    elif sys.argv[3] == "ada":

        boostRounds = 50

        listOfAlphas, listOfWeakClassifier, listOfTrainingErrors = adaboost_function(table, boostRounds)

        temp = [[] for i in range(3)]
        temp[0] = listOfAlphas
        temp[1] = listOfWeakClassifier
        temp[2] = boostRounds

        # print()
        # print()
        # print(temp)

        with open(sys.argv[2], 'wb') as files:
            pickle.dump(temp, files)




if __name__ == "__main__":
    main()
