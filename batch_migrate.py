#!/usr/bin/env python
"""
Script de migración por lotes: Oracle Forms → Angular
Convierte archivos .fmb a XML y luego genera componentes Angular

Uso:
    python batch_migrate.py <zip_file>
    python batch_migrate.py <directory_with_fmb>
    python batch_migrate.py <single_fmb_file>
"""
import os
import sys
import zipfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'oracle_forms_converter', 'src'))

from converter import FormsConverter
from angular_generator import AngularGenerator


class BatchMigrator:
    """Migración por lotes de Oracle Forms a Angular"""

    def __init__(self, oracle_home: str = None, java_home: str = None):
        """
        Inicializa el migrador por lotes

        Args:
            oracle_home: Ruta a Oracle Home (opcional, se detectará automáticamente)
            java_home: Ruta a Java Home (opcional, se detectará automáticamente)
        """
        self.oracle_home = oracle_home or os.environ.get('ORACLE_HOME', '')
        self.java_home = java_home or os.environ.get('JAVA_HOME', '')

        # Directorios de trabajo
        self.work_dir = os.path.join(os.getcwd(), 'migration_work')
        self.fmb_dir = os.path.join(self.work_dir, 'forms')
        self.xml_dir = os.path.join(self.work_dir, 'xml_output')
        self.angular_dir = os.path.join(self.work_dir, 'angular_output')

        # Crear directorios
        os.makedirs(self.work_dir, exist_ok=True)
        os.makedirs(self.fmb_dir, exist_ok=True)
        os.makedirs(self.xml_dir, exist_ok=True)
        os.makedirs(self.angular_dir, exist_ok=True)

    def extract_zip(self, zip_file: str) -> List[str]:
        """
        Extrae archivos .fmb de un ZIP

        Args:
            zip_file: Ruta al archivo ZIP

        Returns:
            Lista de rutas a archivos .fmb extraídos
        """
        print(f"\n{'='*70}")
        print(f"Extrayendo archivos de: {zip_file}")
        print(f"{'='*70}\n")

        fmb_files = []

        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            # Listar todos los archivos
            all_files = zip_ref.namelist()

            # Filtrar archivos .fmb, .mmb, .olb, .pll
            supported_extensions = ['.fmb', '.mmb', '.olb', '.pll']
            forms_files = [
                f for f in all_files
                if any(f.lower().endswith(ext) for ext in supported_extensions)
            ]

            print(f"Archivos encontrados: {len(forms_files)}")

            # Extraer archivos
            for file_path in forms_files:
                # Extraer solo el nombre del archivo (sin directorios internos del ZIP)
                filename = os.path.basename(file_path)
                target_path = os.path.join(self.fmb_dir, filename)

                # Extraer archivo
                with zip_ref.open(file_path) as source:
                    with open(target_path, 'wb') as target:
                        shutil.copyfileobj(source, target)

                fmb_files.append(target_path)
                print(f"  ✓ {filename}")

        print(f"\nTotal extraídos: {len(fmb_files)} archivos")
        return fmb_files

    def find_fmb_files(self, directory: str) -> List[str]:
        """
        Encuentra todos los archivos .fmb en un directorio

        Args:
            directory: Directorio a buscar

        Returns:
            Lista de rutas a archivos .fmb
        """
        print(f"\n{'='*70}")
        print(f"Buscando archivos Oracle Forms en: {directory}")
        print(f"{'='*70}\n")

        supported_extensions = ['.fmb', '.mmb', '.olb', '.pll']
        fmb_files = []

        for ext in supported_extensions:
            pattern = f'**/*{ext}'
            files = list(Path(directory).glob(pattern))
            fmb_files.extend([str(f) for f in files])

        print(f"Archivos encontrados: {len(fmb_files)}")
        for f in fmb_files:
            print(f"  - {os.path.basename(f)}")

        return fmb_files

    def convert_to_xml(self, fmb_files: List[str]) -> List[str]:
        """
        Convierte archivos .fmb a XML

        Args:
            fmb_files: Lista de archivos .fmb

        Returns:
            Lista de archivos XML generados
        """
        print(f"\n{'#'*70}")
        print(f"# FASE 1: CONVERSIÓN .FMB → XML")
        print(f"# Archivos a convertir: {len(fmb_files)}")
        print(f"{'#'*70}\n")

        # Crear conversor
        converter = FormsConverter(
            oracle_home=self.oracle_home,
            java_home=self.java_home,
            output_dir=self.xml_dir
        )

        xml_files = []
        successful = 0
        failed = 0

        for i, fmb_file in enumerate(fmb_files, 1):
            print(f"[{i}/{len(fmb_files)}] Convirtiendo: {os.path.basename(fmb_file)}")

            result = converter.convert_file(fmb_file)

            if result['success']:
                xml_files.append(result['output_file'])
                successful += 1
                print(f"  ✓ Éxito: {os.path.basename(result['output_file'])}")
            else:
                failed += 1
                print(f"  ✗ Error: {result.get('error', 'Unknown error')}")

            print()

        print(f"{'='*70}")
        print(f"Resumen Fase 1:")
        print(f"  Total: {len(fmb_files)}")
        print(f"  Exitosos: {successful}")
        print(f"  Fallidos: {failed}")
        print(f"{'='*70}\n")

        return xml_files

    def generate_angular(self, xml_files: List[str]) -> List[Dict]:
        """
        Genera componentes Angular desde archivos XML

        Args:
            xml_files: Lista de archivos XML

        Returns:
            Lista de resultados de generación
        """
        print(f"\n{'#'*70}")
        print(f"# FASE 2: GENERACIÓN DE COMPONENTES ANGULAR")
        print(f"# Archivos XML a procesar: {len(xml_files)}")
        print(f"{'#'*70}\n")

        generator = AngularGenerator(self.angular_dir)
        results = generator.generate_from_multiple_xmls(xml_files)

        # Generar reporte
        report_file = os.path.join(self.angular_dir, 'migration_report.html')
        generator.generate_summary_report(results, report_file)

        return results

    def migrate(self, source: str) -> Dict:
        """
        Ejecuta el proceso completo de migración

        Args:
            source: Puede ser un archivo ZIP, directorio, o archivo .fmb individual

        Returns:
            Diccionario con resultados de la migración
        """
        start_time = datetime.now()

        print("\n" + "="*70)
        print("MIGRACIÓN ORACLE FORMS → ANGULAR")
        print("="*70)
        print(f"Fuente: {source}")
        print(f"Inicio: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)

        # 1. Determinar tipo de fuente y obtener archivos .fmb
        fmb_files = []

        if source.lower().endswith('.zip'):
            fmb_files = self.extract_zip(source)
        elif os.path.isdir(source):
            fmb_files = self.find_fmb_files(source)
        elif os.path.isfile(source):
            # Archivo individual
            fmb_files = [source]
        else:
            print(f"ERROR: Fuente no válida: {source}")
            return {'success': False, 'error': 'Invalid source'}

        if not fmb_files:
            print("ERROR: No se encontraron archivos Oracle Forms")
            return {'success': False, 'error': 'No Oracle Forms files found'}

        # 2. Convertir .fmb a XML
        xml_files = self.convert_to_xml(fmb_files)

        if not xml_files:
            print("ERROR: No se generaron archivos XML")
            return {'success': False, 'error': 'No XML files generated'}

        # 3. Generar componentes Angular
        results = self.generate_angular(xml_files)

        end_time = datetime.now()
        duration = end_time - start_time

        # 4. Resumen final
        successful = len([r for r in results if r.get('success')])
        total_models = sum(r.get('summary', {}).get('models_generated', 0) for r in results)
        total_services = sum(r.get('summary', {}).get('services_generated', 0) for r in results)
        total_components = sum(r.get('summary', {}).get('components_generated', 0) for r in results)

        print("\n" + "="*70)
        print("MIGRACIÓN COMPLETADA")
        print("="*70)
        print(f"Duración: {duration}")
        print(f"Forms procesados: {len(results)}")
        print(f"Exitosos: {successful}")
        print(f"Fallidos: {len(results) - successful}")
        print(f"\nComponentes generados:")
        print(f"  - Modelos: {total_models}")
        print(f"  - Servicios: {total_services}")
        print(f"  - Componentes: {total_components}")
        print(f"\nDirectorio de salida: {self.angular_dir}")
        print(f"Reporte: {os.path.join(self.angular_dir, 'migration_report.html')}")
        print("="*70 + "\n")

        return {
            'success': True,
            'results': results,
            'duration': str(duration),
            'output_dir': self.angular_dir,
        }


def main():
    """Función principal"""
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python batch_migrate.py <archivo.zip>")
        print("  python batch_migrate.py <directorio>")
        print("  python batch_migrate.py <archivo.fmb>")
        sys.exit(1)

    source = sys.argv[1]

    if not os.path.exists(source):
        print(f"ERROR: No se encuentra: {source}")
        sys.exit(1)

    # Crear migrador
    migrator = BatchMigrator()

    # Ejecutar migración
    result = migrator.migrate(source)

    # Exit code
    sys.exit(0 if result.get('success') else 1)


if __name__ == '__main__':
    main()
