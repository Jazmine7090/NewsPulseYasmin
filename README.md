# News Pulse

News Pulse is a live, local Big Data streaming pipeline and dashboard built with Python, PySpark Structured Streaming, and Streamlit. It continuously ingests RSS news feeds, processes the data in real-time using Spark memory sinks, and displays live metrics such as source distribution, news volume over time, and trending keywords. Additionally, it integrates with a large language model API to generate concise, automated summaries of the top trending topics.

## Pipeline Scalability Analysis

**Question: Which step of your pipeline would break first if the input grew 1000×, and which Spark feature would you reach for to fix it?**

If the input grew 1000×, the **Spark memory sinks** (specifically the `top_words` and `by_source` aggregations) would break first, causing an Out of Memory (OOM) crash on the driver. Because they use `outputMode("complete")` without watermarks, Spark must indefinitely retain all historical aggregation state in memory and continually rewrite the growing table to the driver's local RAM. To fix this, I would reach for **Event-Time Watermarks** to allow Spark to safely discard old state, switch to `outputMode("update")` or `"append"`, and direct the output to a distributed, persistent sink like **Kafka or Delta Lake** instead of the driver's memory.
