import os

BASE_DIR = "../scrape_up"

INIT_CONTENT = '''import os
import importlib

modules = [f[:-3] for f in os.listdir(os.path.dirname(__file__)) if f.endswith(".py") and f not in ["__init__.py"]]

for module in modules:
    importlib.import_module(f".{module}", package=__name__)
'''

def create_init_files(base_dir: str):
    for root, dirs, files in os.walk(base_dir):
        py_files = [f for f in files if f.endswith('.py') and f != '__init__.py']
        if py_files:
            init_path = os.path.join(root, '__init__.py')
            if not os.path.exists(init_path):
                with open(init_path, 'w') as init_file:
                    init_file.write(INIT_CONTENT)
                print(f"✅ Created __init__.py in {root}")
            else:
                print(f"✔️ __init__.py already exists in {root}")

if __name__ == "__main__":
    create_init_files(BASE_DIR)
