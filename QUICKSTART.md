# Guía de Inicio Rápido

## 🚀 Inicio Rápido en 3 Pasos

### 1. Requisitos Previos (One-time setup)

- ✅ Python 3.8+ instalado
- ✅ Oracle Forms Developer instalado
- ✅ Java disponible (incluido en Oracle o separado)

### 2. Ejecutar la Aplicación

**Windows:**
```
Doble clic en: run_converter.bat
```

**Linux/Mac:**
```bash
./run_converter.sh
```

**O manualmente:**
```bash
cd oracle_forms_converter/src
python main.py
```

### 3. Configurar y Convertir

1. **Paso 1 - Configuración**:
   - Oracle Home: `C:\Oracle\Middleware\Oracle_FRHome1`
   - Output: Donde quieras los XML
   - Click "Verificar Configuración"

2. **Paso 2 - Archivos**:
   - Click "Agregar Archivos" o "Agregar Directorio"
   - Selecciona tus archivos `.fmb`, `.mmb`, o `.olb`

3. **Paso 3 - Convertir**:
   - Click "Iniciar Conversión"
   - Observa el progreso

4. **Paso 4 - Resultados**:
   - Revisa resultados
   - Click "Abrir Carpeta de Salida" para ver XMLs

## 🎯 Ejemplo de Configuración

### Windows Típico:
- **Oracle Home**: `C:\Oracle\Middleware\Oracle_FRHome1`
- **Java Home**: `C:\Program Files\Java\jdk1.8.0_281` (o déjalo vacío)
- **Output**: `C:\Users\TuUsuario\Documents\FormsXML`

### Linux/Mac:
- **Oracle Home**: `/opt/oracle/middleware/oracle_frhome1`
- **Java Home**: `/usr/lib/jvm/java-8-openjdk`
- **Output**: `/home/usuario/forms_xml`

## ❓ Problemas Comunes

### "Python no está instalado"
👉 Descarga Python desde [python.org](https://www.python.org)
👉 Marca "Add Python to PATH" durante instalación

### "tkinter no está disponible" (Linux)
```bash
sudo apt-get install python3-tk
```

### "Java not found"
👉 Instala Java JDK 8+
👉 O configura JAVA_HOME
👉 O deja vacío para usar el de Oracle

### "Oracle Home no existe"
👉 Verifica la ruta de instalación de Oracle Forms
👉 Debe contener carpeta `jlib` con los JARs

## 📚 Más Información

Ver **README.md** para documentación completa.

## 🆘 Soporte

- Issues: [GitHub Issues](https://github.com/tu-repo/issues)
- Docs: Ver README.md y comentarios en el código
