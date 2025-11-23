"""
Oracle Forms to XML Converter
Main application with Tkinter GUI using Stepper pattern
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
from pathlib import Path
from converter import FormsConverter
from config_manager import ConfigManager


class StepperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Oracle Forms to XML Converter")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Initialize converter and config
        self.converter = FormsConverter()
        self.config_manager = ConfigManager()

        # Stepper state
        self.current_step = 0
        self.max_steps = 4
        self.selected_files = []
        self.conversion_results = []

        # Setup UI
        self.setup_ui()
        self.show_step(0)

    def setup_ui(self):
        """Setup the main UI components"""
        # Main container
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=1)

        # Title
        title_label = ttk.Label(
            main_container,
            text="Oracle Forms to XML Converter",
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, pady=10)

        # Stepper indicator
        self.stepper_frame = ttk.Frame(main_container)
        self.stepper_frame.grid(row=1, column=0, pady=10, sticky=(tk.W, tk.E))
        self.create_stepper()

        # Content area (will change based on step)
        self.content_frame = ttk.Frame(main_container)
        self.content_frame.grid(row=2, column=0, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)

        # Navigation buttons
        nav_frame = ttk.Frame(main_container)
        nav_frame.grid(row=3, column=0, pady=10, sticky=(tk.W, tk.E))

        self.prev_button = ttk.Button(
            nav_frame,
            text="← Anterior",
            command=self.previous_step,
            state=tk.DISABLED
        )
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = ttk.Button(
            nav_frame,
            text="Siguiente →",
            command=self.next_step
        )
        self.next_button.pack(side=tk.RIGHT, padx=5)

    def create_stepper(self):
        """Create the stepper indicator"""
        steps = [
            "1. Configuración",
            "2. Selección de Archivos",
            "3. Conversión",
            "4. Resultados"
        ]

        for i, step_text in enumerate(steps):
            # Step circle
            canvas = tk.Canvas(
                self.stepper_frame,
                width=40,
                height=40,
                highlightthickness=0
            )
            canvas.grid(row=0, column=i*2, padx=5)

            # Draw circle
            circle_id = canvas.create_oval(5, 5, 35, 35, fill="lightgray", outline="gray")
            text_id = canvas.create_text(20, 20, text=str(i+1), font=("Arial", 12, "bold"))

            # Store canvas and IDs for later updates
            canvas.circle_id = circle_id
            canvas.text_id = text_id
            canvas.step_num = i

            # Step label
            label = ttk.Label(self.stepper_frame, text=step_text)
            label.grid(row=1, column=i*2, padx=5)

            # Store for updates
            if not hasattr(self, 'step_canvases'):
                self.step_canvases = []
            self.step_canvases.append(canvas)

            # Connector line (except for last step)
            if i < len(steps) - 1:
                line_canvas = tk.Canvas(
                    self.stepper_frame,
                    width=80,
                    height=40,
                    highlightthickness=0
                )
                line_canvas.grid(row=0, column=i*2+1)
                line_canvas.create_line(0, 20, 80, 20, fill="gray", width=2)

    def update_stepper(self):
        """Update stepper visual state"""
        for i, canvas in enumerate(self.step_canvases):
            if i < self.current_step:
                # Completed step
                canvas.itemconfig(canvas.circle_id, fill="green", outline="darkgreen")
                canvas.itemconfig(canvas.text_id, fill="white")
            elif i == self.current_step:
                # Current step
                canvas.itemconfig(canvas.circle_id, fill="blue", outline="darkblue")
                canvas.itemconfig(canvas.text_id, fill="white")
            else:
                # Future step
                canvas.itemconfig(canvas.circle_id, fill="lightgray", outline="gray")
                canvas.itemconfig(canvas.text_id, fill="black")

    def show_step(self, step_num):
        """Show the specified step"""
        # Clear current content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Show appropriate step content
        if step_num == 0:
            self.show_config_step()
        elif step_num == 1:
            self.show_file_selection_step()
        elif step_num == 2:
            self.show_conversion_step()
        elif step_num == 3:
            self.show_results_step()

        # Update stepper visual
        self.update_stepper()

        # Update navigation buttons
        self.prev_button.config(state=tk.NORMAL if step_num > 0 else tk.DISABLED)

        if step_num == self.max_steps - 1:
            self.next_button.config(text="Finalizar", command=self.finish)
        else:
            self.next_button.config(text="Siguiente →", command=self.next_step)

    def show_config_step(self):
        """Step 1: Configuration"""
        step_frame = ttk.LabelFrame(
            self.content_frame,
            text="Configuración de Oracle Forms",
            padding="20"
        )
        step_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
        step_frame.columnconfigure(1, weight=1)

        # Auto-detect button at the top
        auto_detect_frame = ttk.Frame(step_frame)
        auto_detect_frame.grid(row=0, column=0, columnspan=3, pady=(0, 15))

        ttk.Button(
            auto_detect_frame,
            text="🔍 Detectar Automáticamente",
            command=self.auto_detect_paths
        ).pack(side=tk.LEFT, padx=5)

        self.detection_status_label = ttk.Label(
            auto_detect_frame,
            text="",
            foreground="gray"
        )
        self.detection_status_label.pack(side=tk.LEFT, padx=10)

        # Oracle Home path
        ttk.Label(step_frame, text="Oracle Forms Home:").grid(row=1, column=0, sticky=tk.W, pady=(10, 5))
        self.oracle_home_var = tk.StringVar(value=self.config_manager.get_oracle_home())
        oracle_entry = ttk.Entry(step_frame, textvariable=self.oracle_home_var, width=50)
        oracle_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=10, pady=(10, 5))

        browse_oracle_btn = ttk.Button(
            step_frame,
            text="Examinar...",
            command=self.browse_oracle_home
        )
        browse_oracle_btn.grid(row=1, column=2, padx=5, pady=(10, 5))

        # Oracle Home status label
        self.oracle_status_label = ttk.Label(
            step_frame,
            text="",
            foreground="gray",
            font=("Arial", 8)
        )
        self.oracle_status_label.grid(row=2, column=1, sticky=tk.W, padx=10, pady=(0, 10))

        # JAVA_HOME path
        ttk.Label(step_frame, text="JAVA_HOME (opcional):").grid(row=3, column=0, sticky=tk.W, pady=(10, 5))
        self.java_home_var = tk.StringVar(value=self.config_manager.get_java_home())
        java_entry = ttk.Entry(step_frame, textvariable=self.java_home_var, width=50)
        java_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=10, pady=(10, 5))

        browse_java_btn = ttk.Button(
            step_frame,
            text="Examinar...",
            command=self.browse_java_home
        )
        browse_java_btn.grid(row=3, column=2, padx=5, pady=(10, 5))

        # Java Home status label
        self.java_status_label = ttk.Label(
            step_frame,
            text="",
            foreground="gray",
            font=("Arial", 8)
        )
        self.java_status_label.grid(row=4, column=1, sticky=tk.W, padx=10, pady=(0, 10))

        # Output directory
        ttk.Label(step_frame, text="Directorio de salida:").grid(row=5, column=0, sticky=tk.W, pady=(10, 5))
        self.output_dir_var = tk.StringVar(value=self.config_manager.get_output_dir())
        output_entry = ttk.Entry(step_frame, textvariable=self.output_dir_var, width=50)
        output_entry.grid(row=5, column=1, sticky=(tk.W, tk.E), padx=10, pady=(10, 5))

        browse_output_btn = ttk.Button(
            step_frame,
            text="Examinar...",
            command=self.browse_output_dir
        )
        browse_output_btn.grid(row=5, column=2, padx=5, pady=(10, 5))

        # Test and diagnostic buttons
        button_frame = ttk.Frame(step_frame)
        button_frame.grid(row=6, column=1, pady=20)

        ttk.Button(
            button_frame,
            text="Verificar Configuración",
            command=self.test_configuration
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="🔍 Diagnóstico Detallado",
            command=self.show_diagnostic
        ).pack(side=tk.LEFT, padx=5)

        # Auto-detect on first load if fields are empty
        if not self.oracle_home_var.get() and not self.java_home_var.get():
            self.root.after(100, self.auto_detect_paths)

        # Info label
        info_text = """
