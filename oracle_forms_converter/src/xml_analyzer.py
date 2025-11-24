"""
Analizador de XML de Oracle Forms
Extrae información estructurada de archivos XML generados por frmf2xml.bat
"""
import xml.etree.ElementTree as ET
from typing import Dict, List, Optional
import os


class FormsXMLAnalyzer:
    """Analiza archivos XML de Oracle Forms y extrae estructura"""

    def __init__(self, xml_file: str):
        """
        Inicializa el analizador

        Args:
            xml_file: Ruta al archivo XML a analizar
        """
        self.xml_file = xml_file
        self.tree = None
        self.root = None
        self.form_name = os.path.splitext(os.path.basename(xml_file))[0]

    def parse(self) -> Dict:
        """
        Parsea el archivo XML y extrae toda la estructura

        Returns:
            Diccionario con la estructura completa del formulario
        """
        try:
            self.tree = ET.parse(self.xml_file)
            self.root = self.tree.getroot()

            return {
                'form_name': self.form_name,
                'xml_file': self.xml_file,
                'module_type': self._get_module_type(),
                'data_blocks': self._extract_data_blocks(),
                'canvases': self._extract_canvases(),
                'windows': self._extract_windows(),
                'triggers': self._extract_triggers(),
                'lovs': self._extract_lovs(),
                'record_groups': self._extract_record_groups(),
                'parameters': self._extract_parameters(),
                'program_units': self._extract_program_units(),
            }
        except ET.ParseError as e:
            return {
                'error': f'Error parsing XML: {str(e)}',
                'form_name': self.form_name,
                'xml_file': self.xml_file
            }
        except Exception as e:
            return {
                'error': f'Unexpected error: {str(e)}',
                'form_name': self.form_name,
                'xml_file': self.xml_file
            }

    def _get_module_type(self) -> str:
        """Obtiene el tipo de módulo (FormModule, MenuModule, ObjectLibrary, etc.)"""
        if self.root is not None:
            return self.root.tag
        return 'Unknown'

    def _extract_data_blocks(self) -> List[Dict]:
        """
        Extrae todos los Data Blocks del formulario

        Returns:
            Lista de diccionarios con información de cada Data Block
        """
        data_blocks = []

        if self.root is None:
            return data_blocks

        # Buscar todos los elementos Block o DataBlock
        for block in self.root.findall('.//Block') or self.root.findall('.//DataBlock'):
            block_info = {
                'name': block.get('Name', 'UNNAMED'),
                'query_data_source_name': block.findtext('QueryDataSourceName', ''),
                'query_data_source_type': block.findtext('QueryDataSourceType', ''),
                'database_table': block.findtext('DatabaseTable', ''),
                'items': self._extract_block_items(block),
                'triggers': self._extract_element_triggers(block),
                'relations': self._extract_block_relations(block),
            }
            data_blocks.append(block_info)

        return data_blocks

    def _extract_block_items(self, block) -> List[Dict]:
        """Extrae todos los items de un Data Block"""
        items = []

        for item in block.findall('.//Item'):
            item_info = {
                'name': item.get('Name', 'UNNAMED'),
                'item_type': item.findtext('ItemType', ''),
                'data_type': item.findtext('DataType', ''),
                'database_item': item.findtext('DatabaseItem', 'false'),
                'column_name': item.findtext('ColumnName', ''),
                'required': item.findtext('Required', 'false'),
                'max_length': item.findtext('MaximumLength', ''),
                'format_mask': item.findtext('FormatMask', ''),
                'default_value': item.findtext('DefaultValue', ''),
                'prompt': item.findtext('PromptText', ''),
                'canvas': item.findtext('Canvas', ''),
                'x_position': item.findtext('XPosition', ''),
                'y_position': item.findtext('YPosition', ''),
                'width': item.findtext('Width', ''),
                'height': item.findtext('Height', ''),
                'lov': item.findtext('ListOfValues', ''),
                'triggers': self._extract_element_triggers(item),
            }
            items.append(item_info)

        return items

    def _extract_block_relations(self, block) -> List[Dict]:
        """Extrae las relaciones de un Data Block"""
        relations = []

        for relation in block.findall('.//Relation'):
            relation_info = {
                'name': relation.get('Name', 'UNNAMED'),
                'detail_block': relation.findtext('DetailBlock', ''),
                'master_deletes': relation.findtext('MasterDeletes', ''),
                'join_condition': relation.findtext('JoinCondition', ''),
            }
            relations.append(relation_info)

        return relations

    def _extract_canvases(self) -> List[Dict]:
        """Extrae todos los Canvas del formulario"""
        canvases = []

        if self.root is None:
            return canvases

        for canvas in self.root.findall('.//Canvas'):
            canvas_info = {
                'name': canvas.get('Name', 'UNNAMED'),
                'canvas_type': canvas.findtext('CanvasType', ''),
                'window': canvas.findtext('Window', ''),
                'width': canvas.findtext('Width', ''),
                'height': canvas.findtext('Height', ''),
                'viewport_width': canvas.findtext('ViewportWidth', ''),
                'viewport_height': canvas.findtext('ViewportHeight', ''),
            }
            canvases.append(canvas_info)

        return canvases

    def _extract_windows(self) -> List[Dict]:
        """Extrae todas las Windows del formulario"""
        windows = []

        if self.root is None:
            return windows

        for window in self.root.findall('.//Window'):
            window_info = {
                'name': window.get('Name', 'UNNAMED'),
                'title': window.findtext('Title', ''),
                'width': window.findtext('Width', ''),
                'height': window.findtext('Height', ''),
                'x_position': window.findtext('XPosition', ''),
                'y_position': window.findtext('YPosition', ''),
                'modal': window.findtext('Modal', 'false'),
                'resizable': window.findtext('Resizable', 'true'),
                'minimize_allowed': window.findtext('MinimizeAllowed', 'true'),
                'maximize_allowed': window.findtext('MaximizeAllowed', 'true'),
            }
            windows.append(window_info)

        return windows

    def _extract_triggers(self) -> List[Dict]:
        """Extrae todos los triggers a nivel de formulario"""
        return self._extract_element_triggers(self.root)

    def _extract_element_triggers(self, element) -> List[Dict]:
        """Extrae triggers de un elemento específico"""
        triggers = []

        if element is None:
            return triggers

        for trigger in element.findall('.//Trigger'):
            trigger_info = {
                'name': trigger.get('Name', 'UNNAMED'),
                'trigger_text': trigger.findtext('TriggerText', ''),
                'execution_hierarchy': trigger.findtext('ExecutionHierarchy', ''),
                'fire_in_query': trigger.findtext('FireInQuery', ''),
            }
            triggers.append(trigger_info)

        return triggers

    def _extract_lovs(self) -> List[Dict]:
        """Extrae todas las List of Values (LOVs)"""
        lovs = []

        if self.root is None:
            return lovs

        for lov in self.root.findall('.//LOV'):
            lov_info = {
                'name': lov.get('Name', 'UNNAMED'),
                'record_group': lov.findtext('RecordGroup', ''),
                'title': lov.findtext('Title', ''),
                'width': lov.findtext('Width', ''),
                'height': lov.findtext('Height', ''),
                'column_mapping': self._extract_lov_column_mapping(lov),
            }
            lovs.append(lov_info)

        return lovs

    def _extract_lov_column_mapping(self, lov) -> List[Dict]:
        """Extrae el mapeo de columnas de un LOV"""
        mappings = []

        for mapping in lov.findall('.//ColumnMapping'):
            mapping_info = {
                'display_width': mapping.findtext('DisplayWidth', ''),
                'column_name': mapping.findtext('ColumnName', ''),
                'title': mapping.findtext('Title', ''),
            }
            mappings.append(mapping_info)

        return mappings

    def _extract_record_groups(self) -> List[Dict]:
        """Extrae todos los Record Groups"""
        record_groups = []

        if self.root is None:
            return record_groups

        for rg in self.root.findall('.//RecordGroup'):
            rg_info = {
                'name': rg.get('Name', 'UNNAMED'),
                'record_group_type': rg.findtext('RecordGroupType', ''),
                'query': rg.findtext('RecordGroupQuery', ''),
                'columns': self._extract_record_group_columns(rg),
            }
            record_groups.append(rg_info)

        return record_groups

    def _extract_record_group_columns(self, rg) -> List[Dict]:
        """Extrae las columnas de un Record Group"""
        columns = []

        for col in rg.findall('.//Column'):
            col_info = {
                'name': col.get('Name', 'UNNAMED'),
                'data_type': col.findtext('DataType', ''),
                'max_length': col.findtext('MaximumLength', ''),
            }
            columns.append(col_info)

        return columns

    def _extract_parameters(self) -> List[Dict]:
        """Extrae todos los parámetros del formulario"""
        parameters = []

        if self.root is None:
            return parameters

        for param in self.root.findall('.//Parameter'):
            param_info = {
                'name': param.get('Name', 'UNNAMED'),
                'parameter_data_type': param.findtext('ParameterDataType', ''),
                'initial_value': param.findtext('InitialValue', ''),
                'max_length': param.findtext('MaximumLength', ''),
            }
            parameters.append(param_info)

        return parameters

    def _extract_program_units(self) -> List[Dict]:
        """Extrae todas las unidades de programa (procedures, functions, packages)"""
        program_units = []

        if self.root is None:
            return program_units

        for pu in self.root.findall('.//ProgramUnit'):
            pu_info = {
                'name': pu.get('Name', 'UNNAMED'),
                'program_unit_type': pu.findtext('ProgramUnitType', ''),
                'program_unit_text': pu.findtext('ProgramUnitText', ''),
            }
            program_units.append(pu_info)

        return program_units


def analyze_xml_file(xml_file: str) -> Dict:
    """
    Función helper para analizar un archivo XML

    Args:
        xml_file: Ruta al archivo XML

    Returns:
        Diccionario con la estructura extraída
    """
    analyzer = FormsXMLAnalyzer(xml_file)
    return analyzer.parse()


if __name__ == '__main__':
    # Test básico
    import sys

    if len(sys.argv) > 1:
        xml_file = sys.argv[1]
        if os.path.exists(xml_file):
            result = analyze_xml_file(xml_file)

            print(f"Form: {result.get('form_name')}")
            print(f"Module Type: {result.get('module_type')}")
            print(f"\nData Blocks: {len(result.get('data_blocks', []))}")
            for block in result.get('data_blocks', []):
                print(f"  - {block['name']}: {len(block['items'])} items")

            print(f"\nCanvases: {len(result.get('canvases', []))}")
            print(f"Windows: {len(result.get('windows', []))}")
            print(f"Triggers: {len(result.get('triggers', []))}")
            print(f"LOVs: {len(result.get('lovs', []))}")
        else:
            print(f"File not found: {xml_file}")
    else:
        print("Usage: python xml_analyzer.py <xml_file>")
