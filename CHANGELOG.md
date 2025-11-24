# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [1.0.0] - 2024-11-23

### Agregado
- ✨ Interfaz gráfica completa con patrón Stepper (4 pasos)
- ✨ Paso 1: Configuración de Oracle Home, Java Home y directorio de salida
- ✨ Paso 2: Selección de archivos individuales o por directorio
- ✨ Paso 3: Conversión con barra de progreso y log en tiempo real
- ✨ Paso 4: Visualización de resultados en tabla con estado
- 🔧 Sistema de configuración persistente (JSON)
- 🔧 Generación dinámica de script batch frmf2xml.bat
- 📝 Soporte para formatos .fmb, .mmb, y .olb
- 📝 Log detallado de conversión
- 📝 Exportación de log a archivo de texto
- 🎨 Indicador visual de pasos con estados (pendiente, actual, completado)
- 🎨 Código de colores en resultados (verde=éxito, rojo=error)
- 🚀 Scripts de inicio rápido (run_converter.bat / .sh)
- 📚 Documentación completa (README.md, QUICKSTART.md)
- 📚 Ejemplos de configuración
- 🔒 Archivo .gitignore para proteger datos sensibles

### Características Técnicas
- Conversión por lotes de múltiples archivos
- Timeout de 2 minutos por archivo
- Validación de configuración antes de conversión
- Detección automática de Java en Oracle Forms
- Manejo robusto de errores
- Interfaz responsiva con scrollbars
- Soporte para rutas con espacios

### Documentación
- README.md completo con ejemplos
- QUICKSTART.md para inicio rápido
- CHANGELOG.md para seguimiento de versiones
- Comentarios extensos en código
- Archivo de configuración de ejemplo

## [2.0.0] - 2025-11-24

### Agregado - Pipeline Completo de Migración
- ✨ **Pipeline completo Oracle Forms → Angular**
- 🚀 Analizador XML de Oracle Forms (xml_analyzer.py)
  - Extrae Data Blocks, Items, Triggers, LOVs, Canvases, Windows
  - Analiza relaciones entre bloques
  - Extrae Program Units y Parameters
- 🎯 Sistema de mapeo de tipos Oracle → TypeScript (type_mapper.py)
  - Mapeo automático de tipos de datos
  - Generación de validadores Angular
  - Detección de controles HTML según tipo de dato
- 📝 Sistema de convenciones de nombres (naming_convention.py)
  - Conversión automática a PascalCase, camelCase, kebab-case
  - Generación de nombres para componentes, servicios, modelos
  - Manejo de singular/plural
- 🏗️ Generadores de código Angular:
  - **ModelGenerator**: Genera interfaces TypeScript con tipado fuerte
  - **ServiceGenerator**: Genera servicios con operaciones CRUD completas
  - **ComponentGenerator**: Genera componentes (.ts, .html, .css)
- 🎭 Generador maestro (angular_generator.py)
  - Orquesta todo el proceso de generación
  - Crea estructura de directorios Angular
  - Genera reportes HTML detallados
- 📦 Script de migración por lotes (batch_migrate.py)
  - Acepta ZIP, directorios o archivos individuales
  - Conversión automática .fmb → XML → Angular
  - Reporte de migración con estadísticas

### Agregado - Características Previas
- ✨ Soporte genérico para todos los tipos de archivos Oracle Forms (.fmb, .mmb, .olb, .pll)
- 🔧 Sistema de formato de archivos dinámico y extensible
- 🔧 Métodos estáticos para validación de formatos soportados
- 📝 Detección automática de formatos en diálogos de selección de archivos
- 📝 Visualización dinámica de formatos admitidos en la interfaz

### Cambiado
- 🔄 Refactorizado sistema de extensiones de archivo para ser genérico
- 🔄 Los diálogos de selección de archivos ahora se construyen dinámicamente
- 🔄 La interfaz muestra automáticamente todos los formatos soportados

### Estructura Generada
```
angular_output/
├── models/              # Interfaces TypeScript
├── services/            # Servicios Angular con CRUD
├── components/          # Componentes completos
│   └── [entity]/
│       ├── .component.ts
│       ├── .component.html
│       └── .component.css
├── analysis/            # Estructuras JSON analizadas
└── migration_report.html
```

### Planeado para futuras versiones
- Soporte para Linux/Mac (scripts shell en lugar de .bat)
- Conversión paralela de múltiples archivos
- Validación automática de XML generado
- Comparación visual entre Forms y XML
- Integración con pipeline de conversión a Angular
- Modo línea de comandos (CLI) sin GUI
- Plantillas de configuración predefinidas
- Historial de conversiones
- Estadísticas y reportes
- Soporte para archivos adicionales de Oracle Forms

---

## Tipos de Cambios

- `Added` (Agregado): para nuevas características
- `Changed` (Cambiado): para cambios en funcionalidad existente
- `Deprecated` (Deprecado): para características que serán removidas
- `Removed` (Removido): para características removidas
- `Fixed` (Arreglado): para corrección de bugs
- `Security` (Seguridad): en caso de vulnerabilidades
