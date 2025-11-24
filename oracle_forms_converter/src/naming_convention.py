"""
Sistema de convenciones de nombres para convertir nombres de Oracle Forms a Angular
"""
import re
from typing import List


class NamingConvention:
    """Convierte nombres de Oracle Forms a convenciones de Angular/TypeScript"""

    @staticmethod
    def to_pascal_case(name: str) -> str:
        """
        Convierte a PascalCase
        CUSTOMER_MASTER -> CustomerMaster
        customer_master -> CustomerMaster
        customerMaster -> CustomerMaster

        Args:
            name: Nombre a convertir

        Returns:
            Nombre en PascalCase
        """
        if not name:
            return ''

        # Limpiar caracteres especiales excepto guiones bajos
        name = re.sub(r'[^a-zA-Z0-9_]', '_', name)

        # Dividir por guiones bajos o cambios de mayúsculas
        words = re.split(r'[_\s]+', name)

        # Capitalizar cada palabra
        pascal = ''.join(word.capitalize() for word in words if word)

        return pascal

    @staticmethod
    def to_camel_case(name: str) -> str:
        """
        Convierte a camelCase
        CUSTOMER_ID -> customerId
        customer_id -> customerId
        CustomerID -> customerId

        Args:
            name: Nombre a convertir

        Returns:
            Nombre en camelCase
        """
        pascal = NamingConvention.to_pascal_case(name)

        if not pascal:
            return ''

        # Primera letra en minúscula
        return pascal[0].lower() + pascal[1:] if len(pascal) > 1 else pascal.lower()

    @staticmethod
    def to_kebab_case(name: str) -> str:
        """
        Convierte a kebab-case
        CUSTOMER_MASTER -> customer-master
        CustomerMaster -> customer-master

        Args:
            name: Nombre a convertir

        Returns:
            Nombre en kebab-case
        """
        if not name:
            return ''

        # Limpiar caracteres especiales
        name = re.sub(r'[^a-zA-Z0-9_]', '_', name)

        # Insertar guiones antes de mayúsculas
        name = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', name)

        # Reemplazar guiones bajos y espacios por guiones
        name = re.sub(r'[_\s]+', '-', name)

        # Convertir a minúsculas
        return name.lower()

    @staticmethod
    def to_snake_case(name: str) -> str:
        """
        Convierte a snake_case
        CustomerMaster -> customer_master
        CUSTOMER_MASTER -> customer_master

        Args:
            name: Nombre a convertir

        Returns:
            Nombre en snake_case
        """
        if not name:
            return ''

        # Insertar guiones bajos antes de mayúsculas
        name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)

        # Reemplazar guiones y espacios por guiones bajos
        name = re.sub(r'[-\s]+', '_', name)

        # Convertir a minúsculas
        return name.lower()

    @staticmethod
    def to_singular(name: str) -> str:
        """
        Convierte nombre plural a singular (simplificado)
        CUSTOMERS -> CUSTOMER
        Orders -> Order

        Args:
            name: Nombre a convertir

        Returns:
            Nombre en singular
        """
        if not name:
            return ''

        # Reglas simples de pluralización
        if name.upper().endswith('IES'):
            # CATEGORIES -> CATEGORY
            return name[:-3] + 'Y'
        elif name.upper().endswith('SES'):
            # ADDRESSES -> ADDRESS
            return name[:-2]
        elif name.upper().endswith('S') and not name.upper().endswith('SS'):
            # CUSTOMERS -> CUSTOMER, pero no ADDRESS -> ADDRES
            return name[:-1]

        return name

    @staticmethod
    def to_plural(name: str) -> str:
        """
        Convierte nombre singular a plural (simplificado)
        CUSTOMER -> CUSTOMERS
        Category -> Categories

        Args:
            name: Nombre a convertir

        Returns:
            Nombre en plural
        """
        if not name:
            return ''

        # Reglas simples de pluralización
        if name.upper().endswith('Y') and len(name) > 1 and name[-2].lower() not in 'aeiou':
            # CATEGORY -> CATEGORIES
            return name[:-1] + 'ies'
        elif name.upper().endswith('S') or name.upper().endswith('X') or name.upper().endswith('Z'):
            # ADDRESS -> ADDRESSES
            return name + 'es'
        else:
            # CUSTOMER -> CUSTOMERS
            return name + 's'

    @staticmethod
    def to_component_name(forms_name: str) -> str:
        """
        Genera nombre de componente Angular
        CUSTOMER_MASTER -> CustomerMasterComponent

        Args:
            forms_name: Nombre del formulario

        Returns:
            Nombre del componente
        """
        pascal = NamingConvention.to_pascal_case(forms_name)
        return f'{pascal}Component'

    @staticmethod
    def to_component_selector(forms_name: str, prefix: str = 'app') -> str:
        """
        Genera selector de componente Angular
        CUSTOMER_MASTER -> app-customer-master

        Args:
            forms_name: Nombre del formulario
            prefix: Prefijo del selector (default: 'app')

        Returns:
            Selector del componente
        """
        kebab = NamingConvention.to_kebab_case(forms_name)
        return f'{prefix}-{kebab}'

    @staticmethod
    def to_component_file_base(forms_name: str) -> str:
        """
        Genera nombre base de archivos de componente
        CUSTOMER_MASTER -> customer-master.component

        Args:
            forms_name: Nombre del formulario

        Returns:
            Nombre base de archivos
        """
        kebab = NamingConvention.to_kebab_case(forms_name)
        return f'{kebab}.component'

    @staticmethod
    def to_service_name(forms_name: str) -> str:
        """
        Genera nombre de servicio Angular
        CUSTOMERS -> CustomerService

        Args:
            forms_name: Nombre del bloque de datos

        Returns:
            Nombre del servicio
        """
        singular = NamingConvention.to_singular(forms_name)
        pascal = NamingConvention.to_pascal_case(singular)
        return f'{pascal}Service'

    @staticmethod
    def to_service_file_base(forms_name: str) -> str:
        """
        Genera nombre base de archivo de servicio
        CUSTOMERS -> customer.service

        Args:
            forms_name: Nombre del bloque de datos

        Returns:
            Nombre base de archivo
        """
        singular = NamingConvention.to_singular(forms_name)
        kebab = NamingConvention.to_kebab_case(singular)
        return f'{kebab}.service'

    @staticmethod
    def to_model_name(forms_name: str) -> str:
        """
        Genera nombre de interfaz/modelo TypeScript
        CUSTOMERS -> Customer

        Args:
            forms_name: Nombre del bloque de datos

        Returns:
            Nombre del modelo
        """
        singular = NamingConvention.to_singular(forms_name)
        return NamingConvention.to_pascal_case(singular)

    @staticmethod
    def to_model_file_base(forms_name: str) -> str:
        """
        Genera nombre base de archivo de modelo
        CUSTOMERS -> customer.model

        Args:
            forms_name: Nombre del bloque de datos

        Returns:
            Nombre base de archivo
        """
        singular = NamingConvention.to_singular(forms_name)
        kebab = NamingConvention.to_kebab_case(singular)
        return f'{kebab}.model'

    @staticmethod
    def to_module_name(forms_name: str) -> str:
        """
        Genera nombre de módulo Angular
        CUSTOMER_MANAGEMENT -> CustomerManagementModule

        Args:
            forms_name: Nombre del módulo

        Returns:
            Nombre del módulo
        """
        pascal = NamingConvention.to_pascal_case(forms_name)
        return f'{pascal}Module'

    @staticmethod
    def to_module_file_base(forms_name: str) -> str:
        """
        Genera nombre base de archivo de módulo
        CUSTOMER_MANAGEMENT -> customer-management.module

        Args:
            forms_name: Nombre del módulo

        Returns:
            Nombre base de archivo
        """
        kebab = NamingConvention.to_kebab_case(forms_name)
        return f'{kebab}.module'

    @staticmethod
    def to_property_name(item_name: str) -> str:
        """
        Genera nombre de propiedad TypeScript
        CUSTOMER_ID -> customerId
        FIRST_NAME -> firstName

        Args:
            item_name: Nombre del item

        Returns:
            Nombre de propiedad en camelCase
        """
        return NamingConvention.to_camel_case(item_name)

    @staticmethod
    def to_api_endpoint(entity_name: str, plural: bool = True) -> str:
        """
        Genera endpoint de API REST
        CUSTOMER -> /api/customers o /api/customer

        Args:
            entity_name: Nombre de la entidad
            plural: Si debe ser plural

        Returns:
            Endpoint de API
        """
        singular = NamingConvention.to_singular(entity_name)
        kebab = NamingConvention.to_kebab_case(singular)

        if plural:
            plural_kebab = NamingConvention.to_kebab_case(
                NamingConvention.to_plural(singular)
            )
            return f'/api/{plural_kebab}'

        return f'/api/{kebab}'


if __name__ == '__main__':
    # Tests básicos
    print("=== Naming Convention Tests ===\n")

    test_names = [
        'CUSTOMER_MASTER',
        'CUSTOMERS',
        'ORDER_DETAILS',
        'INVOICE',
        'employee_form',
    ]

    for name in test_names:
        print(f"Original: {name}")
        print(f"  PascalCase: {NamingConvention.to_pascal_case(name)}")
        print(f"  camelCase: {NamingConvention.to_camel_case(name)}")
        print(f"  kebab-case: {NamingConvention.to_kebab_case(name)}")
        print(f"  snake_case: {NamingConvention.to_snake_case(name)}")
        print(f"  Singular: {NamingConvention.to_singular(name)}")
        print(f"  Component: {NamingConvention.to_component_name(name)}")
        print(f"  Selector: {NamingConvention.to_component_selector(name)}")
        print(f"  Service: {NamingConvention.to_service_name(name)}")
        print(f"  Model: {NamingConvention.to_model_name(name)}")
        print(f"  API Endpoint: {NamingConvention.to_api_endpoint(name)}")
        print()
