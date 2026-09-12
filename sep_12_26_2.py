import os 

from dotenv import load_dotenv
from snowflake.snowpark import Session

# load the env 
load_dotenv()

# connection params. 
connection_parameters = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
}

session = Session.builder.configs(connection_parameters).create()
print(session.sql("SELECT CURRENT_USER()").collect())

from transformers import pipeline
from transformers import logging
logging.set_verbosity_error()

sentiment_model = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)
# Get 5 posts from Snowflake
import pandas as pd

# Get all posts from Snowflake
rows = session.sql("""
    SELECT POST_ID, POST_TEXT
    FROM ANALYSIS_SEP_2026.SOCIAL.SOCIAL_POSTS_RAW
    ORDER BY POST_ID
""").collect()

# Run sentiment analysis and build a DataFrame
results = []

for row in rows:
    result = sentiment_model(row.POST_TEXT)[0]

    results.append({
        "POST_ID": row.POST_ID,
        "POST_TEXT": row.POST_TEXT,
        "SENTIMENT": result["label"],
        "SCORE": result["score"]
    })

df = pd.DataFrame(results)

# Write the DataFrame to a new Snowflake table
session.write_pandas(
    df,
    table_name="SOCIAL_POSTS_SENTIMENT",
    database="ANALYSIS_SEP_2026",
    schema="SOCIAL",
    auto_create_table=True,
    overwrite=True
)

print("Data written to Snowflake.")
