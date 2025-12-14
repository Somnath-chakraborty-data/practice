import importlib

required = ['numpy', 'pandas', 'scikit-learn']

for pkg in required:
    try:
        importlib.import_module(pkg)
        print(f"{pkg} is installed.")
    except ImportError:
        print(f"{pkg} is NOT installed.")
