import subprocess, sys

print("\nStarting app at external browser")
print("Ctrl+C to stop")

from src.classifier import train_model
train_model()
subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])