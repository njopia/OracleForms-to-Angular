# Oracle Forms to XML Converter

Una aplicación Python con interfaz gráfica (GUI) que convierte archivos de Oracle Forms a formato XML utilizando la herramienta `frmf2xml.bat` de Oracle.

## 🎯 Características

- ✅ **Interfaz Stepper intuitiva**: Guía paso a paso para el proceso de conversión
- ✅ **Soporte múltiple formatos**: `.fmb` (Forms), `.mmb` (Menus), `.olb` (Object Libraries)
- ✅ **Conversión por lotes**: Procesa múltiples archivos simultáneamente
- ✅ **Configuración persistente**: Guarda tus configuraciones para uso futuro
- ✅ **Log detallado**: Registro completo del proceso de conversión
- ✅ **Resultados visuales**: Tabla de resultados con estado de cada conversión

## 📋 Requisitos Previos

### Software Requerido

1. **Python 3.8 o superior**
   - Descargar de [python.org](https://www.python.org/downloads/)
   - Asegúrate de marcar "Add Python to PATH" durante la instalación

2. **Oracle Forms Developer Suite**
   - Debe estar instalado en tu sistema
   - La herramienta Forms2XML debe estar disponible

3. **Java Runtime Environment (JRE)**
   - Puede ser el JDK incluido con Oracle Forms
   - O un JAVA_HOME configurado en el sistema

### Dependencias Python

El proyecto utiliza únicamente bibliotecas estándar de Python:
- `tkinter` - Interfaz gráfica (incluido con Python en Windows/Mac)
- `subprocess` - Ejecución de procesos
- `json` - Gestión de configuración
- `pathlib` - Manejo de rutas

**Nota para Linux**: Puede que necesites instalar tkinter por separado:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora/RHEL
sudo dnf install python3-tkinter

# Arch
sudo pacman -S tk
```

## 🚀 Instalación

1. **Clonar o descargar el repositorio**
   ```bash
   git clone <repository-url>
   cd OracleForms-to-Angular
   ```

2. **Verificar instalación de Python**
   ```bash
   python --version
   # Debe mostrar Python 3.8 o superior
   ```

3. **No se requiere instalación de dependencias adicionales** (usa librerías estándar)

## 💻 Uso

### Iniciar la aplicación

```bash
cd oracle_forms_converter/src
python main.py
```

### Proceso de Conversión (4 Pasos)

#### **Paso 1: Configuración**

Configure las rutas necesarias:

- **Oracle Forms Home**: Ruta de instalación de Oracle Forms Developer
  - Ejemplo: `C:\Oracle\Middleware\Oracle_FRHome1`
  - Debe contener la carpeta `jlib` con los JARs necesarios

- **JAVA_HOME** (opcional): Ruta de instalación de Java
  - Si no se especifica, se usa el JDK incluido en Oracle Forms
  - Ejemplo: `C:\Program Files\Java\jdk1.8.0_281`

- **Directorio de Salida**: Donde se guardarán los archivos XML
  - Se crea automáticamente si no existe
  - Ejemplo: `C:\Output\XML_Files`

Haz clic en **"Verificar Configuración"** para validar las rutas antes de continuar.

#### **Paso 2: Selección de Archivos**

Agrega los archivos Oracle Forms que deseas convertir:

- **Agregar Archivos**: Selecciona archivos individuales (`.fmb`, `.mmb`, `.olb`)
- **Agregar Directorio**: Escanea recursivamente un directorio completo
- **Limpiar Lista**: Elimina todos los archivos de la lista
- **Eliminar Seleccionados**: Remueve archivos específicos

Formatos soportados:
- `.fmb` - Oracle Forms Module Binary
- `.mmb` - Oracle Menu Module Binary
- `.olb` - Oracle Object Library Binary

#### **Paso 3: Conversión**

Inicia y monitorea el proceso de conversión:

1. Revisa el resumen de archivos a convertir
2. Haz clic en **"Iniciar Conversión"**
3. Observa la barra de progreso
4. Lee el log detallado en tiempo real

El proceso:
- Crea un script batch temporal con tu configuración
- Ejecuta Forms2XML para cada archivo
- Genera archivos XML en el directorio de salida
- Registra todos los eventos y errores

#### **Paso 4: Resultados**

Revisa los resultados de la conversión:

- **Tabla de Resultados**:
  - ✓ Verde: Conversión exitosa
  - ✗ Rojo: Conversión fallida
  - Muestra archivo origen, estado y archivo XML generado

- **Acciones disponibles**:
  - **Abrir Carpeta de Salida**: Abre el directorio con los XML generados
  - **Exportar Log**: Guarda un registro detallado en archivo de texto
  - **Finalizar**: Opción de procesar más archivos o cerrar

---

## 🚀 NUEVO: Pipeline Completo de Migración a Angular

### Migración Automática: Oracle Forms → Angular

A partir de la versión 2.0, el proyecto incluye un **pipeline completo** que no solo convierte Forms a XML, sino que **genera automáticamente componentes Angular completos** listos para usar.

### Características del Pipeline

```
Oracle Forms (.fmb) → XML → Análisis → Angular (Components + Services + Models)
```

#### ¿Qué genera?

✅ **Modelos TypeScript** - Interfaces con tipado fuerte
✅ **Servicios Angular** - CRUD completo con HttpClient
✅ **Componentes Angular** - .ts, .html, .css
✅ **Formularios Reactivos** - Con validaciones
✅ **Tablas de datos** - Con acciones CRUD
✅ **Reporte HTML** - Documentación de la migración

### Uso del Pipeline Completo

#### Opción 1: Script de Migración por Lotes

```bash
# Desde un archivo ZIP
python batch_migrate.py oracle_forms.zip

# Desde un directorio
python batch_migrate.py /path/to/forms/directory

# Archivo individual
python batch_migrate.py customer_form.fmb
```

#### Proceso Automático

1. **Extracción** (si es ZIP) → Encuentra todos los archivos .fmb, .mmb, .olb, .pll
2. **Conversión** → .fmb → XML usando frmf2xml.bat
3. **Análisis** → Extrae Data Blocks, Items, Triggers, LOVs, etc.
4. **Generación** → Crea componentes Angular completos
5. **Reporte** → Genera `migration_report.html` con estadísticas

#### Estructura Generada

```
migration_work/
├── angular_output/
│   ├── models/                    # Interfaces TypeScript
│   │   ├── customer.model.ts
│   │   ├── order.model.ts
│   │   └── product.model.ts
│   ├── services/                  # Servicios con CRUD
│   │   ├── customer.service.ts
│   │   ├── order.service.ts
│   │   └── product.service.ts
│   ├── components/                # Componentes completos
│   │   ├── customer/
│   │   │   ├── customer.component.ts
│   │   │   ├── customer.component.html
│   │   │   └── customer.component.css
│   │   ├── order/
│   │   └── product/
│   ├── analysis/                  # Estructuras JSON analizadas
│   │   ├── CUSTOMER_FORM_structure.json
│   │   └── ORDER_FORM_structure.json
│   └── migration_report.html     # Reporte detallado
```

### Ejemplo de Código Generado

#### Modelo TypeScript
```typescript
// models/customer.model.ts
export interface Customer {
  customerId: number;
  firstName: string;
  lastName: string;
  email?: string | null;
  phone?: string | null;
  createdDate: Date;
}
```

#### Servicio Angular
```typescript
// services/customer.service.ts
@Injectable({ providedIn: 'root' })
export class CustomerService {
  private apiUrl = '/api/customers';

  constructor(private http: HttpClient) { }

  getAll(): Observable<Customer[]> { /* ... */ }
  getById(id: number): Observable<Customer> { /* ... */ }
  create(entity: Customer): Observable<Customer> { /* ... */ }
  update(id: number, entity: Customer): Observable<Customer> { /* ... */ }
  delete(id: number): Observable<void> { /* ... */ }
  search(filters: any): Observable<Customer[]> { /* ... */ }
}
```

#### Componente Angular
```typescript
// components/customer/customer.component.ts
@Component({
  selector: 'app-customer',
  templateUrl: './customer.component.html',
  styleUrls: ['./customer.component.css']
})
export class CustomerComponent implements OnInit {
  customerForm: FormGroup;
  customers: Customer[] = [];

  constructor(
    private fb: FormBuilder,
    private customerService: CustomerService
  ) {
    this.customerForm = this.createForm();
  }

  ngOnInit(): void {
    this.loadData();
  }

  onSubmit(): void { /* CRUD logic */ }
  onEdit(entity: Customer): void { /* ... */ }
  onDelete(entity: Customer): void { /* ... */ }
}
```

### Mapeo Automático

#### Tipos de Datos
| Oracle Forms | TypeScript |
|-------------|-----------|
| VARCHAR2 | string |
| NUMBER | number |
| DATE | Date |
| TIMESTAMP | Date |
| CHAR | string |
| BLOB | Blob |

#### Convenciones de Nombres
| Oracle Forms | Angular |
|-------------|---------|
| CUSTOMER_MASTER | CustomerMasterComponent |
| CUSTOMERS | CustomerService |
| CUSTOMER_ID | customerId |
| ORDER_DETAILS | order-details.component.ts |

### Arquitectura del Pipeline

```
┌─────────────────┐
│  Oracle Forms   │
│   (.fmb, .mmb)  │
└────────┬────────┘
         │
         ↓ frmf2xml.bat
┌─────────────────┐
│      XML        │
└────────┬────────┘
         │
         ↓ xml_analyzer.py
┌─────────────────┐
│   Estructura    │
│   Analizada     │
└────────┬────────┘
         │
         ↓ Generadores
┌─────────────────┬─────────────────┬─────────────────┐
│  ModelGenerator │ ServiceGenerator│ComponentGenerator│
└────────┬────────┴────────┬────────┴────────┬────────┘
         │                 │                 │
         ↓                 ↓                 ↓
   ┌─────────┐      ┌──────────┐     ┌────────────┐
   │ Models  │      │ Services │     │ Components │
   │   .ts   │      │   .ts    │     │.ts .html   │
   └─────────┘      └──────────┘     │   .css     │
                                      └────────────┘
```

### Componentes del Sistema

#### 1. **xml_analyzer.py** - Analizador XML
- Extrae Data Blocks, Items, Triggers
- Identifica Canvases, Windows, LOVs
- Analiza relaciones entre bloques
- Exporta estructura como JSON

#### 2. **type_mapper.py** - Mapeo de Tipos
- Oracle → TypeScript
- Generación de validadores Angular
- Detección de controles HTML por tipo

#### 3. **naming_convention.py** - Convenciones
- PascalCase, camelCase, kebab-case
- Singular/Plural automático
- Nombres de archivos consistentes

#### 4. **Generadores**
- `model_gen.py` → Interfaces TypeScript
- `service_gen.py` → Servicios Angular
- `component_gen.py` → Componentes completos

#### 5. **angular_generator.py** - Orquestador
- Coordina todo el proceso
- Genera estructura de directorios
- Crea reportes HTML

### Personalización

Los archivos generados son **puntos de partida** que puedes personalizar:

- ✅ Código limpio y comentado
- ✅ Estructura estándar Angular
- ✅ Preparado para TypeScript strict mode
- ✅ Incluye manejo de errores básico
- ⚠️ Ajustar endpoints de API según tu backend
- ⚠️ Refinar validaciones según reglas de negocio
- ⚠️ Agregar lógica de triggers específica

---

## 📂 Estructura del Proyecto

```
OracleForms-to-Angular/
├── oracle_forms_converter/
│   ├── src/
│   │   ├── __init__.py              # Inicialización del paquete
│   │   ├── main.py                  # Aplicación principal con GUI
│   │   ├── converter.py             # Lógica de conversión FMB→XML
│   │   ├── config_manager.py        # Gestión de configuración
│   │   ├── xml_analyzer.py          # Analizador de XML de Oracle Forms
│   │   ├── type_mapper.py           # Mapeo Oracle→TypeScript
│   │   ├── naming_convention.py     # Convenciones de nombres
│   │   ├── angular_generator.py     # Orquestador de generación
│   │   └── generators/
│   │       ├── __init__.py
│   │       ├── model_gen.py         # Generador de modelos TS
│   │       ├── service_gen.py       # Generador de servicios
│   │       └── component_gen.py     # Generador de componentes
│   ├── config/
│   │   └── settings.json            # Configuración guardada (auto)
│   ├── output/                      # Archivos XML generados
│   └── logs/                        # Logs de conversión
├── batch_migrate.py                 # Script de migración completa
├── CHANGELOG.md                     # Historial de cambios
├── QUICKSTART.md                    # Guía rápida
└── README.md                        # Este archivo
```

## ⚙️ Configuración Avanzada

### Archivo de Configuración

La configuración se guarda automáticamente en `config/settings.json`:

```json
{
    "oracle_home": "C:\\Oracle\\Middleware\\Oracle_FRHome1",
    "java_home": "C:\\Program Files\\Java\\jdk1.8.0_281",
    "output_dir": "C:\\Output\\XML_Files",
    "recent_files": [],
    "last_input_dir": "",
    "auto_open_output": true
}
```

### Script Batch Generado

La aplicación genera dinámicamente un script batch basado en `frmf2xml.bat` con tu configuración:

```batch
@ECHO OFF
REM Configuración de PATH y CLASSPATH
set PATH=%ORACLE_HOME%\bin;%PATH%

REM Detección de Java
if exist %JAVA_HOME%\bin\java.exe (...)

REM Ejecución de Forms2XML
%FORMS_JDK_HOME%\java -classpath [...] oracle.forms.util.xmltools.Forms2XML source=input.fmb dest=output.xml overwrite=yes
```

## 🔧 Solución de Problemas

### Error: "Java not found"

**Problema**: No se encuentra Java en el sistema.

**Soluciones**:
1. Instala Java JDK 8 o superior
2. Configura la variable de entorno `JAVA_HOME`
3. O deja que la aplicación use el JDK incluido en Oracle Forms

### Error: "JAR requerido no encontrado"

**Problema**: Faltan archivos JAR de Oracle Forms.

**Solución**: Verifica que Oracle Forms esté correctamente instalado y que la ruta incluya:
- `jlib/frmxmltools.jar`
- `jlib/frmf2xml.jar`
- `jlib/frmdapi.jar`
- `oracle_common/modules/oracle.xdk/xmlparserv2.jar`

### Error: "No se generó el archivo XML"

**Posibles causas**:
1. Archivo de entrada corrupto o en formato incorrecto
2. Permisos insuficientes en el directorio de salida
3. Error en la herramienta Forms2XML de Oracle

**Solución**:
- Revisa el log detallado para mensajes de error específicos
- Verifica que tienes permisos de escritura en el directorio de salida
- Prueba convertir el archivo manualmente con Forms2XML

### Error: "tkinter no disponible" (Linux)

**Problema**: Tkinter no está instalado en tu sistema Linux.

**Solución**:
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora/RHEL
sudo dnf install python3-tkinter
```

## 📝 Notas Adicionales

### Formatos de Archivo Oracle Forms

- **`.fmb`**: Forms Module Binary - Formularios de Oracle Forms
- **`.mmb`**: Menu Module Binary - Menús de Oracle Forms
- **`.olb`**: Object Library Binary - Bibliotecas de objetos compartidos

### Limitaciones

- Timeout de conversión: 2 minutos por archivo
- Requiere Oracle Forms Developer Suite instalado
- Solo funciona en Windows (debido a dependencia de `.bat` files)

### Roadmap Futuro

- [ ] Soporte para Linux/Mac (usando scripts shell)
- [ ] Conversión paralela de múltiples archivos
- [ ] Validación de XML generado
- [ ] Comparación visual de Forms vs XML
- [ ] Integración con Angular conversion pipeline

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo licencia MIT. Ver archivo `LICENSE` para más detalles.

## 👥 Autores

- Oracle Forms Converter Team

## 🙏 Agradecimientos

- Oracle Corporation por la herramienta Forms2XML
- Comunidad Python por las excelentes bibliotecas estándar

---

**Versión**: 1.0.0
**Última actualización**: 2024
