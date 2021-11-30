import fasttext
from os import path


def create_model():
    """
    Creates and formats the training set and the validation. 
    Creates and trains model from training and validation set.
    """
    if not path.exists("./src/classification.train"):
        print("Training set not found. Creating training set.")
        try:
            create_set(
                "./src/classification.train", head("./srs/dataset.txt", 3500)
            )
        except Exception as e:
            print(
                "Error creating training set. Emergency exit triggered. Exception: "
                + str(e)
            )
            exit()
    if not path.exists("./src/classification.valid"):
        print("Validation set not found. Creating validation set")
        try:
            create_set(
                "./src/classification.valid", tail("./src/dataset.txt", 1500)
            )
        except Exception as e:
            print(
                "Error creating validation set. Emergency exit triggered. Exception: "
                + str(e)
            )
            exit()

    model = fasttext.train_supervised(
        input="./src/classification.train", lr=1.0, epoch=25, wordNgrams=2, loss="ova"
    )
    model.save_model("./src/model_classification.bin")
    return model


def debug_model(content, count):
    """
    Sample tests to check whether model works. Model does indeed work. 
    NOTE: THIS FUNCTION RE-TRAINS THE MODEL, USE predict() INSTEAD
    """
    model = create_model()
    return model.predict(content, k=count), model.test("./src/classification.valid")


def predict(content, thresholdVal=-1, predictionCount=1):
    """
    Loads and predicts with the train model in model_classification.bin
    """
    model = fasttext.load_model("./src/model_classification.bin")
    print("Model Loaded!")
    if thresholdVal < 0:
        return model.predict(content, k=predictionCount)
    else:
        return model.predict(content, k=predictionCount, threshold=thresholdVal)


def head(file, N):
    with open(file) as f:
        head = [next(f) for x in range(N)]
    return head


def tail(file, N):
    assert N >= 0
    pos = N + 1
    lines = []

    with open(file) as f:
        while len(lines) <= N:
            try:
                f.seek(-pos, 2)
            except IOError:
                f.seek(0)
                break
            finally:
                lines = list(f)
                pos *= 2

    return lines[-N:]


def create_set(file, data):
    open(file, "w+").close()  # clear data
    with open(file, "w+") as f:
        for x in data:
            f.write(x)
