import os
import ast
import requests
import logging
from jinja2 import Environment, FileSystemLoader

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# --- Code Parsing Functions ---
def parse_python_code(src_dir):
    """Parse Python files for functions, classes, and Flask routes."""
    docs = []
    for fname in os.listdir(src_dir):
        if fname.endswith('.py'):
            fpath = os.path.join(src_dir, fname)
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    source_code = f.read()
            except IOError as e:
                logging.error(f"Could not read file {fpath}: {e}")
                continue

            try:
                tree = ast.parse(source_code)
            except SyntaxError as e:
                logging.error(f"Syntax error in {fpath}: {e}")
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    route_path = None
                    for deco in node.decorator_list:
                        if (
                            isinstance(deco, ast.Call) and
                            getattr(getattr(deco, 'func', None), 'attr', '') == 'route'
                        ):
                            route_path = (
                                deco.args[0].s
                                if deco.args and isinstance(deco.args[0], ast.Constant)
                                else None
                            )
                    func_doc = ast.get_docstring(node)
                    docs.append({
                        'name': node.name,
                        'path': route_path,
                        'doc': func_doc,
                        'type': 'flask_route' if route_path else 'function',
                        'file': fname,
                        'code': ast.get_source_segment(source_code, node)
                    })
                elif isinstance(node, ast.ClassDef):
                    class_doc = ast.get_docstring(node)
                    docs.append({
                        'name': node.name,
                        'doc': class_doc,
                        'type': 'class',
                        'file': fname,
                        'code': ast.get_source_segment(source_code, node)
                    })
    return docs

def simple_summarize_code(code):
    """Basic summary of code functionality for demo purposes. Replace with API if needed."""
    if "Flask" in code:
        return "This code defines a Flask web server exposing an endpoint for currency conversion. It fetches live rates, performs conversion, validates numerical inputs, and handles errors gracefully."
    elif "requests" in code or "API" in code:
        return "This function/module integrates a third-party API (Alpha Vantage) to fetch live currency rates for conversion."
    else:
        return "This function or class is part of the currency converter backend logic."

# --- Document Rendering Functions ---
def render_docs(docs, output_dir):
    """Renders documentation into an HTML file using a Jinja2 template."""
    env = Environment(loader=FileSystemLoader('templates'))
    try:
        template = env.get_template('api_doc_template.html')
        output = template.render(docs=docs)
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, 'api_docs.html'), 'w', encoding='utf-8') as f:
            f.write(output)
        logging.info("HTML documentation generated.")
    except Exception as e:
        logging.error(f"HTML doc rendering failed: {e}")

def generate_plain_english_doc(docs, output_dir):
    """Generates summary with module highlights, API endpoints, error handling, and use cases."""
    lines = []
    lines.append("Currency Converter Python Code - Documentation\n" + "="*45 + "\n")
    for doc in docs:
        lines.append(f"Name: {doc['name']}")
        lines.append(f"Location: {doc['file']}")
        if doc.get('path'):
            lines.append(f"API Endpoint: {doc['path']}")
        lines.append(f"Type: {doc['type']}")
        if doc.get('doc'):
            lines.append("Docstring:")
            for line in doc['doc'].splitlines():
                lines.append(f"  - {line}")
        lines.append("Functionality Highlight:")
        lines.append("  " + simple_summarize_code(doc['code']))
        lines.append("Error Handling Highlight:")
        if "except" in doc['code']:
            lines.append("  This module uses try/except blocks to catch and gracefully handle errors, e.g., invalid inputs, API failures.")
        else:
            lines.append("  No explicit error handling.")
        lines.append("Use Cases:")
        if doc['type'] == 'flask_route':
            lines.append("  - Converts user input currency amounts using live exchange rates.")
            lines.append("  - Handles numeric validation and API integration.")
        elif doc['type'] == 'function':
            lines.append("  - Logic for currency conversion or backend calculation.")
        elif doc['type'] == 'class':
            lines.append("  - Structuring code and implementing reusable components.")
        lines.append("-"*40)
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'api_docs.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    logging.info("Plain English documentation generated.")

# --- Main ---
if __name__ == "__main__":
    py_src = './src/python'
    out_dir = './out'
    if not os.path.exists(py_src):
        logging.error(f"Source directory '{py_src}' not found.")
    elif not os.path.exists('templates'):
        logging.error("Template directory 'templates' not found.")
    else:
        docs = parse_python_code(py_src)
        if not docs:
            logging.warning("No code found for documentation.")
        else:
            render_docs(docs, out_dir)
            generate_plain_english_doc(docs, out_dir)
