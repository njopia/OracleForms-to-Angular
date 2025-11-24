"""
Generador maestro que orquesta todo el proceso de migración de Oracle Forms a Angular
"""
import os
import json
from typing import Dict, List
from datetime import datetime

from xml_analyzer import FormsXMLAnalyzer
from generators.model_gen import ModelGenerator
from generators.service_gen import ServiceGenerator
from generators.component_gen import ComponentGenerator


class AngularGenerator:
    """Generador maestro para migración Oracle Forms -> Angular"""

    def __init__(self, output_dir: str):
        """
        Inicializa el generador maestro

        Args:
            output_dir: Directorio base de salida para archivos Angular
        """
        self.output_dir = output_dir
        self.model_generator = ModelGenerator(output_dir)
        self.service_generator = ServiceGenerator(output_dir)
        self.component_generator = ComponentGenerator(output_dir)

        # Crear estructura de directorios
        self._create_directory_structure()

    def _create_directory_structure(self):
        """Crea la estructura de directorios para el proyecto Angular"""
        directories = [
            'models',
            'services',
            'components',
            'modules',
        ]

        for directory in directories:
            dir_path = os.path.join(self.output_dir, directory)
            os.makedirs(dir_path, exist_ok=True)

    def generate_from_xml(self, xml_file: str) -> Dict:
        """
        Genera componentes Angular completos a partir de un archivo XML de Oracle Forms

        Args:
            xml_file: Ruta al archivo XML

        Returns:
            Diccionario con resultados de la generación
        """
        print(f"\n{'='*70}")
        print(f"Procesando: {os.path.basename(xml_file)}")
        print(f"{'='*70}\n")

        # 1. Analizar XML
        print("1. Analizando XML de Oracle Forms...")
        analyzer = FormsXMLAnalyzer(xml_file)
        structure = analyzer.parse()

        if 'error' in structure:
            return {
                'success': False,
                'error': structure['error'],
                'xml_file': xml_file,
            }

        form_name = structure.get('form_name', 'UNNAMED')
        data_blocks = structure.get('data_blocks', [])

        print(f"   ✓ Formulario: {form_name}")
        print(f"   ✓ Data Blocks encontrados: {len(data_blocks)}")
        print(f"   ✓ Canvases: {len(structure.get('canvases', []))}")
        print(f"   ✓ Windows: {len(structure.get('windows', []))}")
        print(f"   ✓ Triggers: {len(structure.get('triggers', []))}")
        print(f"   ✓ LOVs: {len(structure.get('lovs', []))}")
        print()

        # 2. Generar Modelos
        print("2. Generando modelos TypeScript...")
        models_results = self.model_generator.generate_multiple(data_blocks)
        successful_models = [r for r in models_results if r.get('success')]
        print(f"   ✓ Generados: {len(successful_models)}/{len(data_blocks)} modelos")
        for result in successful_models:
            print(f"     - {result['model_name']}")
        print()

        # 3. Generar Servicios
        print("3. Generando servicios Angular...")
        services_results = self.service_generator.generate_multiple(data_blocks)
        successful_services = [r for r in services_results if r.get('success')]
        print(f"   ✓ Generados: {len(successful_services)}/{len(data_blocks)} servicios")
        for result in successful_services:
            print(f"     - {result['service_name']}")
        print()

        # 4. Generar Componentes
        print("4. Generando componentes Angular...")
        components_results = self.component_generator.generate_multiple(data_blocks, structure)
        successful_components = [r for r in components_results if r.get('success')]
        print(f"   ✓ Generados: {len(successful_components)}/{len(data_blocks)} componentes")
        for result in successful_components:
            print(f"     - {result['component_name']}")
            print(f"       {len(result['files'])} archivos (.ts, .html, .css)")
        print()

        # 5. Guardar estructura analizada para referencia
        self._save_structure(structure, form_name)

        # Compilar resultados
        return {
            'success': True,
            'xml_file': xml_file,
            'form_name': form_name,
            'structure': structure,
            'models': models_results,
            'services': services_results,
            'components': components_results,
            'output_dir': self.output_dir,
            'summary': {
                'data_blocks': len(data_blocks),
                'models_generated': len(successful_models),
                'services_generated': len(successful_services),
                'components_generated': len(successful_components),
                'total_files': sum(len(c.get('files', [])) for c in successful_components)
                            + len(successful_models)
                            + len(successful_services),
            }
        }

    def generate_from_multiple_xmls(self, xml_files: List[str]) -> List[Dict]:
        """
        Genera componentes Angular para múltiples archivos XML

        Args:
            xml_files: Lista de rutas a archivos XML

        Returns:
            Lista de resultados de generación
        """
        results = []

        print(f"\n{'#'*70}")
        print(f"# INICIANDO MIGRACIÓN ORACLE FORMS → ANGULAR")
        print(f"# Archivos a procesar: {len(xml_files)}")
        print(f"{'#'*70}\n")

        for i, xml_file in enumerate(xml_files, 1):
            print(f"[{i}/{len(xml_files)}] {xml_file}")
            result = self.generate_from_xml(xml_file)
            results.append(result)

        return results

    def _save_structure(self, structure: Dict, form_name: str):
        """
        Guarda la estructura analizada como JSON para referencia

        Args:
            structure: Estructura analizada del formulario
            form_name: Nombre del formulario
        """
        analysis_dir = os.path.join(self.output_dir, 'analysis')
        os.makedirs(analysis_dir, exist_ok=True)

        file_path = os.path.join(analysis_dir, f'{form_name}_structure.json')

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(structure, f, indent=2, ensure_ascii=False)

        print(f"   ℹ Estructura guardada en: {file_path}")

    def generate_summary_report(self, results: List[Dict], output_file: str = None) -> str:
        """
        Genera un reporte resumen de la migración

        Args:
            results: Lista de resultados de generación
            output_file: Ruta del archivo de salida (opcional)

        Returns:
            Contenido del reporte en HTML
        """
        # Estadísticas totales
        total_forms = len(results)
        successful = len([r for r in results if r.get('success')])
        failed = total_forms - successful

        total_models = sum(r.get('summary', {}).get('models_generated', 0) for r in results)
        total_services = sum(r.get('summary', {}).get('services_generated', 0) for r in results)
        total_components = sum(r.get('summary', {}).get('components_generated', 0) for r in results)
        total_files = sum(r.get('summary', {}).get('total_files', 0) for r in results)

        # Generar HTML
        html = self._generate_html_report(
            results,
            total_forms,
            successful,
            failed,
            total_models,
            total_services,
            total_components,
            total_files
        )

        # Guardar archivo si se especificó
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html)
            print(f"\n{'='*70}")
            print(f"Reporte generado: {output_file}")
            print(f"{'='*70}\n")

        return html

    def _generate_html_report(
        self,
        results: List[Dict],
        total_forms: int,
        successful: int,
        failed: int,
        total_models: int,
        total_services: int,
        total_components: int,
        total_files: int
    ) -> str:
        """Genera el contenido HTML del reporte"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Oracle Forms to Angular - Migration Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            margin: 0;
            font-size: 2em;
        }}
        .header .timestamp {{
            opacity: 0.9;
            margin-top: 10px;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .summary-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .summary-card h3 {{
            margin: 0 0 10px 0;
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
        }}
        .summary-card .value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }}
        .details {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .form-item {{
            border-left: 4px solid #667eea;
            padding: 15px;
            margin-bottom: 20px;
            background: #f9f9f9;
            border-radius: 4px;
        }}
        .form-item.failed {{
            border-left-color: #e74c3c;
        }}
        .form-item h3 {{
            margin: 0 0 10px 0;
            color: #333;
        }}
        .form-item .info {{
            color: #666;
            font-size: 0.9em;
        }}
        .status-success {{
            color: #27ae60;
            font-weight: bold;
        }}
        .status-failed {{
            color: #e74c3c;
            font-weight: bold;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
        }}
        th, td {{
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f0f0f0;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Oracle Forms to Angular Migration Report</h1>
        <div class="timestamp">Generated: {timestamp}</div>
    </div>

    <div class="summary">
        <div class="summary-card">
            <h3>Total Forms</h3>
            <div class="value">{total_forms}</div>
        </div>
        <div class="summary-card">
            <h3>Successful</h3>
            <div class="value" style="color: #27ae60;">{successful}</div>
        </div>
        <div class="summary-card">
            <h3>Failed</h3>
            <div class="value" style="color: #e74c3c;">{failed}</div>
        </div>
        <div class="summary-card">
            <h3>Components Generated</h3>
            <div class="value">{total_components}</div>
        </div>
        <div class="summary-card">
            <h3>Services Generated</h3>
            <div class="value">{total_services}</div>
        </div>
        <div class="summary-card">
            <h3>Models Generated</h3>
            <div class="value">{total_models}</div>
        </div>
        <div class="summary-card">
            <h3>Total Files</h3>
            <div class="value">{total_files}</div>
        </div>
    </div>

    <div class="details">
        <h2>Migration Details</h2>
"""

        # Detalles de cada formulario
        for result in results:
            success = result.get('success', False)
            form_name = result.get('form_name', 'UNKNOWN')
            xml_file = result.get('xml_file', '')

            status_class = 'status-success' if success else 'status-failed'
            item_class = 'form-item' if success else 'form-item failed'

            html += f'        <div class="{item_class}">\n'
            html += f'            <h3>{form_name}</h3>\n'
            html += f'            <div class="info">File: {os.path.basename(xml_file)}</div>\n'
            html += f'            <div class="{status_class}">{"✓ SUCCESS" if success else "✗ FAILED"}</div>\n'

            if success:
                summary = result.get('summary', {})
                html += f"""
            <table>
                <tr>
                    <th>Data Blocks</th>
                    <td>{summary.get('data_blocks', 0)}</td>
                </tr>
                <tr>
                    <th>Models</th>
                    <td>{summary.get('models_generated', 0)}</td>
                </tr>
                <tr>
                    <th>Services</th>
                    <td>{summary.get('services_generated', 0)}</td>
                </tr>
                <tr>
                    <th>Components</th>
                    <td>{summary.get('components_generated', 0)}</td>
                </tr>
                <tr>
                    <th>Total Files</th>
                    <td>{summary.get('total_files', 0)}</td>
                </tr>
            </table>
"""
            else:
                error = result.get('error', 'Unknown error')
                html += f'            <div style="color: #e74c3c; margin-top: 10px;">Error: {error}</div>\n'

            html += '        </div>\n'

        html += """
    </div>
</body>
</html>
"""

        return html


if __name__ == '__main__':
    # Test básico
    import sys

    if len(sys.argv) > 1:
        xml_files = sys.argv[1:]
        output_dir = './angular_output'

        generator = AngularGenerator(output_dir)
        results = generator.generate_from_multiple_xmls(xml_files)

        # Generar reporte
        report_file = os.path.join(output_dir, 'migration_report.html')
        generator.generate_summary_report(results, report_file)

        # Resumen en consola
        print("\n" + "="*70)
        print("RESUMEN DE MIGRACIÓN")
        print("="*70)
        successful = len([r for r in results if r.get('success')])
        print(f"Total procesados: {len(results)}")
        print(f"Exitosos: {successful}")
        print(f"Fallidos: {len(results) - successful}")
        print(f"\nDirectorio de salida: {output_dir}")
        print(f"Reporte: {report_file}")
    else:
        print("Usage: python angular_generator.py <xml_file1> [xml_file2] ...")
