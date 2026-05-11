# News Pulse

News Pulse is a live, local Big Data streaming pipeline and dashboard built with Python, PySpark Structured Streaming, and Streamlit. It continuously ingests RSS news feeds, processes the data in real-time using Spark memory sinks, and displays live metrics such as source distribution, news volume over time, and trending keywords. Additionally, it integrates with a large language model API to generate concise, automated summaries of the top trending topics.

## Pipeline Scalability Analysis

**Question: Which step of your pipeline would break first if the input grew 1000×, and which Spark feature would you reach for to fix it?**

If the input grew 1000×, the **Spark memory sinks** (specifically the `top_words` and `by_source` aggregations) would break first, causing an Out of Memory (OOM) crash on the driver. Because they use `outputMode("complete")` without watermarks, Spark must indefinitely retain all historical aggregation state in memory and continually rewrite the growing table to the driver's local RAM. To fix this, I would reach for **Event-Time Watermarks** to allow Spark to safely discard old state, switch to `outputMode("update")` or `"append"`, and direct the output to a distributed, persistent sink like **Kafka or Delta Lake** instead of the driver's memory.
# Screenshots(couldn't record the demo)
<img width="1910" height="925" alt="stg1" src="https://github.com/user-attachments/assets/ded03d43-c600-47a7-a3a1-8304beb3c3de" />
<img width="903" height="817" alt="stg4" src="https://github.com/user-attachments/assets/f5af6053-dbc0-490c-b253-085ae7b83a3e" />
<img width="1910" height="925" alt="stg3" src="https://github.com/user-attachments/assets/5a30524d-225b-4c25-8e8d-d677f9cbd28b" />
<img width="1763" height="853" alt="Screenshot_11-5-2026_114426_localhost" src="https://github.com/user-attachments/assets/7119db56-058a-46d8-bb38-9412460bdb3c" />

<img width="1756" height="910" alt="fullScreen" src="https://github.com/user-attachments/assets/bc8710ae-5bb6-42e2-93b9-7707fab0f7ec" />
