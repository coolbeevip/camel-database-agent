import textwrap


class PromptTemplates:
    QUESTION_INFERENCE_PIPELINE = textwrap.dedent("""
    # JSON Format Request
    
    You are a specialized JSON generator. Your only function is to parse the provided data and convert it to JSON format, strictly following the format requirements.    

    ## Database Schema:
    ```
    {{ddl_sql}}
    ```

    ## Data Example:
    ```sql
    {{data_sql}}
    ```

    ## Instructions:
    Database System: {{dialect_name}}
    1. Please carefully analyze the following database information and conduct an in-depth analysis from a business perspective. What business query questions might users raise? Please fully consider some complex query scenarios, including but not limited to multi-table associations, grouping statistics, etc.
    2. Please ensure that the SQL you write conforms to {{dialect_name}} syntax.
    3. Generate {{query_samples_size}} real user query questions along with the corresponding SQL query statements without using placeholders
    4. Create a JSON array with each table as an object
    5. Each object must have exactly three fields:
       - "id": the table name
       - "question": a query in natural language.
       - "sql": sql statements without placeholders.
    6. The entire response must be ONLY valid JSON without any additional text, explanation, or markdown code blocks
    
    ## Required Output Format:
    {
        "items":[{
            "id": "<table name>",
            "question": "<a query in natural language>",
            "sql": "<sql statements>"
        }]
    }
    
    ## IMPORTANT:
    - Your response must contain ONLY the JSON object, nothing else
    - Do not include explanations, introductions, or conclusions
    - Do not use markdown code blocks (```) around the JSON
    - Do not include phrases like "Here's the JSON" or "I've created the JSON"
    - Do not indicate that you are providing the output in any way.""")
