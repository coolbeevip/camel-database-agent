# Copyright 2025 Lei Zhang
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import textwrap


class PromptTemplates:
    POLISH_SCHEMA_OUTPUT_EXAMPLE = textwrap.dedent("""
    Please add detailed {{language}} comments to the following DDL script, explaining the business meaning and design intent of each table and field.
    
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
    """)

    PARSE_SAMPLED_RECORD = textwrap.dedent("""
    # JSON Format Request
    You are a specialized JSON generator. Your only function is to parse the provided data and convert it to JSON format, strictly following the format requirements.
    
    ## Input Data:
    {{section}}
    
    ## Instructions:
    1. Create a JSON array with each table as an object
    2. Each object must have exactly three fields:
       - "id": the table name
       - "summary": a brief description of the table
       - "dataset": the data in markdown format
    3. The entire response must be ONLY valid JSON without any additional text, explanation, or markdown code blocks
    
    ## Required Output Format:
    {
        "items":[{
            "id": "<table name>",
            "summary": "<table summary>",
            "dataset": "<markdown dataset>"
        }]
    }
    
    ## IMPORTANT:
    - Your response must contain ONLY the JSON object, nothing else
    - Do not include explanations, introductions, or conclusions
    - Do not use markdown code blocks (```) around the JSON
    - Do not include phrases like "Here's the JSON" or "I've created the JSON"
    - Do not indicate that you are providing the output in any way""")
