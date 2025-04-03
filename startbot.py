import subprocess
import os

# Finn riktig sti til python i venv
base_path = os.path.dirname(os.path.abspath(__file__))
venv_python = os.path.join(base_path, "venv", "bin", "python3")

# Kjør bot_v5.py
print("🔁 Kjører bot_v5.py ...")
subprocess.run([venv_python, "bot_v5.py"])

# Kjør rapport.py
print("📄 Kjører rapport.py ...")
subprocess.run([venv_python, "rapport.py"])

print("\n✅ Ferdig! Rapporten ligger i 'dagens_ai_rapport.txt'")
input("\nTrykk Enter for å lukke vinduet.")

