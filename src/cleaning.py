import pandas as pd
from pathlib import Path

def strip_col_names(df: pd.DataFrame):
    df = df.copy()
    df.columns = df.columns.str.strip()
    return df

def drop_cols(df: pd.DataFrame):
    cols = ["Account username", "Account name", "Data comment", 'Date']
    return df.drop(columns=cols, errors="ignore")
        
def rename_cols(df: pd.DataFrame):
    df = df.copy()
    rename = {
        "Name" : "Post",
        "Publish time" : "Published",
        "Post type" : "Format"
    }
    return df.rename(columns=rename, errors="ignore")

def modify_cats(df: pd.DataFrame):
    df = df.copy()
    if "Category" in df.columns:
        df["Category"] = pd.Categorical(
            df["Category"]
        )
    if "Format" in df.columns:
        df["Format"] = pd.Categorical(
            df["Format"].replace({
                "IG image" : "Image",
                "IG carousel" : 'Carousel',
                "IG reel" : "Reel"
        }),
        categories = ["Image", "Carousel", "Reel"]  
        )
    return df
    
def sort_published(df: pd.DataFrame):
    if "Published" not in df:
        return df
    
    return(
        df
        .assign(
            Published= lambda d: pd.to_datetime(
                d["Published"],
                format =  "%m/%d/%y %H:%M",
                errors = "coerce"
            )
        )
        .sort_values("Published")
        .reset_index(drop = True)
    )

def sep_time(df: pd.DataFrame):
    if "Published" not in df:
        return df
    
    return(
        df
        .assign(
            **{
                "Date" : lambda d: d["Published"].dt.date,
                "Time" : lambda d: d["Published"].dt.time
            }
        )
        .drop(columns = ["Published"])
    )
    
def sort_inter(df: pd.DataFrame):
    if "Interactions" not in df:
        return df
    return df.sort_values("Interactions", ascending = False).reset_index(drop=True)
