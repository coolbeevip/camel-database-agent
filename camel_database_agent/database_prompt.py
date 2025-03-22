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
