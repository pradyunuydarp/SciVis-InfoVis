import pandas as pd

def clean_tsv(file_path,save_path):
    df = pd.read_csv(file_path, sep="\t")

# Split 'PROPERTIES' column into multiple columns based on the vector order
    properties_cols = [
    "Num_Chars", "Num_Chars_No_Whitespace", "Frac_Alphabetical", "Frac_Digits",
    "Frac_Uppercase", "Frac_Whitespace", "Frac_Special", "Num_Words", "Num_Unique_Words",
    "Num_Long_Words", "Avg_Word_Length", "Num_Unique_Stopwords", "Frac_Stopwords",
    "Num_Sentences", "Num_Long_Sentences", "Avg_Chars_Per_Sentence", "Avg_Words_Per_Sentence",
    "Readability_Index", "VADER_Pos", "VADER_Neg", "VADER_Compound",
    "LIWC_Funct", "LIWC_Pronoun", "LIWC_Ppron", "LIWC_I", "LIWC_We", "LIWC_You",
    "LIWC_SheHe", "LIWC_They", "LIWC_Ipron", "LIWC_Article", "LIWC_Verbs", "LIWC_AuxVb",
    "LIWC_Past", "LIWC_Present", "LIWC_Future", "LIWC_Adverbs", "LIWC_Prep",
    "LIWC_Conj", "LIWC_Negate", "LIWC_Quant", "LIWC_Numbers", "LIWC_Swear",
    "LIWC_Social", "LIWC_Family", "LIWC_Friends", "LIWC_Humans", "LIWC_Affect",
    "LIWC_Posemo", "LIWC_Negemo", "LIWC_Anx", "LIWC_Anger", "LIWC_Sad",
    "LIWC_CogMech", "LIWC_Insight", "LIWC_Cause", "LIWC_Discrep", "LIWC_Tentat",
    "LIWC_Certain", "LIWC_Inhib", "LIWC_Incl", "LIWC_Excl", "LIWC_Percept",
    "LIWC_See", "LIWC_Hear", "LIWC_Feel", "LIWC_Bio", "LIWC_Body", "LIWC_Health",
    "LIWC_Sexual", "LIWC_Ingest", "LIWC_Relativ", "LIWC_Motion", "LIWC_Space",
    "LIWC_Time", "LIWC_Work", "LIWC_Achiev", "LIWC_Leisure", "LIWC_Home",
    "LIWC_Money", "LIWC_Relig", "LIWC_Death", "LIWC_Assent", "LIWC_Dissent",
    "LIWC_Nonflu", "LIWC_Filler"
    ]

    properties_df = df["PROPERTIES"].str.split(",", expand=True)
    properties_df.columns = properties_cols

    df = pd.concat([df.drop(columns=["PROPERTIES"]), properties_df], axis=1)

    df=df.rename(columns={"SOURCE_SUBREDDIT":"Source","TARGET_SUBREDDIT":"Target"})
    df.drop(columns=["POST_ID"],inplace=True)
    
    nodes_df=df.drop(columns=["Target","LINK_SENTIMENT"])
    edges_df=df.drop(columns=properties_cols+["TIMESTAMP"])

    nodes_df=nodes_df.rename(columns={"Source":"Id"})
    nodes_df.to_csv(save_path+"_nodes.csv",index=False)
    edges_df.to_csv(save_path+"_edges.csv",index=False)

def add_impact_score(file_path,save_path):
    df = pd.read_csv(file_path)
    
    df["Positive_Impact_Score"] = (df["VADER_Pos"]+df["LIWC_Posemo"]+df["LIWC_Affect"]+df["LIWC_Social"]+df["LIWC_Friends"]) / df["Num_Words"]
    df["Negative_Impact_Score"] = (df["VADER_Neg"]+df["LIWC_Negemo"]+df["LIWC_Anx"]+df["LIWC_Anger"]+df["LIWC_Sad"]) / df["Num_Words"]
    df["Impact_Score"] = df["Positive_Impact_Score"] - df["Negative_Impact_Score"]
    df["Impact_Score"] = (df["Impact_Score"]-df["Impact_Score"].min())/(df["Impact_Score"].max()-df["Impact_Score"].min())
    df.to_csv(save_path,index=False)
if __name__ == "__main__":
    # clean_tsv("./dataset/soc-redditHyperlinks-body.tsv","./dataset/reddit_body_")
    # clean_tsv("./dataset/soc-redditHyperlinks-title.tsv","./dataset/reddit_title_")
    add_impact_score("./dataset/reddit_body__nodes.csv","./dataset/reddit_body__nodes.csv")
    add_impact_score("./dataset/reddit_title__nodes.csv","./dataset/reddit_title__nodes.csv")
  
   