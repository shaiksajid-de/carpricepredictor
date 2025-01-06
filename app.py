from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load the trained model
model = pickle.load(open("LinearRegressionModel.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Extract features from the form
        name = request.form["name"]  # Include name in the input
        company = request.form["company"]
        year = int(request.form["year"])
        kms_driven = int(request.form["kms_driven"])
        fuel_type = request.form["fuel_type"]

        # Create a DataFrame for prediction
        data = pd.DataFrame([[name, company, year, kms_driven, fuel_type]],
                            columns=["name", "company", "year", "kms_driven", "fuel_type"])

        # Make the prediction
        prediction = model.predict(data)
        output = round(prediction[0], 2)

        return render_template("index.html", prediction_text=f"Estimated Car Price: ${output}")
    except Exception as e:
        return render_template("index.html", prediction_text=f"Error: {e}")

if __name__ == "__main__":
    app.run(debug=True)
