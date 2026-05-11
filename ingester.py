import os
import json
import time
from datetime import datetime
import feedparser

# RSS feeds to poll
FEEDS = {
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",

"Arab News": "https://www.arabnews.com/rss.xml",

"Middle East Eye": "https://www.middleeasteye.net/rss",

"Al Arabiya": "https://english.alarabiya.net/.mrss/en.xml"
}

# Ensure the output directory exists
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "data", "incoming")
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def fetch_feeds():
    batch_num = 0
    print(f"Starting ingester. Writing to: {OUTPUT_DIR}")
    
    while True:
        records = []
        for source, url in FEEDS.items():
            try:
                # Parse the RSS feed
                feed = feedparser.parse(url)
                # Process each entry
                for entry in feed.entries:
                    records.append({
                        "source": source,
                        "title": entry.title,
                        "url": getattr(entry, "link", ""),
                        "ts": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                    })
            except Exception as e:
                # Tolerate dead feeds
                print(f"Error fetching {source}: {e}")
        
        # Write batch if we have data
        if records:
            output_file = os.path.join(OUTPUT_DIR, f"batch_{batch_num}.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                for record in records:
                    # Write one JSON object per line (JSONL format)
                    f.write(json.dumps(record) + '\n')
            
            print(f"Batch {batch_num}: Wrote {len(records)} records to {output_file}")
            batch_num += 1
            
        print("Sleeping for 60 seconds...")
        time.sleep(60)

if __name__ == "__main__":
    fetch_feeds()
