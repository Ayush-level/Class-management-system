from abc import ABC, abstractmethod
from typing import Optional, Any, Dict, List
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from database.model import get_database_manager
import logging

logger = logging.getLogger(__name__)

class BaseService(ABC):
    """Base service class providing common database operations and error handling"""
    
    def __init__(self):
        self.db_manager = get_database_manager()
        self.engine: Optional[Engine] = None
    
    def get_engine(self) -> Engine:
        """Get database engine"""
        if self.engine is None:
            self.engine = self.db_manager.get_engine()
        return self.engine
    
    def execute_query(self, query, params: Optional[Dict] = None) -> Any:
        """Execute a database query with error handling"""
        try:
            with self.get_engine().connect() as conn:
                if params:
                    result = conn.execute(query, params)
                else:
                    result = conn.execute(query)
                return result
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            raise DatabaseException(f"Database operation failed: {str(e)}")
    
    def execute_insert(self, table_name: str, data: Dict) -> Any:
        """Insert data into a table"""
        table = self.db_manager.get_table(table_name)
        insert_stmt = table.insert().values(**data)
        return self.execute_query(insert_stmt)
    
    def execute_select(self, table_name: str, where_clause: Optional[str] = None, params: Optional[Dict] = None) -> List[Dict]:
        """Select data from a table"""
        table = self.db_manager.get_table(table_name)
        select_stmt = table.select()
        
        if where_clause:
            select_stmt = select_stmt.where(text(where_clause))
        
        result = self.execute_query(select_stmt, params)
        return [dict(row._mapping) for row in result]
    
    def execute_update(self, table_name: str, data: Dict, where_clause: str, params: Dict) -> Any:
        """Update data in a table"""
        table = self.db_manager.get_table(table_name)
        update_stmt = table.update().values(**data).where(text(where_clause))
        return self.execute_query(update_stmt, params)
    
    def execute_delete(self, table_name: str, where_clause: str, params: Dict) -> Any:
        """Delete data from a table"""
        table = self.db_manager.get_table(table_name)
        delete_stmt = table.delete().where(text(where_clause))
        return self.execute_query(delete_stmt, params)
    
    def exists(self, table_name: str, where_clause: str, params: Dict) -> bool:
        """Check if a record exists"""
        table = self.db_manager.get_table(table_name)
        exists_stmt = table.select().where(text(where_clause)).limit(1)
        result = self.execute_query(exists_stmt, params)
        return result.rowcount > 0
