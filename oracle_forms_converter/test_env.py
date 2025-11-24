"""
Script de diagnóstico para verificar variables de entorno
"""
import os
import sys

print("=" * 70)
print("DIAGNÓSTICO DE VARIABLES DE ENTORNO")
print("=" * 70)
print()

# Check Python version
print(f"Python Version: {sys.version}")
print(f"Python Executable: {sys.executable}")
print()

# Check ORACLE_HOME
oracle_home = os.environ.get('ORACLE_HOME', '')
print(f"ORACLE_HOME detectado:")
print(f"  Valor: {oracle_home if oracle_home else '(no configurado)'}")
print(f"  Existe: {os.path.exists(oracle_home) if oracle_home else 'N/A'}")
print()

# Check JAVA_HOME
java_home = os.environ.get('JAVA_HOME', '')
print(f"JAVA_HOME detectado:")
print(f"  Valor: {java_home if java_home else '(no configurado)'}")
print(f"  Existe: {os.path.exists(java_home) if java_home else 'N/A'}")
print()

# List all environment variables with ORACLE or JAVA
print("Todas las variables con 'ORACLE' o 'JAVA':")
print("-" * 70)
for key, value in sorted(os.environ.items()):
    if 'ORACLE' in key.upper() or 'JAVA' in key.upper():
        print(f"  {key} = {value}")
print()

print("=" * 70)
print("Presiona Enter para cerrar...")
input()
