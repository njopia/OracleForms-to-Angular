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

## [Unreleased]

### Agregado
- ✨ Soporte genérico para todos los tipos de archivos Oracle Forms (.fmb, .mmb, .olb, .pll)
- 🔧 Sistema de formato de archivos dinámico y extensible
- 🔧 Métodos estáticos para validación de formatos soportados
- 📝 Detección automática de formatos en diálogos de selección de archivos
- 📝 Visualización dinámica de formatos admitidos en la interfaz

### Cambiado
- 🔄 Refactorizado sistema de extensiones de archivo para ser genérico
- 🔄 Los diálogos de selección de archivos ahora se construyen dinámicamente
- 🔄 La interfaz muestra automáticamente todos los formatos soportados

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
