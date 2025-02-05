import json
import logging
import hashlib
import boto3
from datetime import datetime
from tools import sentiment_analysis, topic_categorization, keyword_extraction, summarization

import datetime
import logging

# 


# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Helper function to generate cache key
def generate_cache_key(event):
    key_string = f"{event['feedback_text']}|{event.get('instructions', '')}"
    return hashlib.sha256(key_string.encode()).hexdigest()


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Initialize DynamoDB
dynamodb = boto3.client('dynamodb', region_name='us-west-1')

def cache_result(cache_key, feedback_id, result, customer_name):
    current_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        # Log the item before saving
        logger.info(f"Saving to DynamoDB: feedback_id={feedback_id}, result={result}")

        response = dynamodb.put_item(
            TableName="FeedbackCache",
            Item={
                'cache_key': {'S': cache_key},
                'feedback_id': {'S': feedback_id},
                'cached_result': {'S': json.dumps(result)},
                'customer_name': {'S': customer_name},
                'last_updated': {'S': current_time}
            }
        )

        # Log the response to confirm the item is saved
        logger.info(f"DynamoDB put_item response: {response}")

    except Exception as e:
        logger.error(f"Error while caching result: {e}")


# Process a single feedback entry
def process_feedback(entry):
    try:
        cache_key = generate_cache_key(entry)
        instructions = entry.get('instructions', '')

        # Process tools based on instructions
        result = {}
        result['sentiment_scores'] = sentiment_analysis.analyze(entry['feedback_text'])
        result['topics'] = topic_categorization.categorize(entry['feedback_text'])
        result['keywords'] = keyword_extraction.extract(entry['feedback_text'])
        result['summary'] = summarization.summarize(entry['feedback_text'])

        # Save result to DynamoDB
        cache_result(cache_key, entry['feedback_id'], result, entry['customer_name'])
        return result

    except Exception as e:
        logger.error(f"Error processing feedback entry: {e}")
        return {"error": str(e)}

# Main function for local testing
if __name__ == "__main__":
    test_event = {
        "feedback_id": "002",
        "customer_name": "Vinod",
        "feedback_text": "The delivery was prompt and the product quality was great.",
        "instructions": "Focus on sentiment analysis and keyword extraction."
    }

    result = process_feedback(test_event)
    print("Processing Result:", json.dumps(result, indent=2))
