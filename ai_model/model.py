import pandas as pd

def preprocess(dataframe : pd.DataFrame) -> pd.DataFrame:
    boolean_columns = ['Fever', 'Cough', 'Fatigue', 'Difficulty Breathing']
    categorical_columns = ['Blood Pressure', 'Cholesterol Level']
    for col in boolean_columns:
        dataframe[col] = dataframe[col].replace({'Yes': True, 'No': False})
    for col in categorical_columns:
        dataframe[col] = dataframe[col].replace({'Low': 0, 'Normal': 1, 'High': 2})
    dataframe['Gender'] = dataframe['Gender'].replace({'Male': 1, 'Female': 0})
    return dataframe

def diagnose(data: dict):
    pass


def main():
    pass

if __name__ == '__main__':
    main()