# start_debug.py -- put this at project root and use as temporary start command on Render
import sys, os, traceback

def find_numpy_on_path():
    found = []
    for p in sys.path:
        if not p:
            p = os.getcwd()
        name = os.path.basename(os.path.normpath(p))
        try:
            entries = os.listdir(p)
        except Exception:
            entries = []
        # check for any folder/file named 'numpy' or 'numpy.py'
        for e in entries:
            if e.lower().startswith('numpy'):
                found.append(os.path.join(p, e))
    return found

print("=== DEBUG START ===")
print("cwd:", os.getcwd())
print("sys.executable:", sys.executable)
print("python version:", sys.version.replace('\\n',' '))
print("sys.path (first 12 entries):")
for i, p in enumerate(sys.path[:12]):
    print(f" {i}: {p!r}")
print()
numpy_hits = find_numpy_on_path()
print("Potential numpy-like entries found on sys.path:")
if numpy_hits:
    for h in numpy_hits:
        print(" -", h)
else:
    print(" - NONE found in listed sys.path entries (scan limited to readable entries)")
print()

print("Attempting to import numpy and show details...")
try:
    import importlib, numpy
    print("IMPORT OK")
    print("numpy.__file__:", getattr(numpy, '__file__', None))
    print("numpy.__path__:", getattr(numpy, '__path__', None))
    # print first 5 files inside the numpy package (if accessible)
    try:
        if hasattr(numpy, '__path__'):
            sample_files = [f for f in os.listdir(numpy.__path__[0])][:10]
            print("sample files in numpy package:", sample_files)
    except Exception as e:
        print("Could not list numpy package files:", e)
except Exception as e:
    print("IMPORT FAILED — full traceback below:")
    traceback.print_exc()

print("=== DEBUG END ===")

# After debug, start the real app to see the same logs (optional)
# If you want to auto-start uvicorn as well, uncomment these lines and adjust import path:
# import runpy
# runpy.run_path('start_uvicorn.py', run_name='__main__')
