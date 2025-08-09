from app import model_pred

new_data = {
    "Gender": 0,
    "AGE": 50,
    "Urea": 4.7,
    "Cr": 46,
    "HbA1c": 4.9,
    "Chol": 4.2,
    "TG": 0.9,
    "HDL": 2.4,
    "LDL": 1.4,
    "VLDL": 0.5,
    "BMI": 24
}


def test_predict():
    prediction = model_pred(new_data)
    assert prediction == 0
    print(prediction)