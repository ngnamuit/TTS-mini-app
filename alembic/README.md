## Follow these step for first run app
### 1. Initialize Alembic
- If you haven’t already initialized Alembic in your project, do so by running: `alembic init alembic`

### 2. Configure Alembic
- Edit alembic.ini: `sqlalchemy.url = postgresql://fastapi_user:securepassword@localhost/fastapi_db`
- Edit alembic/env.py:
    ```
    from app.database import Base  # Import Base from your project
    from app.models import Transaction  # Ensure your model is imported
    
    target_metadata = Base.metadata
    ```

### 3. Generate Migration Script
- Run the following command to autogenerate a migration script for the Transaction table:
    ```
    alembic revision --autogenerate -m "Create Transaction table"
    ```

### 4. Run cmd
- Create new alembic: `alembic revision --autogenerate -m "Create Transaction table"`
- Migrate it to database: `alembic upgrade head`
    
    
   