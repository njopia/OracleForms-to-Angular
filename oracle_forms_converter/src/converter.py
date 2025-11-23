"""
Oracle Forms to XML Converter
Handles the actual conversion using frmf2xml.bat
"""
import os
import subprocess
import tempfile
from pathlib import Path
import shutil


class FormsConverter:
    def __init__(self):
        self.oracle_home = None
        self.java_home = None
        self.output_dir = None

    def set_config(self, oracle_home, java_home, output_dir):
        """Set configuration paths"""
        self.oracle_home = oracle_home
        self.java_home = java_home if java_home else None
        self.output_dir = output_dir

        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)

    def create_batch_script(self):
        """Create the frmf2xml.bat script dynamically"""
        batch_content = f"""@ECHO OFF
REM Oracle Forms to XML Conversion Script
REM DESCRIPTION: This file is used to call the Forms2XML conversion tool.
REM It takes .fmb, .mmb, and .olb files and converts them into XML.

SETLOCAL

REM Setup the path to include the necessary Forms dlls.
set PATH={self.oracle_home}\\bin;%PATH%

REM Use JAVA_HOME if it exists, else use JDK in the Oracle_Home if it exists.
if exist %JAVA_HOME%\\bin\\java.exe (
    set FORMS_JDK_HOME=%JAVA_HOME%\\bin
    goto java_found
)

REM Setup CT_JAVA_HOME
set CT_JAVA_HOME=%CT_JAVA_HOME%

if exist %CT_JAVA_HOME%\\bin\\java.exe (
    set FORMS_JDK_HOME=%CT_JAVA_HOME%\\bin
    goto java_found
)

if exist {self.oracle_home}\\oracle_common\\jdk\\bin\\java.exe (
    set FORMS_JDK_HOME={self.oracle_home}\\oracle_common\\jdk\\bin
    goto java_found
)

echo Java not found: set JAVA_HOME.
goto end

:java_found

REM Run the tool with the required jar files added to the classpath
%FORMS_JDK_HOME%\\java -classpath {self.oracle_home}\\jlib\\frmxmltools.jar;{self.oracle_home}\\jlib\\frmf2xml.jar;{self.oracle_home}\\jlib\\frmdapi.jar;{self.oracle_home}\\oracle_common\\modules\\oracle.xdk\\xmlparserv2.jar oracle.forms.util.xmltools.Forms2XML %*

:end

ENDLOCAL
"""
        return batch_content

    def convert_file(self, input_file):
        """Convert a single Oracle Forms file to XML"""
        result = {
            'input_file': input_file,
            'success': False,
            'output_file': None,
            'error': None
        }

        try:
            # Validate input file
            if not os.path.exists(input_file):
                result['error'] = "El archivo no existe"
                return result

            # Get file extension
            file_ext = os.path.splitext(input_file)[1].lower()
            if file_ext not in ['.fmb', '.mmb', '.olb']:
                result['error'] = f"Formato no soportado: {file_ext}"
                return result

            # Prepare output file path
            base_name = os.path.splitext(os.path.basename(input_file))[0]
            output_file = os.path.join(self.output_dir, f"{base_name}.xml")

            # Create temporary batch script
            with tempfile.NamedTemporaryFile(mode='w', suffix='.bat', delete=False) as bat_file:
                bat_file.write(self.create_batch_script())
                batch_script = bat_file.name

            try:
                # Prepare command
                # Forms2XML syntax: Forms2XML source=input.fmb dest=output.xml overwrite=yes
                cmd = [
                    batch_script,
                    f'source={input_file}',
                    f'dest={output_file}',
                    'overwrite=yes'
                ]

                # Set environment variables
                env = os.environ.copy()
                if self.oracle_home:
                    env['ORACLE_HOME'] = self.oracle_home
                    env['PATH'] = f"{self.oracle_home}\\bin;{env.get('PATH', '')}"

                if self.java_home:
                    env['JAVA_HOME'] = self.java_home

                # Execute conversion
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env=env,
                    text=True,
                    shell=True
                )

                stdout, stderr = process.communicate(timeout=120)  # 2 minute timeout

                # Check if output file was created
                if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                    result['success'] = True
                    result['output_file'] = output_file
                else:
                    result['error'] = f"No se generó el archivo XML. STDERR: {stderr}"

            finally:
                # Clean up temporary batch file
                try:
                    os.unlink(batch_script)
                except:
                    pass

        except subprocess.TimeoutExpired:
            result['error'] = "La conversión excedió el tiempo límite (2 minutos)"
        except Exception as e:
            result['error'] = str(e)

        return result

    def convert_files_batch(self, input_files, progress_callback=None):
        """Convert multiple files with optional progress callback"""
        results = []
        total = len(input_files)

        for i, input_file in enumerate(input_files):
            result = self.convert_file(input_file)
            results.append(result)

            if progress_callback:
                progress_callback(i + 1, total, result)

        return results

    def validate_setup(self):
        """Validate that all required components are available"""
        errors = []

        if not self.oracle_home:
            errors.append("Oracle Home no configurado")
        elif not os.path.exists(self.oracle_home):
            errors.append(f"Oracle Home no existe: {self.oracle_home}")
        else:
            # Check for required JAR files
            required_jars = [
                'jlib\\frmxmltools.jar',
                'jlib\\frmf2xml.jar',
                'jlib\\frmdapi.jar'
            ]

            for jar in required_jars:
                jar_path = os.path.join(self.oracle_home, jar)
                if not os.path.exists(jar_path):
                    errors.append(f"JAR requerido no encontrado: {jar}")

        if not self.output_dir:
            errors.append("Directorio de salida no configurado")

        # Check for Java
        java_found = False
        if self.java_home and os.path.exists(os.path.join(self.java_home, 'bin', 'java.exe')):
            java_found = True
        elif self.oracle_home:
            oracle_java = os.path.join(self.oracle_home, 'oracle_common', 'jdk', 'bin', 'java.exe')
            if os.path.exists(oracle_java):
                java_found = True

        if not java_found:
            errors.append("Java no encontrado. Configure JAVA_HOME o use el JDK incluido en Oracle")

        return len(errors) == 0, errors
