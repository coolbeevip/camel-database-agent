class PromptTemplates:
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
