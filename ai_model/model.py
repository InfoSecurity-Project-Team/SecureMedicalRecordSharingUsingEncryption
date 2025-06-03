import pandas as pd
import pickle
import os
pd.set_option('future.no_silent_downcasting', True) # Ignores downcasting warning from replace()

def preprocess(dataframe : pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess the data which is to be passed to the model for prediction of target

    :param dataframe: The data of the patient (symptoms, age, gender)
    :return: DataFrame (padnas)
    """
    boolean_columns = ['Fever', 'Cough', 'Fatigue', 'Difficulty Breathing']
    categorical_columns = ['Blood Pressure', 'Cholesterol Level']
    for col in boolean_columns:
        dataframe[col] = dataframe[col].replace({'Yes': True, 'No': False})
    for col in categorical_columns:
        dataframe[col] = dataframe[col].replace({'Low': 0, 'Normal': 1, 'High': 2})
    dataframe['Gender'] = dataframe['Gender'].replace({'Male': 1, 'Female': 0})
    return dataframe

def diagnose(data: dict) -> str:
    """
    Predicts the disease from given symptoms and other details.
    :param data: A dict containing all the patient details
    :return: str: Disease name
    """
    dataframe = pd.DataFrame(data=data)
    model_path = os.path.join(os.path.dirname(__file__), 'disease_diagnosis_model.pkl')
    with open(model_path, 'rb') as f:

        model = pickle.load(f)
    df_processed = preprocess(dataframe)
    prediction = model.predict(df_processed)
    return prediction[0]


def main():
    d =  {
        'Fever': ['Yes'],
        'Cough': ['No'],
        'Fatigue': ['No'],
        'Difficulty Breathing': ['Yes'],
        'Age': [20],
        'Gender': ['Male'],
        'Blood Pressure': ['Normal'],
        'Cholesterol Level': ['High']
    }
    print(diagnose(d))

if __name__ == '__main__':
    main()