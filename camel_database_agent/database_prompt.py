import textwrap


class PromptTemplates:
    DATABASE_SUMMARY_OUTPUT_EXAMPLE = textwrap.dedent("""
    You are a business database expert. Please generate a {{language}} database summary based on the following table structure, with the aim of helping people understand what information this database can provide from a business perspective.
    
    ## Table Schema
    {{ddl_sql}}
    
    ## Output Example
    
    This database is the core data model of a typical e-commerce system,  
    including modules for user management, product management, order transactions,  
    payment processes, and address management.  
    
    It achieves a complete business loop through multi-table associations  
    (such as user-order-product-payment), supporting users throughout  
    the entire process from registration, browsing products,  
    placing orders and making payments to receiving goods.  
    
    Each table ensures data consistency through foreign key constraints  
    (such as the strong association between orders and users or addresses)  
    and includes timestamp fields (`created_at`/`updated_at`) for tracking data changes.
    
    Now, You only need to output a descriptive text in {{language}}.
    """)

    QUESTION_CONVERT_SQL = textwrap.dedent("""
    The following is the table structure in the database and some common query SQL statements. Please convert the user's question into an SQL query statement. Note to comply with sqlite syntax. Do not explain, just provide the SQL directly.
    
    Database System: {{dialect_name}}
    
    ## Table Schema
    ```sql
    {{table_schema}}
    ```
    
    ## Data Example
    ```sql
    {{sample_data}}
    ```
    ## Few-Shot Example
    {{qa_pairs}}
    
    ## User Question
    {{question}}
    
    ## Instructions
    1. Follow {{dialect_name}} syntax
    2. Do not provide explanations, just give the SQL statement directly
    """)
