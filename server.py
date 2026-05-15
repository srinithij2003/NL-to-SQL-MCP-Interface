from mcp.server.fastmcp import FastMCP
import sqlite3

# Initialize the FastMCP server
mcp = FastMCP("NL-to-SQL-Interface")

# Point to the MLOps registry we just built
DB_PATH = 'mlops_registry.db'

@mcp.tool()
def list_tables() -> str:
    """List all tables available in the database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Query the SQLite master table to find all user-created tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        tables = cursor.fetchall()
        conn.close()
        
        table_names = [t[0] for t in tables]
        return f"Available tables: {', '.join(table_names)}"
    except Exception as e:
        return f"Error connecting to database: {str(e)}"

@mcp.tool()
def describe_table(table_name: str) -> str:
    """Get the schema and column details for a specific table. Always call this before writing a query."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        conn.close()
        
        if not columns:
            return f"Error: Table '{table_name}' not found."
        
        schema = f"Schema for {table_name}:\n"
        for col in columns:
            # col[1] is name, col[2] is data type
            schema += f"- {col[1]} ({col[2]})\n" 
        return schema
    except Exception as e:
        return f"Error reading schema: {str(e)}"

@mcp.tool()
def execute_query(query: str) -> str:
    """Execute a READ-ONLY SQL query and return the results."""
    # Senior Engineer Touch: A basic safeguard against destructive queries
    forbidden_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'ALTER', 'TRUNCATE']
    if any(keyword in query.upper() for keyword in forbidden_keywords):
        return "Error: For security reasons, only SELECT (read-only) queries are permitted."
        
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Get column names for better readability
        column_names = [description[0] for description in cursor.description]
        conn.close()
        
        # Format the output cleanly for the LLM to read
        output = f"Columns: {column_names}\n"
        output += f"Total Rows: {len(results)}\nResults:\n"
        for row in results:
            output += f"{row}\n"
            
        return output
    except Exception as e:
        return f"SQL Execution Error: {str(e)}"

if __name__ == "__main__":
    # Run the server
    print("Starting NL-to-SQL MCP Interface...")
    mcp.run()