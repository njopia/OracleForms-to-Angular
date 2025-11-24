"""
Generador de componentes Angular a partir de Data Blocks y Canvases de Oracle Forms
"""
import os
from typing import Dict, List
from naming_convention import NamingConvention
from type_mapper import TypeMapper


class ComponentGenerator:
    """Genera componentes Angular completos (.ts, .html, .css)"""

    def __init__(self, output_dir: str):
        """
        Inicializa el generador de componentes

        Args:
            output_dir: Directorio de salida para los archivos generados
        """
        self.output_dir = output_dir
        self.naming = NamingConvention()
        self.type_mapper = TypeMapper()

    def generate_from_datablock(self, datablock: Dict, form_info: Dict = None) -> Dict[str, any]:
        """
        Genera un componente Angular a partir de un Data Block

        Args:
            datablock: Diccionario con información del Data Block
            form_info: Información adicional del formulario

        Returns:
            Diccionario con información de los archivos generados
        """
        block_name = datablock.get('name', 'UNNAMED')
        items = datablock.get('items', [])

        # Generar nombres según convenciones
        component_name = self.naming.to_component_name(block_name)
        selector = self.naming.to_component_selector(block_name)
        file_base = self.naming.to_component_file_base(block_name)
        model_name = self.naming.to_model_name(block_name)
        service_name = self.naming.to_service_name(block_name)

        # Preparar directorio del componente
        component_dir = os.path.join(
            self.output_dir,
            'components',
            self.naming.to_kebab_case(block_name)
        )
        os.makedirs(component_dir, exist_ok=True)

        # Generar archivos
        files_generated = []

        # 1. TypeScript Component
        ts_content = self._generate_typescript_content(
            component_name,
            selector,
            file_base,
            model_name,
            service_name,
            items,
            datablock
        )
        ts_file = os.path.join(component_dir, f'{file_base}.ts')
        with open(ts_file, 'w', encoding='utf-8') as f:
            f.write(ts_content)
        files_generated.append(ts_file)

        # 2. HTML Template
        html_content = self._generate_html_content(
            model_name,
            items,
            datablock
        )
        html_file = os.path.join(component_dir, f'{file_base}.html')
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        files_generated.append(html_file)

        # 3. CSS Styles
        css_content = self._generate_css_content()
        css_file = os.path.join(component_dir, f'{file_base}.css')
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(css_content)
        files_generated.append(css_file)

        return {
            'component_name': component_name,
            'selector': selector,
            'files': files_generated,
            'component_dir': component_dir,
            'block_name': block_name,
        }

    def _generate_typescript_content(
        self,
        component_name: str,
        selector: str,
        file_base: str,
        model_name: str,
        service_name: str,
        items: List[Dict],
        datablock: Dict
    ) -> str:
        """Genera el contenido TypeScript del componente"""
        block_name = datablock.get('name', 'UNNAMED')
        model_file_base = self.naming.to_model_file_base(datablock.get('name'))
        service_file_base = self.naming.to_service_file_base(datablock.get('name'))

        lines = []

        # Imports
        lines.append("import { Component, OnInit } from '@angular/core';")
        lines.append("import { FormBuilder, FormGroup, Validators } from '@angular/forms';")
        lines.append(f"import {{ {model_name} }} from '../../models/{model_file_base}';")
        lines.append(f"import {{ {service_name} }} from '../../services/{service_file_base}';")
        lines.append('')

        # Comentario de encabezado
        lines.append('/**')
        lines.append(f' * Componente generado desde Oracle Forms Data Block: {block_name}')
        lines.append(' * Proporciona formulario para CRUD de datos')
        lines.append(' * Generado automáticamente - ajustar según necesidades')
        lines.append(' */')
        lines.append('@Component({')
        lines.append(f"  selector: '{selector}',")
        lines.append(f"  templateUrl: './{file_base}.html',")
        lines.append(f"  styleUrls: ['./{file_base}.css']")
        lines.append('})')
        lines.append(f'export class {component_name} implements OnInit {{')
        lines.append(f'  {self.naming.to_camel_case(block_name)}Form: FormGroup;')
        lines.append(f'  {self.naming.to_plural(self.naming.to_camel_case(block_name))}: {model_name}[] = [];')
        lines.append(f'  selected{model_name}: {model_name} | null = null;')
        lines.append('  isEditMode = false;')
        lines.append('  isLoading = false;')
        lines.append('  errorMessage = \'\';')
        lines.append('')

        # Constructor
        lines.append('  constructor(')
        lines.append('    private fb: FormBuilder,')
        lines.append(f'    private {self.naming.to_camel_case(service_name)}: {service_name}')
        lines.append('  ) {')
        lines.append(f'    this.{self.naming.to_camel_case(block_name)}Form = this.createForm();')
        lines.append('  }')
        lines.append('')

        # ngOnInit
        lines.append('  ngOnInit(): void {')
        lines.append('    this.loadData();')
        lines.append('  }')
        lines.append('')

        # createForm
        lines.append('  /**')
        lines.append('   * Crea el formulario reactivo con validadores')
        lines.append('   */')
        lines.append('  private createForm(): FormGroup {')
        lines.append('    return this.fb.group({')

        for item in items:
            item_name = item.get('name', 'UNNAMED')
            data_type = item.get('data_type', '')
            required = item.get('required', 'false').lower() == 'true'
            max_length = item.get('max_length', '')

            property_name = self.naming.to_property_name(item_name)
            validators = self.type_mapper.get_validators(data_type, required, max_length)
            validators_str = f'[{", ".join(validators)}]' if validators else '[]'

            lines.append(f"      {property_name}: ['', {validators_str}],")

        lines.append('    });')
        lines.append('  }')
        lines.append('')

        # loadData
        lines.append('  /**')
        lines.append('   * Carga todos los registros')
        lines.append('   */')
        lines.append('  loadData(): void {')
        lines.append('    this.isLoading = true;')
        lines.append('    this.errorMessage = \'\';')
        lines.append('')
        lines.append(f'    this.{self.naming.to_camel_case(service_name)}.getAll()')
        lines.append('      .subscribe({')
        lines.append('        next: (data) => {')
        lines.append(f'          this.{self.naming.to_plural(self.naming.to_camel_case(block_name))} = data;')
        lines.append('          this.isLoading = false;')
        lines.append('        },')
        lines.append('        error: (error) => {')
        lines.append('          this.errorMessage = \'Error loading data: \' + error.message;')
        lines.append('          this.isLoading = false;')
        lines.append('        }')
        lines.append('      });')
        lines.append('  }')
        lines.append('')

        # onSubmit
        lines.append('  /**')
        lines.append('   * Maneja el envío del formulario (crear o actualizar)')
        lines.append('   */')
        lines.append('  onSubmit(): void {')
        lines.append(f'    if (this.{self.naming.to_camel_case(block_name)}Form.valid) {{')
        lines.append('      this.isLoading = true;')
        lines.append('      this.errorMessage = \'\';')
        lines.append('')
        lines.append(f'      const formValue = this.{self.naming.to_camel_case(block_name)}Form.value;')
        lines.append('')
        lines.append('      if (this.isEditMode && this.selected' + model_name + ') {')
        lines.append('        // Actualizar registro existente')
        lines.append(f'        const id = this.selected{model_name}.' + self.naming.to_camel_case(items[0].get('name', 'id') if items else 'id') + ';')
        lines.append(f'        this.{self.naming.to_camel_case(service_name)}.update(id, formValue)')
        lines.append('          .subscribe({')
        lines.append('            next: () => {')
        lines.append('              this.loadData();')
        lines.append('              this.resetForm();')
        lines.append('            },')
        lines.append('            error: (error) => {')
        lines.append('              this.errorMessage = \'Error updating: \' + error.message;')
        lines.append('              this.isLoading = false;')
        lines.append('            }')
        lines.append('          });')
        lines.append('      } else {')
        lines.append('        // Crear nuevo registro')
        lines.append(f'        this.{self.naming.to_camel_case(service_name)}.create(formValue)')
        lines.append('          .subscribe({')
        lines.append('            next: () => {')
        lines.append('              this.loadData();')
        lines.append('              this.resetForm();')
        lines.append('            },')
        lines.append('            error: (error) => {')
        lines.append('              this.errorMessage = \'Error creating: \' + error.message;')
        lines.append('              this.isLoading = false;')
        lines.append('            }')
        lines.append('          });')
        lines.append('      }')
        lines.append('    }')
        lines.append('  }')
        lines.append('')

        # onEdit
        lines.append('  /**')
        lines.append('   * Prepara el formulario para editar un registro')
        lines.append('   */')
        lines.append(f'  onEdit(entity: {model_name}): void {{')
        lines.append(f'    this.selected{model_name} = entity;')
        lines.append('    this.isEditMode = true;')
        lines.append(f'    this.{self.naming.to_camel_case(block_name)}Form.patchValue(entity);')
        lines.append('  }')
        lines.append('')

        # onDelete
        lines.append('  /**')
        lines.append('   * Elimina un registro')
        lines.append('   */')
        lines.append(f'  onDelete(entity: {model_name}): void {{')
        lines.append("    if (confirm('Are you sure you want to delete this record?')) {")
        lines.append('      this.isLoading = true;')
        lines.append(f'      const id = entity.' + self.naming.to_camel_case(items[0].get('name', 'id') if items else 'id') + ';')
        lines.append('')
        lines.append(f'      this.{self.naming.to_camel_case(service_name)}.delete(id)')
        lines.append('        .subscribe({')
        lines.append('          next: () => {')
        lines.append('            this.loadData();')
        lines.append('          },')
        lines.append('          error: (error) => {')
        lines.append('            this.errorMessage = \'Error deleting: \' + error.message;')
        lines.append('            this.isLoading = false;')
        lines.append('          }')
        lines.append('        });')
        lines.append('    }')
        lines.append('  }')
        lines.append('')

        # resetForm
        lines.append('  /**')
        lines.append('   * Resetea el formulario')
        lines.append('   */')
        lines.append('  resetForm(): void {')
        lines.append(f'    this.{self.naming.to_camel_case(block_name)}Form.reset();')
        lines.append(f'    this.selected{model_name} = null;')
        lines.append('    this.isEditMode = false;')
        lines.append('    this.isLoading = false;')
        lines.append('  }')
        lines.append('}')
        lines.append('')

        return '\n'.join(lines)

    def _generate_html_content(
        self,
        model_name: str,
        items: List[Dict],
        datablock: Dict
    ) -> str:
        """Genera el contenido HTML del template"""
        block_name = datablock.get('name', 'UNNAMED')
        form_var_name = self.naming.to_camel_case(block_name) + 'Form'
        list_var_name = self.naming.to_plural(self.naming.to_camel_case(block_name))

        lines = []

        # Encabezado
        lines.append(f'<!-- Componente generado desde Oracle Forms Data Block: {block_name} -->')
        lines.append('<div class="container">')
        lines.append(f'  <h2>{self.naming.to_pascal_case(block_name)} Management</h2>')
        lines.append('')

        # Mensajes de error
        lines.append('  <!-- Error Message -->')
        lines.append('  <div *ngIf="errorMessage" class="alert alert-danger">')
        lines.append('    {{ errorMessage }}')
        lines.append('  </div>')
        lines.append('')

        # Formulario
        lines.append('  <!-- Form -->')
        lines.append(f'  <form [formGroup]="{form_var_name}" (ngSubmit)="onSubmit()" class="form-container">')
        lines.append(f'    <h3>{{{{ isEditMode ? \'Edit\' : \'New\' }}}} {model_name}</h3>')
        lines.append('')

        # Generar campos del formulario
        for item in items:
            item_name = item.get('name', 'UNNAMED')
            item_type = item.get('item_type', 'TEXT_ITEM')
            data_type = item.get('data_type', '')
            required = item.get('required', 'false').lower() == 'true'
            prompt = item.get('prompt', item_name.replace('_', ' ').title())

            property_name = self.naming.to_property_name(item_name)
            control_type, input_type = self.type_mapper.get_html_control_type(item_type, data_type)

            lines.append('    <div class="form-group">')
            lines.append(f'      <label for="{property_name}">')
            lines.append(f'        {prompt}')
            if required:
                lines.append('        <span class="required">*</span>')
            lines.append('      </label>')

            if control_type == 'textarea':
                lines.append(f'      <textarea')
                lines.append(f'        id="{property_name}"')
                lines.append(f'        formControlName="{property_name}"')
                lines.append('        class="form-control"')
                lines.append('        rows="3">')
                lines.append('      </textarea>')
            else:
                lines.append(f'      <input')
                lines.append(f'        id="{property_name}"')
                lines.append(f'        type="{input_type}"')
                lines.append(f'        formControlName="{property_name}"')
                lines.append('        class="form-control"')
                lines.append('      />')

            # Mensajes de validación
            lines.append(f'      <div *ngIf="{form_var_name}.get(\'{property_name}\')?.invalid && {form_var_name}.get(\'{property_name}\')?.touched"')
            lines.append('           class="error-message">')
            if required:
                lines.append(f"        <small *ngIf=\"{form_var_name}.get('{property_name}')?.errors?.['required']\">")
                lines.append(f'          {prompt} is required')
                lines.append('        </small>')
            lines.append('      </div>')
            lines.append('    </div>')
            lines.append('')

        # Botones del formulario
        lines.append('    <div class="form-actions">')
        lines.append(f'      <button type="submit" [disabled]="{form_var_name}.invalid || isLoading" class="btn btn-primary">')
        lines.append('        {{ isEditMode ? \'Update\' : \'Create\' }}')
        lines.append('      </button>')
        lines.append('      <button type="button" (click)="resetForm()" [disabled]="isLoading" class="btn btn-secondary">')
        lines.append('        Cancel')
        lines.append('      </button>')
        lines.append('    </div>')
        lines.append('  </form>')
        lines.append('')

        # Tabla de datos
        lines.append('  <!-- Data Table -->')
        lines.append('  <div class="table-container">')
        lines.append(f'    <h3>{model_name} List</h3>')
        lines.append('')
        lines.append('    <div *ngIf="isLoading" class="loading">Loading...</div>')
        lines.append('')
        lines.append(f'    <table *ngIf="!isLoading" class="data-table">')
        lines.append('      <thead>')
        lines.append('        <tr>')

        # Encabezados de tabla
        for item in items[:6]:  # Limitar a 6 columnas para no saturar
            prompt = item.get('prompt', item.get('name', '').replace('_', ' ').title())
            lines.append(f'          <th>{prompt}</th>')

        lines.append('          <th>Actions</th>')
        lines.append('        </tr>')
        lines.append('      </thead>')
        lines.append('      <tbody>')
        lines.append(f'        <tr *ngFor="let item of {list_var_name}">')

        # Datos de tabla
        for item in items[:6]:
            property_name = self.naming.to_property_name(item.get('name', ''))
            data_type = item.get('data_type', '')

            if 'DATE' in data_type.upper():
                lines.append(f'          <td>{{{{ item.{property_name} | date:\'short\' }}}}</td>')
            else:
                lines.append(f'          <td>{{{{ item.{property_name} }}}}</td>')

        # Botones de acciones
        lines.append('          <td class="action-buttons">')
        lines.append('            <button (click)="onEdit(item)" class="btn btn-sm btn-info">Edit</button>')
        lines.append('            <button (click)="onDelete(item)" class="btn btn-sm btn-danger">Delete</button>')
        lines.append('          </td>')
        lines.append('        </tr>')
        lines.append('      </tbody>')
        lines.append('    </table>')
        lines.append('  </div>')
        lines.append('</div>')
        lines.append('')

        return '\n'.join(lines)

    def _generate_css_content(self) -> str:
        """Genera el contenido CSS básico del componente"""
        return """/* Estilos generados automáticamente */
.container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

h2, h3 {
  color: #333;
  margin-bottom: 20px;
}

.alert {
  padding: 12px;
  margin-bottom: 20px;
  border-radius: 4px;
}

.alert-danger {
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  color: #721c24;
}

.form-container {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #555;
}

.required {
  color: red;
  margin-left: 3px;
}

.form-control {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-control:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 5px rgba(76, 175, 80, 0.3);
}

.error-message {
  color: #d32f2f;
  font-size: 12px;
  margin-top: 5px;
}

.form-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #45a049;
}

.btn-secondary {
  background-color: #757575;
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #616161;
}

.btn-info {
  background-color: #2196F3;
  color: white;
}

.btn-info:hover {
  background-color: #0b7dda;
}

.btn-danger {
  background-color: #f44336;
  color: white;
}

.btn-danger:hover {
  background-color: #da190b;
}

.btn-sm {
  padding: 5px 10px;
  font-size: 12px;
}

.table-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table thead {
  background-color: #f5f5f5;
}

.data-table th,
.data-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.data-table th {
  font-weight: 600;
  color: #333;
}

.data-table tbody tr:hover {
  background-color: #f9f9f9;
}

.action-buttons {
  display: flex;
  gap: 5px;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #666;
  font-style: italic;
}
"""

    def generate_multiple(self, datablocks: List[Dict], form_info: Dict = None) -> List[Dict]:
        """
        Genera múltiples componentes a partir de una lista de Data Blocks

        Args:
            datablocks: Lista de Data Blocks
            form_info: Información adicional del formulario

        Returns:
            Lista de resultados de generación
        """
        results = []

        for datablock in datablocks:
            try:
                result = self.generate_from_datablock(datablock, form_info)
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

        generator = ComponentGenerator(output_dir)
        datablocks = structure.get('data_blocks', [])

        print(f"Generating {len(datablocks)} components...")
        results = generator.generate_multiple(datablocks)

        for result in results:
            if result.get('success'):
                print(f"  ✓ {result['component_name']}")
                for file_path in result['files']:
                    print(f"    - {file_path}")
            else:
                print(f"  ✗ {result['block_name']}: {result['error']}")
    else:
        print("Usage: python component_gen.py <structure.json> [output_dir]")
