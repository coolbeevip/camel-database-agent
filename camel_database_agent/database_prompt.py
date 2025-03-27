DATABASE_SUMMARY_OUTPUT_EXAMPLE = """You are a business database expert. Please generate a {{language}} database summary based on the following table structure, with the aim of helping people understand what information this database can provide from a business perspective.

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
"""

POLISH_SCHEMA_OUTPUT_EXAMPLE = """Please add detailed {{language}} comments to the following DDL script, explaining the business meaning and design intent of each table and field.

Requirements:
- Keep the original DDL script completely unchanged
- Add comments before the script
- Comments should be professional and concise
- Use SQL -- comment syntax

DDL Script:
```sql
{{ddl_sql}}
```

Output Example:
```json
-- User Management Table stores basic information and authentication credentials for system users. Applicable scenarios include user registration, login, and permission management.
CREATE TABLE users (    
    id INT AUTO_INCREMENT PRIMARY KEY, -- Unique user identifier, auto-increment ID    
    username VARCHAR(50) NOT NULL UNIQUE, -- User login account, 50 character length, ensures uniqueness    
    email VARCHAR(100) NOT NULL UNIQUE, -- User email, used for notifications and password recovery, 100 character length    
    password VARCHAR(255) NOT NULL, -- User password stored with encryption, recommended to use hash algorithm        
    full_name VARCHAR(100), -- User full name, optional field    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- User account creation timestamp, defaults to current time        
    last_login TIMESTAMP NULL, -- Most recent login time, can be initially null        
    is_active BOOLEAN DEFAULT TRUE -- Account status flag, default is active
);
```

Key Strategies:
- Clearly instruct not to modify the original DDL
- Provide specific guidance for adding comments
- Specify the expected format and content of comments
- Emphasize professionalism and conciseness
"""

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


QUESTION_CONVERT_SQL = """The following is the table structure in the database and some common query SQL statements. Please convert the user's question into an SQL query statement. Note to comply with sqlite syntax. Do not explain, just provide the SQL directly.

Database System: {{dialect_name}}

## Table Schema
```sql
{{table_schema}}
```

## Data Example
```sql
{{sample_data}}
```

{{qa_pairs}}
QUESTION: {{question}}
SQL: 
"""
