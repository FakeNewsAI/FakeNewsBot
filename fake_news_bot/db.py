from langchain_community.cache import SQLAlchemyCache
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class MySQLCache(SQLAlchemyCache):
    """Cache that uses Sqlite. This is created for deleting cache records."""

    def __init__(self, database_path: str = ".langchain.db"):
        """Initialize by creating the engine and all tables."""
        engine = create_engine(f"sqlite:///{database_path}")
        super().__init__(engine)

    def delete_by_prompt(self, prompt: str) -> None:
        """Delete records based on prompt."""
        with Session(self.engine) as session:
            try:
                question_prompt = f"Question: {prompt}"
                rows = session.query(self.cache_schema).filter(self.cache_schema.prompt.contains(question_prompt)).delete()
                print("Deleted", rows, "rows")
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                # Handle exception or log the error here
                print(f"Error occurred: {e}")
