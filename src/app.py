from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import classification as algorithm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)


class Entry(db.Model):
    """
    id - ID of each entry.
    content - Article content.
    date_created - Date of Entry creation.
    """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Task %r>" % self.id


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        article_content = request.form["article_content"]
        threshold_val = request.form["threshold_input"]
        prediction_count = request.form["prediction_count"]

        if article_content == "":
            return render_template("templates/index.html", error_text="No text entered!")
        if threshold_val == "":
            int_threshold_val = int("0")
        else:
            int_threshold_val = float(threshold_val)
        if prediction_count == "":
            int_prediction_count = int("1")
        else:
            int_prediction_count = int(prediction_count)

        result = algorithm.predict(
            article_content,
            thresholdVal=int_threshold_val,
            predictionCount=int_prediction_count,
        )
        predictions = result[0]
        predictions = list(predictions)
        for prediction in predictions:
            prediction = str(prediction)
            prediction = prediction.replace("label", " ")

        if predictions.count == 0:
            predictions.append("Unable to predict a system with the given settings.")

        return render_template("index.html", predictions=predictions)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
