"""
Generador de servicios Angular a partir de Data Blocks de Oracle Forms
"""
import os
from typing import Dict, List
from naming_convention import NamingConvention


class ServiceGenerator:
    """Genera servicios Angular con operaciones CRUD"""

    def __init__(self, output_dir: str):
        """
        Inicializa el generador de servicios

        Args:
            output_dir: Directorio de salida para los archivos generados
        """
        self.output_dir = output_dir
        self.naming = NamingConvention()

    def generate_from_datablock(self, datablock: Dict) -> Dict[str, str]:
        """
        Genera un servicio Angular a partir de un Data Block

        Args:
            datablock: Diccionario con información del Data Block

        Returns:
            Diccionario con información del archivo generado
        """
        block_name = datablock.get('name', 'UNNAMED')
        items = datablock.get('items', [])

        # Generar nombres según convenciones
        service_name = self.naming.to_service_name(block_name)
        model_name = self.naming.to_model_name(block_name)
        file_base = self.naming.to_service_file_base(block_name)
        file_name = f'{file_base}.ts'
        api_endpoint = self.naming.to_api_endpoint(block_name, plural=True)

        # Buscar campo ID (primary key)
        id_field = self._find_id_field(items)

        # Generar contenido del archivo
        content = self._generate_service_content(
            service_name,
            model_name,
            api_endpoint,
            id_field,
            datablock
        )

        # Preparar ruta completa
        services_dir = os.path.join(self.output_dir, 'services')
        os.makedirs(services_dir, exist_ok=True)
        file_path = os.path.join(services_dir, file_name)

        # Escribir archivo
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return {
            'service_name': service_name,
            'model_name': model_name,
            'file_name': file_name,
            'file_path': file_path,
            'block_name': block_name,
            'api_endpoint': api_endpoint,
        }

    def _find_id_field(self, items: List[Dict]) -> Dict:
        """
        Encuentra el campo ID (primary key) en la lista de items

        Args:
            items: Lista de items del Data Block

        Returns:
            Información del campo ID
        """
        # Buscar campos que terminen en _ID o ID
        for item in items:
            name = item.get('name', '').upper()
            if name.endswith('_ID') or name == 'ID':
                return {
                    'name': item.get('name'),
                    'property_name': self.naming.to_property_name(item.get('name')),
                    'data_type': item.get('data_type'),
                }

        # Si no se encuentra, usar el primer campo
        if items:
            first_item = items[0]
            return {
                'name': first_item.get('name'),
                'property_name': self.naming.to_property_name(first_item.get('name')),
                'data_type': first_item.get('data_type'),
            }

        return {
            'name': 'id',
            'property_name': 'id',
            'data_type': 'NUMBER',
        }

    def _generate_service_content(
        self,
        service_name: str,
        model_name: str,
        api_endpoint: str,
        id_field: Dict,
        datablock: Dict
    ) -> str:
        """
        Genera el contenido del servicio Angular

        Args:
            service_name: Nombre del servicio
            model_name: Nombre del modelo
            api_endpoint: Endpoint de API
            id_field: Información del campo ID
            datablock: Información del Data Block

        Returns:
            Contenido del archivo TypeScript
        """
        block_name = datablock.get('name', 'UNNAMED')
        table_name = datablock.get('database_table', '')
        id_property = id_field.get('property_name', 'id')

        # Generar imports relativos
        model_file_base = self.naming.to_model_file_base(datablock.get('name'))

        lines = []

        # Imports
        lines.append("import { Injectable } from '@angular/core';")
        lines.append("import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';")
        lines.append("import { Observable, throwError } from 'rxjs';")
        lines.append("import { catchError, map } from 'rxjs/operators';")
        lines.append(f"import {{ {model_name} }} from '../models/{model_file_base}';")
        lines.append('')

        # Comentario de encabezado
        lines.append('/**')
        lines.append(f' * Servicio generado desde Oracle Forms Data Block: {block_name}')
        if table_name:
            lines.append(f' * Tabla de base de datos: {table_name}')
        lines.append(f' * Proporciona operaciones CRUD para {model_name}')
        lines.append(' * Generado automáticamente - ajustar según necesidades')
        lines.append(' */')
        lines.append("@Injectable({")
        lines.append("  providedIn: 'root'")
        lines.append("})")
        lines.append(f'export class {service_name} {{')
        lines.append(f"  private apiUrl = '{api_endpoint}';")
        lines.append('')
        lines.append('  private httpOptions = {')
        lines.append('    headers: new HttpHeaders({')
        lines.append("      'Content-Type': 'application/json'")
        lines.append('    })')
        lines.append('  };')
        lines.append('')

        # Constructor
        lines.append('  constructor(private http: HttpClient) { }')
        lines.append('')

        # Método getAll()
        lines.append('  /**')
        lines.append(f'   * Obtiene todos los registros de {model_name}')
        lines.append(f'   * @returns Observable<{model_name}[]>')
        lines.append('   */')
        lines.append(f'  getAll(): Observable<{model_name}[]> {{')
        lines.append(f'    return this.http.get<{model_name}[]>(this.apiUrl)')
        lines.append('      .pipe(')
        lines.append(f"        catchError(this.handleError<{model_name}[]>('getAll', []))")
        lines.append('      );')
        lines.append('  }')
        lines.append('')

        # Método getById()
        lines.append('  /**')
        lines.append(f'   * Obtiene un registro de {model_name} por ID')
        lines.append(f'   * @param id - ID del registro')
        lines.append(f'   * @returns Observable<{model_name}>')
        lines.append('   */')
        lines.append(f'  getById(id: number | string): Observable<{model_name}> {{')
        lines.append(f'    const url = `${{this.apiUrl}}/${{id}}`;')
        lines.append(f'    return this.http.get<{model_name}>(url)')
        lines.append('      .pipe(')
        lines.append(f"        catchError(this.handleError<{model_name}>('getById'))")
        lines.append('      );')
        lines.append('  }')
        lines.append('')

        # Método create()
        lines.append('  /**')
        lines.append(f'   * Crea un nuevo registro de {model_name}')
        lines.append(f'   * @param entity - Datos del nuevo {model_name}')
        lines.append(f'   * @returns Observable<{model_name}>')
        lines.append('   */')
        lines.append(f'  create(entity: {model_name}): Observable<{model_name}> {{')
        lines.append(f'    return this.http.post<{model_name}>(this.apiUrl, entity, this.httpOptions)')
        lines.append('      .pipe(')
        lines.append(f"        catchError(this.handleError<{model_name}>('create'))")
        lines.append('      );')
        lines.append('  }')
        lines.append('')

        # Método update()
        lines.append('  /**')
        lines.append(f'   * Actualiza un registro de {model_name}')
        lines.append(f'   * @param id - ID del registro')
        lines.append(f'   * @param entity - Datos actualizados')
        lines.append(f'   * @returns Observable<{model_name}>')
        lines.append('   */')
        lines.append(f'  update(id: number | string, entity: {model_name}): Observable<{model_name}> {{')
        lines.append(f'    const url = `${{this.apiUrl}}/${{id}}`;')
        lines.append(f'    return this.http.put<{model_name}>(url, entity, this.httpOptions)')
        lines.append('      .pipe(')
        lines.append(f"        catchError(this.handleError<{model_name}>('update'))")
        lines.append('      );')
        lines.append('  }')
        lines.append('')

        # Método delete()
        lines.append('  /**')
        lines.append(f'   * Elimina un registro de {model_name}')
        lines.append(f'   * @param id - ID del registro')
        lines.append('   * @returns Observable<void>')
        lines.append('   */')
        lines.append('  delete(id: number | string): Observable<void> {')
        lines.append(f'    const url = `${{this.apiUrl}}/${{id}}`;')
        lines.append('    return this.http.delete<void>(url, this.httpOptions)')
        lines.append('      .pipe(')
        lines.append("        catchError(this.handleError<void>('delete'))")
        lines.append('      );')
        lines.append('  }')
        lines.append('')

        # Método search()
        lines.append('  /**')
        lines.append(f'   * Busca registros de {model_name} con filtros')
        lines.append(f'   * @param filters - Objeto con criterios de búsqueda')
        lines.append(f'   * @returns Observable<{model_name}[]>')
        lines.append('   */')
        lines.append(f'  search(filters: any): Observable<{model_name}[]> {{')
        lines.append('    let params = new HttpParams();')
        lines.append('    Object.keys(filters).forEach(key => {')
        lines.append('      if (filters[key] !== null && filters[key] !== undefined) {')
        lines.append('        params = params.set(key, filters[key].toString());')
        lines.append('      }')
        lines.append('    });')
        lines.append('')
        lines.append(f'    return this.http.get<{model_name}[]>(this.apiUrl, {{ params }})')
        lines.append('      .pipe(')
        lines.append(f"        catchError(this.handleError<{model_name}[]>('search', []))")
        lines.append('      );')
        lines.append('  }')
        lines.append('')

        # Método handleError()
        lines.append('  /**')
        lines.append('   * Maneja errores HTTP')
        lines.append('   * @param operation - Nombre de la operación que falló')
        lines.append('   * @param result - Valor opcional a retornar como Observable')
        lines.append('   */')
        lines.append('  private handleError<T>(operation = \'operation\', result?: T) {')
        lines.append('    return (error: any): Observable<T> => {')
        lines.append('      console.error(`${operation} failed:`, error);')
        lines.append('')
        lines.append('      // TODO: Implementar manejo de errores más sofisticado')
        lines.append('      // (logging remoto, notificaciones al usuario, etc.)')
        lines.append('')
        lines.append('      // Retornar resultado vacío para mantener la app funcionando')
        lines.append('      return throwError(() => error);')
        lines.append('    };')
        lines.append('  }')
        lines.append('}')
        lines.append('')

        return '\n'.join(lines)

    def generate_multiple(self, datablocks: List[Dict]) -> List[Dict]:
        """
        Genera múltiples servicios a partir de una lista de Data Blocks

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
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            structure = json.load(f)

        output_dir = sys.argv[2] if len(sys.argv) > 2 else './test_output'

        generator = ServiceGenerator(output_dir)
        datablocks = structure.get('data_blocks', [])

        print(f"Generating {len(datablocks)} services...")
        results = generator.generate_multiple(datablocks)

        for result in results:
            if result.get('success'):
                print(f"  ✓ {result['service_name']} -> {result['file_path']}")
            else:
                print(f"  ✗ {result['block_name']}: {result['error']}")
    else:
        print("Usage: python service_gen.py <structure.json> [output_dir]")
