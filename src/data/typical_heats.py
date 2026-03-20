import pandas as pd

def get_typical_heats (datasets_dict: dict, n: int = 3, seed: int = 42) -> list:
    
    counts = {
        name: df.groupby("HEATID").size().rename(name)
        for name, df in datasets_dict.items()
    }

    combined = pd.concat(counts.values(), axis=1).dropna()

    for col in combined.columns:
        median = combined[col].median()
        mad =  (combined[col] - median).abs().median()
        combined = combined[combined[col].between(median - mad, median + mad)]
        
    return combined.sample(n=n, random_state=seed).index.tolist()
