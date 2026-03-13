import subprocess, os, sys, re

def run_python_code(code: str):
    file_path = "temp_script.py"
    
    # --- IRONCLAD SYNTAX GUARD ---
    # This regex looks for 'try:' followed by a newline where the NEXT line 
    # is NOT indented. It then injects '    pass' to prevent the crash.
    code = re.sub(r"(try:\s*)\n(\S)", r"\1\n    pass\n\2", code)
    
    # Also handle the case where 'try:' is the very last line
    if code.strip().endswith("try:"):
        code += "\n    pass"

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
            f.flush()
            os.fsync(f.fileno())

        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout, result.stderr
    except Exception as e:
        return "", str(e)