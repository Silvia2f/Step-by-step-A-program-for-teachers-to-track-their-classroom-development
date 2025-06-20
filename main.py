import pandas as pd

def load_csv(filepath):
    df = pd.read_csv(filepath)
    print(df.head())  #making sure it all loaded correctly
    return df

if __name__ == "__main__":
    load_csv("data/test_data.csv")