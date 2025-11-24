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

    def find_oracle_frmf2xml_bat(self):
        """Find the original Oracle frmf2xml.bat script"""
        if not self.oracle_home:
            return None

        # Common locations for frmf2xml.bat in Oracle Forms installation
        possible_locations = [
            # Standard locations
            os.path.join(self.oracle_home, 'bin', 'frmf2xml.bat'),
            os.path.join(self.oracle_home, 'forms', 'frmf2xml.bat'),
            os.path.join(self.oracle_home, 'frmf2xml.bat'),
            # Template scripts location (Oracle 12c+) - Esta es tu ubicación!
            os.path.join(self.oracle_home, 'forms', 'templates', 'scripts', 'frmf2xml.bat'),
            # Alternative bin location
            os.path.join(self.oracle_home, 'forms', 'bin', 'frmf2xml.bat'),
        ]

        for bat_path in possible_locations:
            if os.path.exists(bat_path):
                return bat_path

        return None

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
set CLASSPATH={self.oracle_home}\\jlib\\frmxmltools.jar
set CLASSPATH=%CLASSPATH%;{self.oracle_home}\\jlib\\frmf2xml.jar
set CLASSPATH=%CLASSPATH%;{self.oracle_home}\\jlib\\frmdapi.jar
set CLASSPATH=%CLASSPATH%;{self.oracle_home}\\jlib\\frmjdapi.jar
set CLASSPATH=%CLASSPATH%;{self.oracle_home}\\jlib\\xmlparserv2.jar
set CLASSPATH=%CLASSPATH%;{self.oracle_home}\\oracle_common\\modules\\oracle.xdk\\xmlparserv2.jar
set CLASSPATH=%CLASSPATH%;{self.oracle_home}\\forms\\java\\frmall.jar

%FORMS_JDK_HOME%\\java -classpath %CLASSPATH% oracle.forms.util.xmltools.Forms2XML %*

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

            # Try to find Oracle's original frmf2xml.bat first
            oracle_bat = self.find_oracle_frmf2xml_bat()
            batch_script = None
            cleanup_batch = False
            using_oracle_bat = False

            if oracle_bat:
                # Use Oracle's original batch script
                batch_script = oracle_bat
                using_oracle_bat = True
                result['conversion_method'] = f'Oracle original: {oracle_bat}'
            else:
                # Create our own temporary batch script as fallback
                with tempfile.NamedTemporaryFile(mode='w', suffix='.bat', delete=False) as bat_file:
                    bat_file.write(self.create_batch_script())
                    batch_script = bat_file.name
                    cleanup_batch = True
                result['conversion_method'] = 'Generated batch script'

            try:
                # Prepare command based on which script we're using
                if using_oracle_bat:
                    # Oracle's frmf2xml.bat syntax: frmf2xml.bat "archivo.fmb"
                    # Creates XML in the same directory as the input file
                    cmd = [batch_script, input_file]
                    # Calculate where Oracle will create the XML
                    temp_xml = os.path.splitext(input_file)[0] + '.xml'
                else:
                    # Our generated script syntax: script source=input.fmb dest=output.xml overwrite=yes
                    cmd = [
                        batch_script,
                        f'source={input_file}',
                        f'dest={output_file}',
                        'overwrite=yes'
                    ]
                    temp_xml = None

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

                # Check if output file was created based on which method we used
                if using_oracle_bat:
                    # Oracle creates XML in the same directory as input file
                    if temp_xml and os.path.exists(temp_xml) and os.path.getsize(temp_xml) > 0:
                        # Move the XML from input directory to our output directory
                        try:
                            if temp_xml != output_file:
                                # Copy to output directory
                                shutil.copy2(temp_xml, output_file)
                                # Optionally remove the original (uncomment if desired)
                                # os.remove(temp_xml)
                            result['success'] = True
                            result['output_file'] = output_file
                        except Exception as e:
                            result['error'] = f"Error moviendo XML: {str(e)}"
                    else:
                        result['error'] = f"No se generó el archivo XML. STDERR: {stderr}"
                else:
                    # Our generated script creates XML in the specified output location
                    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                        result['success'] = True
                        result['output_file'] = output_file
                    else:
                        result['error'] = f"No se generó el archivo XML. STDERR: {stderr}"

            finally:
                # Clean up temporary batch file (only if we created it)
                if cleanup_batch and batch_script:
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
        warnings = []

        if not self.oracle_home:
            errors.append("Oracle Home no configurado")
        elif not os.path.exists(self.oracle_home):
            errors.append(f"Oracle Home no existe: {self.oracle_home}")
        else:
            # Check for required JAR files
            required_jars = [
                ('jlib\\frmxmltools.jar', True),
                ('jlib\\frmf2xml.jar', True),
                ('jlib\\frmdapi.jar', True),
                ('jlib\\frmjdapi.jar', True),
                ('jlib\\xmlparserv2.jar', False),  # May be in oracle_common instead
                ('oracle_common\\modules\\oracle.xdk\\xmlparserv2.jar', False),
                ('forms\\java\\frmall.jar', False),
            ]

            for jar, is_critical in required_jars:
                jar_path = os.path.join(self.oracle_home, jar)
                if not os.path.exists(jar_path):
                    if is_critical:
                        errors.append(f"JAR crítico no encontrado: {jar}")
                    else:
                        warnings.append(f"JAR opcional no encontrado: {jar}")

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

        return len(errors) == 0, errors, warnings

    def get_diagnostic_info(self):
        """Get detailed diagnostic information about the setup"""
        info = {
            'oracle_home': self.oracle_home,
            'oracle_home_exists': os.path.exists(self.oracle_home) if self.oracle_home else False,
            'java_home': self.java_home,
            'output_dir': self.output_dir,
            'jars_found': [],
            'jars_missing': [],
            'java_executable': None,
            'oracle_frmf2xml_bat': None,
            'has_oracle_bat': False
        }

        # Check for Oracle's original frmf2xml.bat
        oracle_bat = self.find_oracle_frmf2xml_bat()
        if oracle_bat:
            info['oracle_frmf2xml_bat'] = oracle_bat
            info['has_oracle_bat'] = True

        if self.oracle_home and os.path.exists(self.oracle_home):
            # Check all possible JARs
            possible_jars = [
                'jlib\\frmxmltools.jar',
                'jlib\\frmf2xml.jar',
                'jlib\\frmdapi.jar',
                'jlib\\frmjdapi.jar',
                'jlib\\xmlparserv2.jar',
                'oracle_common\\modules\\oracle.xdk\\xmlparserv2.jar',
                'forms\\java\\frmall.jar',
            ]

            for jar in possible_jars:
                jar_path = os.path.join(self.oracle_home, jar)
                if os.path.exists(jar_path):
                    info['jars_found'].append(jar)
                else:
                    info['jars_missing'].append(jar)

        # Find Java executable
        if self.java_home and os.path.exists(os.path.join(self.java_home, 'bin', 'java.exe')):
            info['java_executable'] = os.path.join(self.java_home, 'bin', 'java.exe')
        elif self.oracle_home:
            oracle_java = os.path.join(self.oracle_home, 'oracle_common', 'jdk', 'bin', 'java.exe')
            if os.path.exists(oracle_java):
                info['java_executable'] = oracle_java

        return info
