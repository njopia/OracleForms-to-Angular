"""
Generador de modelos TypeScript/Interfaces a partir de Data Blocks de Oracle Forms
"""
import os
from typing import Dict, List
from naming_convention import NamingConvention
from type_mapper import TypeMapper


class ModelGenerator:
    """Genera interfaces TypeScript a partir de Data Blocks"""

    def __init__(self, output_dir: str):
        """
        Inicializa el generador de modelos

        Args:
            output_dir: Directorio de salida para los archivos generados
        """
        self.output_dir = output_dir
        self.naming = NamingConvention()
        self.type_mapper = TypeMapper()

    def generate_from_datablock(self, datablock: Dict) -> Dict[str, str]:
        """
        Genera una interfaz TypeScript a partir de un Data Block

        Args:
            datablock: Diccionario con información del Data Block

        Returns:
            Diccionario con información del archivo generado
        """
        block_name = datablock.get('name', 'UNNAMED')
        items = datablock.get('items', [])

        # Generar nombres según convenciones
        model_name = self.naming.to_model_name(block_name)
        file_base = self.naming.to_model_file_base(block_name)
        file_name = f'{file_base}.ts'

        # Generar contenido del archivo
        content = self._generate_interface_content(model_name, items, datablock)

        # Preparar ruta completa
        models_dir = os.path.join(self.output_dir, 'models')
        os.makedirs(models_dir, exist_ok=True)
        file_path = os.path.join(models_dir, file_name)

        # Escribir archivo
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return {
            'model_name': model_name,
            'file_name': file_name,
            'file_path': file_path,
            'block_name': block_name,
        }

    def _generate_interface_content(
        self,
        model_name: str,
        items: List[Dict],
        datablock: Dict
    ) -> str:
        """
        Genera el contenido de la interfaz TypeScript

        Args:
            model_name: Nombre de la interfaz
            items: Lista de items del Data Block
            datablock: Información del Data Block

        Returns:
            Contenido del archivo TypeScript
        """
        lines = []

        # Comentario de encabezado
        block_name = datablock.get('name', 'UNNAMED')
        table_name = datablock.get('database_table', '')

        lines.append(f'/**')
        lines.append(f' * Modelo generado desde Oracle Forms Data Block: {block_name}')
        if table_name:
            lines.append(f' * Tabla de base de datos: {table_name}')
        lines.append(f' * Generado automáticamente - no editar manualmente')
        lines.append(f' */')
        lines.append(f'export interface {model_name} {{')

        # Generar propiedades
        for item in items:
            item_name = item.get('name', 'UNNAMED')
            data_type = item.get('data_type', '')
            required = item.get('required', 'false').lower() == 'true'
            column_name = item.get('column_name', '')
            prompt = item.get('prompt', '')

            # Generar nombre de propiedad
            property_name = self.naming.to_property_name(item_name)

            # Convertir tipo
            ts_type = self.type_mapper.to_typescript_with_nullable(data_type, required)

            # Comentario con información adicional
            comment_parts = []
            if prompt:
                comment_parts.append(prompt)
            if column_name:
                comment_parts.append(f'DB Column: {column_name}')
            if data_type:
                comment_parts.append(f'Oracle Type: {data_type}')

            if comment_parts:
                lines.append(f'  /** {" | ".join(comment_parts)} */')

            # Generar propiedad
            optional_marker = '' if required else '?'
            lines.append(f'  {property_name}{optional_marker}: {ts_type};')
            lines.append('')

        lines.append('}')
        lines.append('')

        return '\n'.join(lines)

    def generate_multiple(self, datablocks: List[Dict]) -> List[Dict]:
        """
        Genera múltiples modelos a partir de una lista de Data Blocks

        Args:
            datablocks: Lista de Data Blocks

        Returns:
            Lista de resultados de generación
        """
        results = []

        for datablock in datablocks:
            try:
                result = self.generate_from_datablock(datablock)
                result['success'] = True
                results.append(result)
            except Exception as e:
                results.append({
                    'success': False,
                    'error': str(e),
                    'block_name': datablock.get('name', 'UNNAMED'),
                })

        return results


if __name__ == '__main__':
    # Test básico
    import sys
    import json

    if len(sys.argv) > 1:
        # Leer estructura de prueba desde JSON
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            structure = json.load(f)

        output_dir = sys.argv[2] if len(sys.argv) > 2 else './test_output'

        generator = ModelGenerator(output_dir)
        datablocks = structure.get('data_blocks', [])

        print(f"Generating {len(datablocks)} models...")
        results = generator.generate_multiple(datablocks)

        for result in results:
            if result.get('success'):
                print(f"  ✓ {result['model_name']} -> {result['file_path']}")
            else:
                print(f"  ✗ {result['block_name']}: {result['error']}")
    else:
        print("Usage: python model_gen.py <structure.json> [output_dir]")