Configuración:
• Oracle Forms Home: Requerido - Directorio de instalación de Oracle Forms Developer
• JAVA_HOME: Opcional - Se detectará automáticamente desde variables de entorno o Oracle
• Directorio de salida: Donde se guardarán los archivos XML generados
        """
        info_label = ttk.Label(step_frame, text=info_text, justify=tk.LEFT, foreground="gray")
        info_label.grid(row=7, column=0, columnspan=3, pady=10)

    def show_file_selection_step(self):
        """Step 2: File Selection"""
        step_frame = ttk.LabelFrame(
            self.content_frame,
            text="Selección de Archivos Oracle Forms",
            padding="20"
        )
        step_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
        step_frame.columnconfigure(0, weight=1)
        step_frame.rowconfigure(1, weight=1)

        # Buttons frame
        btn_frame = ttk.Frame(step_frame)
        btn_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=10)

        ttk.Button(
            btn_frame,
            text="Agregar Archivos",
            command=self.add_files
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="Agregar Directorio",
            command=self.add_directory
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="Limpiar Lista",
            command=self.clear_files
        ).pack(side=tk.LEFT, padx=5)

        # File list with scrollbar
        list_frame = ttk.Frame(step_frame)
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        self.file_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            selectmode=tk.EXTENDED,
            height=15
        )
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.file_listbox.yview)

        # Populate with existing files
        for file_path in self.selected_files:
            self.file_listbox.insert(tk.END, file_path)

        # Remove selected button
        ttk.Button(
            step_frame,
            text="Eliminar Seleccionados",
            command=self.remove_selected_files
        ).grid(row=2, column=0, pady=10)

        # Info
        info_text = f"Archivos seleccionados: {len(self.selected_files)}"
        ttk.Label(step_frame, text=info_text, font=("Arial", 10, "bold")).grid(row=3, column=0)

        formats_text = "Formatos admitidos: .fmb (Forms), .mmb (Menus), .olb (Object Libraries)"
        ttk.Label(step_frame, text=formats_text, foreground="gray").grid(row=4, column=0)

    def show_conversion_step(self):
        """Step 3: Conversion"""
        step_frame = ttk.LabelFrame(
            self.content_frame,
            text="Conversión a XML",
            padding="20"
        )
        step_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
        step_frame.columnconfigure(0, weight=1)
        step_frame.rowconfigure(2, weight=1)

        # Summary
        summary_text = f"Se convertirán {len(self.selected_files)} archivo(s) a XML"
        ttk.Label(
            step_frame,
            text=summary_text,
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, pady=10)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            step_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)

        # Log area
        log_frame = ttk.LabelFrame(step_frame, text="Log de conversión", padding="10")
        log_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            height=15,
            state=tk.DISABLED
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Convert button
        self.convert_button = ttk.Button(
            step_frame,
            text="Iniciar Conversión",
            command=self.start_conversion
        )
        self.convert_button.grid(row=3, column=0, pady=10)

    def show_results_step(self):
        """Step 4: Results"""
        step_frame = ttk.LabelFrame(
            self.content_frame,
            text="Resultados de la Conversión",
            padding="20"
        )
        step_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
        step_frame.columnconfigure(0, weight=1)
        step_frame.rowconfigure(1, weight=1)

        # Summary stats
        successful = sum(1 for r in self.conversion_results if r['success'])
        failed = len(self.conversion_results) - successful

        summary_text = f"Conversión completada: {successful} exitosos, {failed} fallidos"
        summary_label = ttk.Label(
            step_frame,
            text=summary_text,
            font=("Arial", 12, "bold")
        )
        summary_label.grid(row=0, column=0, pady=10)

        # Results table
        table_frame = ttk.Frame(step_frame)
        table_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)

        # Create treeview
        columns = ('archivo', 'estado', 'salida')
        self.results_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)

        self.results_tree.heading('archivo', text='Archivo')
        self.results_tree.heading('estado', text='Estado')
        self.results_tree.heading('salida', text='Archivo XML')

        self.results_tree.column('archivo', width=300)
        self.results_tree.column('estado', width=100)
        self.results_tree.column('salida', width=300)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscroll=scrollbar.set)

        self.results_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Populate results
        for result in self.conversion_results:
            status = "✓ Exitoso" if result['success'] else "✗ Fallido"
            self.results_tree.insert(
                '',
                tk.END,
                values=(
                    os.path.basename(result['input_file']),
                    status,
                    result.get('output_file', 'N/A')
                ),
                tags=('success' if result['success'] else 'error',)
            )

        # Configure tags
        self.results_tree.tag_configure('success', foreground='green')
        self.results_tree.tag_configure('error', foreground='red')

        # Buttons
        btn_frame = ttk.Frame(step_frame)
        btn_frame.grid(row=2, column=0, pady=10)

        ttk.Button(
            btn_frame,
            text="Abrir Carpeta de Salida",
            command=self.open_output_folder
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="Exportar Log",
            command=self.export_log
        ).pack(side=tk.LEFT, padx=5)

    # Event handlers
    def browse_oracle_home(self):
        directory = filedialog.askdirectory(title="Seleccionar Oracle Forms Home")
        if directory:
            self.oracle_home_var.set(directory)

    def browse_java_home(self):
        directory = filedialog.askdirectory(title="Seleccionar JAVA_HOME")
        if directory:
            self.java_home_var.set(directory)

    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="Seleccionar directorio de salida")
        if directory:
            self.output_dir_var.set(directory)

    def auto_detect_paths(self):
        """Auto-detect Oracle Home and Java Home from environment"""
        detection_results = self.config_manager.auto_detect_all()

        # Update Oracle Home
        oracle_home = detection_results['oracle_home']
        oracle_source = detection_results['oracle_source']

        if oracle_home:
            # Only update if current value is empty
            if not self.oracle_home_var.get():
                self.oracle_home_var.set(oracle_home)
            self.oracle_status_label.config(
                text=f"✓ {oracle_source}",
                foreground="green"
            )
        else:
            self.oracle_status_label.config(
                text=f"✗ {oracle_source}",
                foreground="orange"
            )

        # Update Java Home
        java_home = detection_results['java_home']
        java_source = detection_results['java_source']

        if java_home:
            # Only update if current value is empty
            if not self.java_home_var.get():
                self.java_home_var.set(java_home)
            self.java_status_label.config(
                text=f"✓ {java_source}",
                foreground="green"
            )
        else:
            self.java_status_label.config(
                text=f"ℹ {java_source}",
                foreground="gray"
            )

        # Update detection status
        if oracle_home and java_home:
            self.detection_status_label.config(
                text="✓ Detección completada exitosamente",
                foreground="green"
            )
        elif oracle_home:
            self.detection_status_label.config(
                text="✓ Oracle detectado. Java será usado desde Oracle.",
                foreground="green"
            )
        else:
            self.detection_status_label.config(
                text="⚠ No se pudo detectar Oracle Home automáticamente",
                foreground="orange"
            )

    def test_configuration(self):
        """Test if configuration is valid"""
        oracle_home = self.oracle_home_var.get()
        java_home = self.java_home_var.get()
        output_dir = self.output_dir_var.get()

        # Update converter config
        self.converter.set_config(oracle_home, java_home, output_dir)

        # Validate
        is_valid, errors, warnings = self.converter.validate_setup()

        if errors:
            error_msg = "Errores encontrados:\n\n" + "\n".join(f"• {e}" for e in errors)
            if warnings:
                error_msg += "\n\nAdvertencias:\n" + "\n".join(f"• {w}" for w in warnings)
            messagebox.showerror("Error de Configuración", error_msg)
        else:
            # Save configuration
            self.config_manager.save_config(oracle_home, java_home, output_dir)

            success_msg = "✓ Configuración válida y guardada correctamente"
            if warnings:
                success_msg += "\n\nAdvertencias:\n" + "\n".join(f"• {w}" for w in warnings)
            messagebox.showinfo("Éxito", success_msg)

    def show_diagnostic(self):
        """Show detailed diagnostic information"""
        oracle_home = self.oracle_home_var.get()
        java_home = self.java_home_var.get()
        output_dir = self.output_dir_var.get()

        # Update converter config
        self.converter.set_config(oracle_home, java_home, output_dir)

        # Get diagnostic info
        diag = self.converter.get_diagnostic_info()

        # Create diagnostic window
        diag_window = tk.Toplevel(self.root)
        diag_window.title("Diagnóstico Detallado")
        diag_window.geometry("700x600")

        # Main frame
        main_frame = ttk.Frame(diag_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(
            main_frame,
            text="Diagnóstico de Configuración",
            font=("Arial", 14, "bold")
        ).pack(pady=(0, 15))

        # Scrolled text for diagnostic info
        text_area = scrolledtext.ScrolledText(
            main_frame,
            wrap=tk.WORD,
            height=25,
            font=("Courier New", 9)
        )
        text_area.pack(fill=tk.BOTH, expand=True)

        # Build diagnostic report
        report = "=" * 70 + "\n"
        report += "DIAGNÓSTICO DE CONFIGURACIÓN - Oracle Forms to XML Converter\n"
        report += "=" * 70 + "\n\n"

        report += "📁 RUTAS CONFIGURADAS:\n"
        report += "-" * 70 + "\n"
        report += f"Oracle Home: {diag['oracle_home'] or '(no configurado)'}\n"
        report += f"  Existe: {'✓ SÍ' if diag['oracle_home_exists'] else '✗ NO'}\n\n"
        report += f"Java Home: {diag['java_home'] or '(no configurado - se usará el de Oracle)'}\n\n"
        report += f"Output Dir: {diag['output_dir'] or '(no configurado)'}\n\n"

        report += "☕ JAVA:\n"
        report += "-" * 70 + "\n"
        if diag['java_executable']:
            report += f"✓ Java encontrado: {diag['java_executable']}\n"
        else:
            report += "✗ Java NO encontrado\n"
        report += "\n"

        report += "🔧 ORACLE FRMF2XML.BAT:\n"
        report += "-" * 70 + "\n"
        if diag['has_oracle_bat']:
            report += f"✓ Oracle frmf2xml.bat encontrado: {diag['oracle_frmf2xml_bat']}\n"
            report += "  → Se usará el script ORIGINAL de Oracle (¡Recomendado!)\n"
            report += "  → No es necesario tener todos los JARs en jlib\n"
        else:
            report += "✗ Oracle frmf2xml.bat NO encontrado\n"
            report += "  → Se generará un script temporal\n"
            report += "  → Requiere que todos los JARs estén presentes\n"
        report += "\n"

        report += "📦 ARCHIVOS JAR:\n"
        report += "-" * 70 + "\n"

        if diag['jars_found']:
            report += f"✓ JARs encontrados ({len(diag['jars_found'])}):\n"
            for jar in diag['jars_found']:
                report += f"  ✓ {jar}\n"
        else:
            report += "✗ No se encontraron JARs\n"

        if diag['jars_missing']:
            report += f"\n✗ JARs faltantes ({len(diag['jars_missing'])}):\n"
            for jar in diag['jars_missing']:
                report += f"  ✗ {jar}\n"

        report += "\n" + "=" * 70 + "\n"
        report += "RECOMENDACIONES:\n"
        report += "=" * 70 + "\n\n"

        # Add recommendations
        if not diag['oracle_home_exists']:
            report += "1. Configure Oracle Home correctamente\n"
            report += "   - Debe apuntar al directorio de instalación de Oracle Forms\n"
            report += "   - Ejemplo: C:\\Oracle\\Middleware\\Oracle_FRHome1\n\n"

        if not diag['java_executable']:
            report += "2. Configure Java:\n"
            report += "   - Configure la variable JAVA_HOME\n"
            report += "   - O asegúrese que Oracle incluya JDK\n\n"

        critical_jars = ['jlib\\frmxmltools.jar', 'jlib\\frmf2xml.jar', 'jlib\\frmdapi.jar', 'jlib\\frmjdapi.jar']
        missing_critical = [j for j in critical_jars if j in diag['jars_missing']]

        if missing_critical and not diag['has_oracle_bat']:
            report += "3. JARs críticos faltantes:\n"
            for jar in missing_critical:
                report += f"   ✗ {jar}\n"
            report += "   OPCIONES:\n"
            report += "   a) Instale Oracle Forms Developer Suite completo\n"
            report += "   b) Busque frmf2xml.bat en su sistema y actualice Oracle Home\n"
            report += "   c) Copie los JARs faltantes de otra instalación Oracle\n\n"
        elif missing_critical and diag['has_oracle_bat']:
            report += "3. Algunos JARs faltan, PERO:\n"
            report += f"   ✓ Se encontró frmf2xml.bat de Oracle en: {diag['oracle_frmf2xml_bat']}\n"
            report += "   → El script de Oracle manejará sus propias dependencias\n"
            report += "   → Los JARs faltantes NO son críticos en este caso\n\n"

        if diag['has_oracle_bat']:
            report += "✓ CONFIGURACIÓN ÓPTIMA:\n"
            report += "  → Usando el frmf2xml.bat ORIGINAL de Oracle\n"
            report += "  → Oracle maneja sus propias dependencias\n"
            report += "  → La conversión debería funcionar correctamente\n\n"
        elif diag['jars_found'] and diag['java_executable'] and diag['oracle_home_exists']:
            report += "✓ La configuración parece correcta.\n"
            report += "  Si aún hay problemas de conversión:\n"
            report += "  - Verifique permisos de archivos\n"
            report += "  - Revise el log de conversión para detalles\n"
            report += "  - Asegúrese que los archivos .fmb no estén corruptos\n"

        # Insert report
        text_area.insert('1.0', report)
        text_area.config(state=tk.DISABLED)

        # Close button
        ttk.Button(
            main_frame,
            text="Cerrar",
            command=diag_window.destroy
        ).pack(pady=(10, 0))

    def add_files(self):
        """Add individual files"""
        filetypes = (
            ('Oracle Forms Files', '*.fmb *.mmb *.olb'),
            ('All files', '*.*')
        )
        files = filedialog.askopenfilenames(
            title="Seleccionar archivos Oracle Forms",
            filetypes=filetypes
        )

        for file_path in files:
            if file_path not in self.selected_files:
                self.selected_files.append(file_path)
                self.file_listbox.insert(tk.END, file_path)

    def add_directory(self):
        """Add all Oracle Forms files from a directory"""
        directory = filedialog.askdirectory(title="Seleccionar directorio")
        if directory:
            extensions = ['.fmb', '.mmb', '.olb']
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in extensions):
                        file_path = os.path.join(root, file)
                        if file_path not in self.selected_files:
                            self.selected_files.append(file_path)
                            self.file_listbox.insert(tk.END, file_path)

    def clear_files(self):
        """Clear all selected files"""
        self.selected_files.clear()
        self.file_listbox.delete(0, tk.END)

    def remove_selected_files(self):
        """Remove selected files from list"""
        selection = self.file_listbox.curselection()
        for index in reversed(selection):
            file_path = self.file_listbox.get(index)
            self.selected_files.remove(file_path)
            self.file_listbox.delete(index)

    def log_message(self, message):
        """Add message to log"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()

    def start_conversion(self):
        """Start the conversion process"""
        if not self.selected_files:
            messagebox.showwarning("Advertencia", "No hay archivos seleccionados")
            return

        # Disable button during conversion
        self.convert_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)

        # Clear previous results
        self.conversion_results.clear()

        # Update config
        self.config_manager.save_config(
            self.oracle_home_var.get(),
            self.java_home_var.get(),
            self.output_dir_var.get()
        )
        self.converter.set_config(
            self.oracle_home_var.get(),
            self.java_home_var.get(),
            self.output_dir_var.get()
        )

        total_files = len(self.selected_files)

        self.log_message(f"Iniciando conversión de {total_files} archivo(s)...")
        self.log_message("-" * 60)

        for i, file_path in enumerate(self.selected_files):
            progress = ((i + 1) / total_files) * 100
            self.progress_var.set(progress)

            self.log_message(f"\n[{i+1}/{total_files}] Procesando: {os.path.basename(file_path)}")

            try:
                result = self.converter.convert_file(file_path)
                self.conversion_results.append(result)

                # Show conversion method
                if 'conversion_method' in result:
                    self.log_message(f"  Método: {result['conversion_method']}")

                if result['success']:
                    self.log_message(f"  ✓ Éxito: {result['output_file']}")
                else:
                    self.log_message(f"  ✗ Error: {result.get('error', 'Error desconocido')}")

            except Exception as e:
                error_msg = str(e)
                self.log_message(f"  ✗ Excepción: {error_msg}")
                self.conversion_results.append({
                    'input_file': file_path,
                    'success': False,
                    'error': error_msg
                })

        self.log_message("\n" + "-" * 60)
        self.log_message("Conversión completada")

        # Re-enable buttons
        self.convert_button.config(state=tk.NORMAL)
        self.next_button.config(state=tk.NORMAL)

    def open_output_folder(self):
        """Open the output folder in file explorer"""
        output_dir = self.config_manager.get_output_dir()
        if os.path.exists(output_dir):
            if sys.platform == 'win32':
                os.startfile(output_dir)
            elif sys.platform == 'darwin':
                os.system(f'open "{output_dir}"')
            else:
                os.system(f'xdg-open "{output_dir}"')
        else:
            messagebox.showwarning("Advertencia", "El directorio de salida no existe")

    def export_log(self):
        """Export conversion log to file"""
        log_file = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Guardar log"
        )

        if log_file:
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write("Oracle Forms to XML Conversion Log\n")
                f.write("=" * 60 + "\n\n")
                for result in self.conversion_results:
                    f.write(f"Input: {result['input_file']}\n")
                    f.write(f"Status: {'Success' if result['success'] else 'Failed'}\n")
                    if result['success']:
                        f.write(f"Output: {result['output_file']}\n")
                    else:
                        f.write(f"Error: {result.get('error', 'Unknown')}\n")
                    f.write("-" * 60 + "\n")

            messagebox.showinfo("Éxito", f"Log exportado a:\n{log_file}")

    def next_step(self):
        """Move to next step"""
        # Validate current step before proceeding
        if self.current_step == 0:
            # Validate configuration
            if not self.oracle_home_var.get():
                messagebox.showwarning("Advertencia", "Debe configurar Oracle Forms Home")
                return
            if not self.output_dir_var.get():
                messagebox.showwarning("Advertencia", "Debe configurar el directorio de salida")
                return

            # Save configuration
            self.config_manager.save_config(
                self.oracle_home_var.get(),
                self.java_home_var.get(),
                self.output_dir_var.get()
            )

        elif self.current_step == 1:
            # Validate file selection
            if not self.selected_files:
                messagebox.showwarning("Advertencia", "Debe seleccionar al menos un archivo")
                return

        elif self.current_step == 2:
            # Check if conversion was done
            if not self.conversion_results:
                messagebox.showwarning("Advertencia", "Debe ejecutar la conversión primero")
                return

        if self.current_step < self.max_steps - 1:
            self.current_step += 1
            self.show_step(self.current_step)

    def previous_step(self):
        """Move to previous step"""
        if self.current_step > 0:
            self.current_step -= 1
            self.show_step(self.current_step)

    def finish(self):
        """Finish the wizard"""
        result = messagebox.askyesno(
            "Finalizar",
            "¿Desea procesar más archivos?"
        )

        if result:
            # Reset to file selection step
            self.selected_files.clear()
            self.conversion_results.clear()
            self.current_step = 1
            self.show_step(self.current_step)
        else:
            self.root.quit()


def main():
    root = tk.Tk()
    app = StepperApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
