import math
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter.scrolledtext import ScrolledText
from tkinter.font import nametofont

# -------------------------------------------------------------------
# 3. LÓGICA DE LA INTERFAZ GRÁFICA (GUI)
# -------------------------------------------------------------------

class PhysicsApp:
    def __init__(self, root):
        self.root = root
        root.title("Calculadora de Movimiento Relativo 🛰️")
        root.geometry("750x450") 
        root.minsize(600, 400)

        # --- Configuración de Fuente Global (REQUIERE COMFORTAA INSTALADA) ---
        self.font_family = "Comfortaa"
        self.font_size = 11
        
        try:
            default_font = nametofont("TkDefaultFont")
            default_font.configure(family=self.font_family, size=self.font_size)
            text_font = nametofont("TkTextFont")
            text_font.configure(family=self.font_family, size=self.font_size)
            fixed_font = nametofont("TkFixedFont")
            fixed_font.configure(family=self.font_family, size=self.font_size)
            root.option_add("*Font", default_font)
        except Exception as e:
            print(f"Advertencia: No se pudo cargar la fuente '{self.font_family}'. Usando fuente por defecto. Error: {e}")
            self.font_family = "Helvetica" # Fuente de respaldo

        # --- Definir fuentes específicas ---
        self.font_bold = (self.font_family, self.font_size, "bold")
        self.font_title = (self.font_family, self.font_size + 1, "bold")
        self.font_result = (self.font_family, self.font_size + 4, "bold") # Tamaño 15

        # --- Layout Principal (PanedWindow) ---
        main_pane = ttk.PanedWindow(root, orient=HORIZONTAL)
        main_pane.pack(fill=BOTH, expand=True)

        # --- Panel Izquierdo (Controles) ---
        control_frame = self.create_control_panel(main_pane)
        main_pane.add(control_frame, weight=1)

        # --- Panel Derecho (Resultados) ---
        output_frame = self.create_output_panel(main_pane)
        main_pane.add(output_frame, weight=2)

        # --- Configuración de Colores Neón para Salida ---
        self.color_op = self.root.style.colors.get('info')        
        self.color_error = self.root.style.colors.get('danger')   
        self.color_result_text = self.root.style.colors.get('warning') 
        self.color_result_bg = "#5e2e8f" 
        
        self.font_output_bold = (self.font_family, self.font_size, "bold")
        
        self.output_text.tag_configure("op", foreground=self.color_op, font=self.font_output_bold)
        self.output_text.tag_configure("error", foreground=self.color_error, font=self.font_output_bold)
        self.output_text.tag_configure("result_text", foreground=self.color_result_text, font=self.font_result)
        self.output_text.tag_configure("result_bg", background=self.color_result_bg, lmargin1=10, lmargin2=10)


    def create_control_panel(self, parent):
        """Crea el panel lateral izquierdo con entradas y botones."""
        control_frame = ttk.Frame(parent, padding=15)
        control_frame.grid_rowconfigure(1, weight=1) # Espacio para empujar
        control_frame.grid_columnconfigure(0, weight=1)

        # --- Grupo de Entradas ---
        input_group = ttk.LabelFrame(control_frame, text="Datos de Entrada 🛰️", padding=15)
        input_group.grid(row=0, column=0, sticky="ew")
        input_group.columnconfigure(1, weight=1)

        # Espacio (s)
        ttk.Label(input_group, text="Espacio (Km)", font=self.font_bold).grid(row=0, column=0, sticky="w", padx=5, pady=8)
        self.s_entry = ttk.Entry(input_group)
        self.s_entry.grid(row=0, column=1, sticky="ew")

        # Tiempo (t1)
        ttk.Label(input_group, text="Tiempo (min)", font=self.font_bold).grid(row=1, column=0, sticky="w", padx=5, pady=8)
        self.t_entry = ttk.Entry(input_group)
        self.t_entry.grid(row=1, column=1, sticky="ew")

        # Velocidad 1 (v1)
        ttk.Label(input_group, text="Velocidad 1 (Km/h)", font=self.font_bold).grid(row=2, column=0, sticky="w", padx=5, pady=8)
        self.v1_entry = ttk.Entry(input_group)
        self.v1_entry.grid(row=2, column=1, sticky="ew")

        # Velocidad 2 (v2)
        ttk.Label(input_group, text="Velocidad 2 (Km/h)", font=self.font_bold).grid(row=3, column=0, sticky="w", padx=5, pady=8)
        self.v2_entry = ttk.Entry(input_group)
        self.v2_entry.grid(row=3, column=1, sticky="ew")

        # --- Botones ---
        button_frame = ttk.Frame(control_frame, padding=(0, 20, 0, 0))
        button_frame.grid(row=2, column=0, sticky="ew")
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        self.calc_btn = ttk.Button(button_frame, text="Calcular", command=self.calculate, bootstyle=INFO)
        self.calc_btn.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        self.clear_btn = ttk.Button(button_frame, text="Limpiar", command=self.clear_output, bootstyle=WARNING)
        self.clear_btn.grid(row=0, column=1, sticky="ew", padx=(5, 0))
        
        return control_frame

    def create_output_panel(self, parent):
        """Crea el panel lateral derecho con el área de texto."""
        output_frame = ttk.Frame(parent, padding=(5, 15, 15, 15))
        output_frame.pack(fill=BOTH, expand=True)

        ttk.Label(output_frame, text="Resultados del Cálculo 📊", font=self.font_title).pack(anchor=NW)

        st_frame = ttk.Frame(output_frame, padding=2, bootstyle=SECONDARY)
        st_frame.pack(fill=BOTH, expand=True, pady=(5,0))
        
        self.output_text = ScrolledText(st_frame, height=10, width=50, 
                                        font=(self.font_family, self.font_size), 
                                        wrap=WORD, relief=FLAT, bd=0)
        self.output_text.pack(fill=BOTH, expand=True)
        self.output_text.config(state=DISABLED)
        
        return output_frame

    def write_output(self, text, style_tag=None):
        """Escribe en el área de resultado usando tags de estilo."""
        self.output_text.config(state=NORMAL)
        
        if style_tag == "result_text":
            self.output_text.insert(END, text + "\n", ("result_text", "result_bg"))
        elif style_tag:
            self.output_text.insert(END, text + "\n", style_tag)
        else:
            self.output_text.insert(END, text + "\n")
            
        if style_tag: # Añade un espacio después de cualquier línea con estilo
            self.output_text.insert(END, "\n")
            
        self.output_text.config(state=DISABLED)
        self.output_text.see(END) 

    def clear_output(self):
        self.output_text.config(state=NORMAL)
        self.output_text.delete(1.0, END)
        self.output_text.config(state=DISABLED)

    def calculate(self):
        """Función principal que ejecuta la lógica del script."""
        try:
            # 1. Registro de datos
            s = float(self.s_entry.get())
            t1_min = float(self.t_entry.get())
            v1 = float(self.v1_entry.get())
            v2 = float(self.v2_entry.get())

            # 2. Conversión y cálculos intermedios
            t_hr = t1_min / 60
            p = v2 * -t_hr
            
            # 3. Cálculo final (usando la fórmula corregida)
            # La fórmula original tenía un error de precedencia de operadores
            if (v1 - v2) == 0:
                raise ZeroDivisionError

            r = (s + p) / (v1 - v2)

            # 4. Mostrar resultados
            self.write_output("--- Datos de Entrada ---", "op")
            self.write_output(f"Espacio (s): {s:.2f} Km")
            self.write_output(f"Tiempo (t): {t1_min:.2f} min ({t_hr:.3f} horas)")
            self.write_output(f"Velocidad 1 (v1): {v1:.2f} Km/h")
            self.write_output(f"Velocidad 2 (v2): {v2:.2f} Km/h")
            
            self.write_output("--- Resultado ---", "op")
            self.write_output(f"Tiempo de Encuentro (r): {r:.3f} horas", "result_text")

        except ValueError:
            self.write_output("Error: Por favor, introduce solo números en todos los campos.", "error")
        except ZeroDivisionError:
            self.write_output("Error: Las velocidades no pueden ser iguales (división por cero).", "error")
        except Exception as e:
            self.write_output(f"Error inesperado: {e}", "error")

# -------------------------------------------------------------------
# 4. EJECUCIÓN PRINCIPAL
# -------------------------------------------------------------------
if __name__ == "__main__":
    app = ttk.Window(themename="cyborg")
    PhysicsApp(app)
    app.mainloop()