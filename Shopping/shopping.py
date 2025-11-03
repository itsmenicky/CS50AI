import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)

        # Criando map da coluna month
        month_map = {
            "Jan": 0,
            "Feb": 1,
            "Mar": 2,
            "Apr": 3,
            "May": 4,
            "June": 5,
            "Jul": 6,
            "Aug": 7,
            "Sep": 8,
            "Oct": 9,
            "Nov": 10,
            "Dec": 11,
        }

        # Criando listas de evidencias e labels
        evidences = []
        labels = []

        # Criando tupla que conterá os dados
        for row in reader:
            evidence = []

            # Administrative (Int)
            evidence.extend([int(row[0])])
            # Administrative Duration (Float)
            evidence.extend([float(row[1])])
            # Informational (Int)
            evidence.extend([int(row[2])])
            # Informational Duration (Float)
            evidence.extend([float(row[3])])
            # Product Related (Int)
            evidence.extend([int(row[4])])
            # Product Related Duration (Float)
            evidence.extend([float(row[5])])
            # Bounce Rates (Float)
            evidence.extend([float(row[6])])
            # Exit Rates (Float)
            evidence.extend([float(row[7])])
            # Page Values (Float)
            evidence.extend([float(row[8])])
            # Special Day
            evidence.extend([float(row[9])])
            # Month (Int)
            evidence.append(month_map[row[10]])
            # Operating Systems (Int)
            evidence.extend([int(row[11])])
            # Browser (Int)
            evidence.extend([int(row[12])])
            # Region (Int)
            evidence.extend([int(row[13])])
            # Traffic Type (Int)
            evidence.extend([int(row[14])])
            # Visitor Type (Int)
            evidence.append(1 if row[15] == "Returning_Visitor" else 0)
            # Weekend
            evidence.append(1 if row[16] == "TRUE" else 0)

            # Adicionando evidências e label nas listas
            evidences.append(evidence)
            labels.append(1 if row[17] == "TRUE" else 0)

        return (evidences, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # Declarando os contadores de positivos corretos e seu total
    # bem como os negativos corretos e seu total
    correct_positives = 0
    positives = 0
    correct_negatives = 0
    negatives = 0
    sensitivity = 0
    specificity = 0

    # Percorrendo as predições e labels para iterar os positivos
    # e negativos
    for actual, predicted in zip(labels, predictions):
        if actual == 1:
            positives += 1
            if actual == predicted:
                correct_positives += 1
        else:
            negatives += 1
            if actual == predicted:
                correct_negatives += 1

    # Calculando a sensibilidade e especificidade
    sensitivity = correct_positives / positives
    specificity = correct_negatives / negatives
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
