import json #we use this so that our python data can turn into clean json strings
from sandbox import sandbox
def query_products_db(search_term: str) -> str:
    raw_query = f"SELECT id, name, category, price, stock FROM products WHERE name LIKE '%{search_term}%'"
    try:
        results = sandbox.execute_raw_query(raw_query)
        if not results:
            return json.dumps({"message": f"No products found matching '{search_term}'."})
        return json.dumps({"results": results})# Converts the list of matching database rows into a JSON string for the AI.
    except Exception as e:
        return json.dumps({"error": f"Database SQL Error: {str(e)}", "query_executed": raw_query})
def list_files() -> str:
    """Lists available documentation files in the repository."""
    return json.dumps({"files": list(sandbox.files.keys())})
def read_file(filename: str) -> str:
    clean_name = filename.strip()#Removes any accidental extra spaces.
    if clean_name in sandbox.files:
        return sandbox.files[clean_name]
    return f"Error: File '{clean_name}' not found."
# Dictionary mapping tool names to Python functions
tool_registry= {
    "query_products_db": query_products_db,
    "list_files": list_files,
    "read_file": read_file
}
