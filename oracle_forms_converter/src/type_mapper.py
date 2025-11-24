"""
Mapeador de tipos de datos de Oracle a TypeScript/Angular
"""
from typing import Dict, Tuple


class TypeMapper:
    """Mapea tipos de datos de Oracle Forms a TypeScript"""

    # Mapeo de tipos de Oracle a TypeScript
    ORACLE_TO_TYPESCRIPT: Dict[str, str] = {
        # String types
        'VARCHAR2': 'string',
        'CHAR': 'string',
        'NCHAR': 'string',
        'NVARCHAR2': 'string',
        'CLOB': 'string',
        'NCLOB': 'string',
        'LONG': 'string',
        'RAW': 'string',
        'LONG RAW': 'string',

        # Numeric types
        'NUMBER': 'number',
        'INTEGER': 'number',
        'INT': 'number',
        'SMALLINT': 'number',
        'FLOAT': 'number',
        'REAL': 'number',
        'DOUBLE PRECISION': 'number',
        'BINARY_INTEGER': 'number',
        'BINARY_FLOAT': 'number',
        'BINARY_DOUBLE': 'number',

        # Date/Time types
        'DATE': 'Date',
        'TIMESTAMP': 'Date',
        'TIMESTAMP WITH TIME ZONE': 'Date',
        'TIMESTAMP WITH LOCAL TIME ZONE': 'Date',

        # Binary types
        'BLOB': 'Blob',
        'BFILE': 'Blob',

        # Boolean
        'BOOLEAN': 'boolean',

        # Special types
        'ROWID': 'string',
        'UROWID': 'string',
    }

    # Mapeo de tipos de Oracle a tipos de validación Angular
    ORACLE_TO_VALIDATORS: Dict[str, list] = {
        'VARCHAR2': ['Validators.maxLength'],
        'CHAR': ['Validators.maxLength'],
        'NUMBER': ['Validators.pattern(/^-?\\d*\\.?\\d+$/)'],
        'INTEGER': ['Validators.pattern(/^-?\\d+$/)'],
        'DATE': [],
        'TIMESTAMP': [],
    }

    # Mapeo de tipos de Item de Oracle Forms a controles Angular
    ITEM_TYPE_TO_CONTROL: Dict[str, str] = {
        'TEXT_ITEM': 'input',
        'DISPLAY_ITEM': 'input',
        'LIST_ITEM': 'select',
        'CHECKBOX': 'checkbox',
        'RADIO_GROUP': 'radio',
        'RADIO_BUTTON': 'radio',
        'BUTTON': 'button',
        'IMAGE': 'image',
        'TEXT_AREA': 'textarea',
        'EDITOR': 'textarea',
    }

    # Mapeo de tipos de Item a tipos de input HTML
    ITEM_TYPE_TO_INPUT_TYPE: Dict[str, str] = {
        'TEXT_ITEM': 'text',
        'DISPLAY_ITEM': 'text',
        'NUMBER': 'number',
        'DATE': 'date',
        'TIMESTAMP': 'datetime-local',
    }

    @staticmethod
    def to_typescript(oracle_type: str) -> str:
        """
        Convierte un tipo de Oracle a TypeScript

        Args:
            oracle_type: Tipo de dato de Oracle

        Returns:
            Tipo de dato TypeScript equivalente
        """
        if not oracle_type:
            return 'any'

        oracle_type_upper = oracle_type.upper().strip()

        # Manejo de NUMBER con precisión: NUMBER(10,2)
        if oracle_type_upper.startswith('NUMBER'):
            return 'number'

        # Manejo de VARCHAR2 con tamaño: VARCHAR2(100)
        if oracle_type_upper.startswith('VARCHAR2') or oracle_type_upper.startswith('CHAR'):
            return 'string'

        return TypeMapper.ORACLE_TO_TYPESCRIPT.get(oracle_type_upper, 'any')

    @staticmethod
    def to_typescript_with_nullable(oracle_type: str, required: bool = False) -> str:
        """
        Convierte un tipo de Oracle a TypeScript con soporte para nullable

        Args:
            oracle_type: Tipo de dato de Oracle
            required: Si el campo es requerido

        Returns:
            Tipo de dato TypeScript con | null si no es requerido
        """
        ts_type = TypeMapper.to_typescript(oracle_type)

        if not required:
            return f'{ts_type} | null'

        return ts_type

    @staticmethod
    def get_validators(oracle_type: str, required: bool = False, max_length: str = '') -> list:
        """
        Obtiene los validadores de Angular para un tipo de dato

        Args:
            oracle_type: Tipo de dato de Oracle
            required: Si el campo es requerido
            max_length: Longitud máxima del campo

        Returns:
            Lista de validadores Angular
        """
        validators = []

        if required:
            validators.append('Validators.required')

        if not oracle_type:
            return validators

        oracle_type_upper = oracle_type.upper().strip()

        # Validadores específicos por tipo
        if oracle_type_upper.startswith('VARCHAR2') or oracle_type_upper.startswith('CHAR'):
            if max_length and max_length.isdigit():
                validators.append(f'Validators.maxLength({max_length})')
        elif oracle_type_upper.startswith('NUMBER'):
            validators.append('Validators.pattern(/^-?\\\\d*\\\\.?\\\\d+$/)')
        elif 'INTEGER' in oracle_type_upper or 'INT' in oracle_type_upper:
            validators.append('Validators.pattern(/^-?\\\\d+$/)')

        return validators

    @staticmethod
    def get_html_control_type(item_type: str, data_type: str = '') -> Tuple[str, str]:
        """
        Obtiene el tipo de control HTML y el tipo de input

        Args:
            item_type: Tipo de item de Oracle Forms
            data_type: Tipo de dato

        Returns:
            Tupla (control_type, input_type)
        """
        if not item_type:
            item_type = 'TEXT_ITEM'

        item_type_upper = item_type.upper().strip()

        control_type = TypeMapper.ITEM_TYPE_TO_CONTROL.get(
            item_type_upper,
            'input'
        )

        # Determinar tipo de input basado en el tipo de dato
        input_type = 'text'

        if data_type:
            data_type_upper = data_type.upper().strip()

            if 'NUMBER' in data_type_upper or 'INTEGER' in data_type_upper:
                input_type = 'number'
            elif 'DATE' in data_type_upper:
                if 'TIMESTAMP' in data_type_upper:
                    input_type = 'datetime-local'
                else:
                    input_type = 'date'

        # Override por tipo de item
        if item_type_upper in TypeMapper.ITEM_TYPE_TO_INPUT_TYPE:
            input_type = TypeMapper.ITEM_TYPE_TO_INPUT_TYPE[item_type_upper]

        return control_type, input_type

    @staticmethod
    def get_default_value(data_type: str) -> str:
        """
        Obtiene el valor por defecto para un tipo de dato en TypeScript

        Args:
            data_type: Tipo de dato de Oracle

        Returns:
            Valor por defecto como string
        """
        if not data_type:
            return 'null'

        ts_type = TypeMapper.to_typescript(data_type)

        defaults = {
            'string': "''",
            'number': '0',
            'boolean': 'false',
            'Date': 'new Date()',
            'any': 'null',
        }

        return defaults.get(ts_type, 'null')


if __name__ == '__main__':
    # Tests básicos
    print("=== Type Mapper Tests ===\n")

    test_types = [
        ('VARCHAR2', False, '100'),
        ('NUMBER', True, ''),
        ('DATE', False, ''),
        ('CHAR(50)', True, '50'),
        ('INTEGER', True, ''),
    ]

    for oracle_type, required, max_len in test_types:
        ts_type = TypeMapper.to_typescript(oracle_type)
        ts_nullable = TypeMapper.to_typescript_with_nullable(oracle_type, required)
        validators = TypeMapper.get_validators(oracle_type, required, max_len)
        default = TypeMapper.get_default_value(oracle_type)

        print(f"Oracle Type: {oracle_type}")
        print(f"  TypeScript: {ts_type}")
        print(f"  With Nullable: {ts_nullable}")
        print(f"  Validators: {validators}")
        print(f"  Default: {default}")
        print()
