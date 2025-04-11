class PromptTemplates:
    QUESTION_INFERENCE_PIPELINE = """Please carefully analyze the following database information and conduct an in-depth analysis from a business perspective. What business query questions might users raise? Please fully consider some complex query scenarios, including but not limited to multi-table associations, grouping statistics, etc.

    Database Schema:
    ```
    {{ddl_sql}}
    ```

    Data Example:
    ```sql
    {{data_sql}}
    ```

    Now, Please generate {{query_samples_size}} real user query questions along with the corresponding SQL query statements without using placeholders. Please output in JSON format."""
