Here is a detailed **README.md** file for your project:

---

# **Intelligent LLM Agent with Dynamic Tool Selection and Caching**

## **Project Description**
This project implements a smart, LLM-driven multi-agent solution capable of dynamic tool selection and result caching. The system can process customer feedback, analyze sentiment, extract keywords, categorize topics, and summarize feedback using AWS services such as **DynamoDB**, **Lambda**, and **CloudWatch**. It is designed to handle both single and batch processing of feedback entries.

---

## **Features**
1. **Sentiment Analysis**: Determines the overall sentiment of feedback using a pre-trained model.
2. **Topic Categorization**: Categorizes feedback into predefined topics such as Product Quality, Delivery, and Customer Support.
3. **Keyword Extraction**: Extracts important keywords from feedback using NLP models.
4. **Summarization**: Summarizes feedback into actionable insights.
5. **Caching**: Results are cached in DynamoDB to avoid redundant processing.
6. **Dynamic Tool Selection**: Based on instructions provided, the system dynamically decides which tools to run.
7. **Batch Processing**: The system supports processing up to 50 feedback entries per request.

---

## **Technologies Used**
- **Python** (v3.9)
- **AWS DynamoDB** (for caching results)
- **AWS CloudWatch** (for logging and monitoring)
- **Hugging Face Transformers** (for NLP models)
- **Boto3** (AWS SDK for Python)

---

## **Project Structure**

```
intelligent-agent-assignment/
├── README.md              # Project documentation
├── main.py                # Main entry point for the application
├── requirements.txt       # Python dependencies
├── tools/                 # Tool modules for processing feedback
│   ├── sentiment_analysis.py
│   ├── topic_categorization.py
│   ├── keyword_extraction.py
│   └── summarization.py
└── config/                # Configuration settings
    └── aws_credentials.py
```

---

## **Setup Instructions**

### **Step 1: Clone the Repository**
```sh
git clone <repository-url>
cd intelligent-agent-assignment
```

### **Step 2: Create a Virtual Environment**
```sh
python3 -m venv python39-env
source python39-env/bin/activate
```

### **Step 3: Install Dependencies**
```sh
pip install -r requirements.txt
```

### **Step 4: Configure AWS Credentials**
Set your AWS credentials by one of the following methods:
1. **Using AWS CLI**:
   ```sh
   aws configure
   ```
2. **Environment Variables**:
   ```sh
   export AWS_ACCESS_KEY_ID="your-access-key-id"
   export AWS_SECRET_ACCESS_KEY="your-secret-access-key"
   export AWS_DEFAULT_REGION="your-region"
   ```

---

## **Usage**

### **Running the Application Locally**
```sh
python main.py
```

The application accepts a JSON input file with feedback entries. Example:

```json
[
    {
        "feedback_id": "001",
        "customer_name": "Alice",
        "feedback_text": "The product quality is excellent, but customer support was unresponsive.",
        "instructions": "Focus on sentiment analysis and keyword extraction."
    },
    {
        "feedback_id": "002",
        "customer_name": "Bob",
        "feedback_text": "Delivery was fast, but the packaging was damaged.",
        "instructions": "Generate actionable insights."
    }
]
```

The output will include sentiment scores, topics, keywords, and summaries.

---

### **AWS Deployment**
1. **Create an S3 bucket and upload the Lambda deployment package.**
2. **Create a Lambda function and attach the necessary IAM role.**
3. **Deploy the function using the uploaded package.**
4. **Enable API Gateway to expose the Lambda function as an endpoint.**
5. **Monitor logs using AWS CloudWatch.**

---

## **Environment Variables**

- `AWS_ACCESS_KEY_ID`: Your AWS access key.
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key.
- `OPENAI_API_KEY`: Your OpenAI API key for dynamic tool selection.

---

## **Sample Input and Output**

### **Input**
```json
{
    "feedback_id": "003",
    "customer_name": "Charlie",
    "feedback_text": "The item arrived with broken packaging.",
    "instructions": "Perform all analyses."
}
```

### **Output**
```json
{
    "sentiment_scores": {
        "positive": 0.0,
        "negative": 0.6,
        "neutral": 0.4
    },
    "topics": ["Delivery"],
    "keywords": {
        "keywords": [
            {"keyword": "packaging", "category": "Delivery"},
            {"keyword": "broken", "category": "Product Quality"}
        ]
    },
    "summary": "The item arrived with broken packaging."
}
```

---

## **Challenges and Lessons Learned**

### **Challenges**
- Handling large dependencies like NLP models in AWS Lambda due to the 50 MB limit.
- Configuring AWS services and resolving permission-related issues.
- Fine-tuning models to handle both positive and negative sentiments in the same feedback.

### **Lessons Learned**
- Implementing a caching mechanism significantly improves performance for repetitive tasks.
- Leveraging pre-trained models accelerates development but requires customization for domain-specific tasks.
- Effective logging and monitoring are critical for debugging and maintaining cloud-based applications.
