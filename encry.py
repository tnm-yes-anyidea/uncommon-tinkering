# /// script
# dependencies = [
#   "cryptography",
# ]
# ///
import sys
import random
import hashlib
import os
from cryptography.fernet import Fernet

# --- OS ENCODING FIX ---
# Force UTF-8 for Windows compatibility and Linux pipe handling
if sys.platform == "win32":
    os.system('chcp 65001 > nul') # Set Windows Code Page to UTF-8
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# --- DATA ---
unicode_lookalikes = {
    'A': ['\u0391', '\u0410', '\uA4EE'], 'B': ['\u0392', '\u0412', '\u1517'],
    'C': ['\u0421', '\u212D', '\u216D'], 'D': ['\u216E', '\u13AA'],
    'E': ['\u0395', '\u0415', '\uA4FF'], 'F': ['\u03DC', '\uA4DD'],
    'G': ['\u050C', '\u13AC'], 'H': ['\u0397', '\u041D', '\uA4E7'],
    'I': ['\u0399', '\u0406', '\u2160'], 'J': ['\u0377', '\u0408'],
    'K': ['\u039A', '\u041A', '\u212A'], 'L': ['\u216C', '\uA4E1'],
    'M': ['\u039C', '\u041C', '\u216F'], 'N': ['\u039D', '\uFF2E'],
    'O': ['\u03BF', '\u041E', '\u104A0'], 'P': ['\u03A1', '\u0420', '\uA4D1'],
    'Q': ['\uFF31', '\u211A'], 'R': ['\uFF32', '\uA4E3'],
    'S': ['\u0405', '\uA4E2'], 'T': ['\u03A4', '\u0422', '\uA4D4'],
    'U': ['\uFF35', '\u222A'], 'V': ['\u2164', '\u2228'],
    'W': ['\uFF37', '\uA4EA'], 'X': ['\u03A7', '\u0425', '\u2169'],
    'Y': ['\u03A5', '\u04AE', '\uFF39'], 'Z': ['\u0396', '\uFF3A'],
    'a': ['\u0430', '\u0251'], 'b': ['\u042C', '\u266D'],
    'c': ['\u0441', '\u217C'], 'd': ['\u217D', '\u0501'],
    'e': ['\u0435', '\uFF45'], 'g': ['\u0261', '\uFF47'],
    'h': ['\u04BB', '\uFF48'], 'i': ['\u0456', '\u2170'],
    'j': ['\u0458', '\uFF4A'], 'k': ['\uFF4B', '\u03BA'],
    'm': ['\uFF4D', '\u217F'], 'n': ['\u0578', '\uFF4E'],
    'o': ['\u03BF', '\u043E', '\u2134'], 'p': ['\u0440', '\u03C1'],
    'q': ['\uFF51', '\u051B'], 'r': ['\u0433', '\uFF52'],
    's': ['\uFF53', '\u0455'], 't': ['\uFF54', '\u03C4'],
    'u': ['\u03C5', '\uFF55'], 'v': ['\u03BD', '\u2174'],
    'w': ['\uFF57', '\u03C9'], 'x': ['\u0445', '\u2179'],
    'y': ['\u0443', '\uFF59'], 'z': ['\uFF5A', '\u0290']
}

# --- LOGIC ---
def obfuscate(text, prob=0.4):
    return "".join(random.choice(unicode_lookalikes[c]) if c in unicode_lookalikes and random.random() < prob else c for c in text)

def main():
    # Argument Handling
    user_input = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Enter text to process: ")
    
    if not user_input:
        print("No input provided.")
        return

    # 1. Obfuscate
    lookalike_text = obfuscate(user_input)
    
    # 2. Hash (SHA-256)
    sha_hash = hashlib.sha256(lookalike_text.encode()).hexdigest()
    
    # 3. Encrypt (AES)
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted_text = cipher_suite.encrypt(lookalike_text.encode())

    # --- DISPLAY ---
    print("\n" + "="*40)
    print(f"RESULT:    {lookalike_text}")
    print(f"SHA-256:   {sha_hash}")
    print(f"ENCRYPTED: {encrypted_text.decode()}")
    print(f"KEY:       {key.decode()}")
    print("="*40 + "\n")

if __name__ == "__main__":
    main()