import tkinter as tk
from tkinter import ttk
from math import sin, radians, cos
import os

# from plxscripting.easy import *

server_password = "82aVYn2%76<gE<XA"
# s_i, g_i = new_server("localhost", 10000, password=server_password)


H1_font = ("Times New Roman", 18)
H2_font = ("Times New Roman", 16)
H3_font = ("Times New Roman", 12)


def toggle_widget(widget, show=False):
    if show:
        widget.grid(**widget._grid_info)
    else:
        widget._grid_info = widget.grid_info()
        widget.grid_remove()


def add_labeled_input(self, label, default=""):
    label = ttk.Label(self, text=f"{label} :", font=H3_font)
    label.grid(row=self.row_no, column=0, pady=10, sticky="E")

    input_field = ttk.Entry(self, width=20)
    input_field.configure(justify="center")
    input_field.insert(0, default)
    input_field.grid(row=self.row_no, column=1, pady=10)
    self.row_no += 1
    return input_field, label


def convert_float(value):
    try:
        return float(value)
    except ValueError:
        return ""


def add_labeled_dropdown(self, label, options, default_index=0, width=15):
    menu_label = ttk.Label(self, text=f"{label} :", font=H3_font)
    menu_label.grid(row=self.row_no, column=0, pady=10, sticky="E")
    menu_label._grid_info = menu_label.grid_info()

    menu_options = tk.StringVar()
    menu_options.set(options[default_index])

    menu_list = tk.OptionMenu(
        self, menu_options, *options, command=lambda _: self.get_data()
    )
    menu_list.config(width=width)
    menu_list.grid(row=self.row_no, column=1, pady=10)
    menu_list._grid_info = menu_list.grid_info()

    self.row_no += 1
    return menu_options, menu_label, menu_list


def setMaterial(material, properties):
    for key in properties:
        material.setproperties(key, properties[key])

    return material


def add_title(self, title):
    label = ttk.Label(self, text=title, font=H3_font)
    label.grid(row=self.row_no, column=0, pady=10, columnspan=2)
    self.row_no += 1


def create_material(material_type, material_properties):
    if material_type == "Plate":
        com = """_platemat 'Comments' '' 'Metadata' '' 'MaterialName' 'Kazık' 'Colour' 16711680 'MaterialNumber' 0 'Elasticity' 0 'IsIsotropic' True 'PreventPunching' True 'ElastoplasticMK' 'M-K diagram' 'ElastoplasticMKTable' '[0, 0, 1, 1]' 'NonSoilSpecificHeatCapacity' 0 'ThermalConductivity' 0 'Density' 0 'ThermalExpansion' 0 'EA' 264000 'EA2' 264000 'EI' 15000 'nu' 0.25 'd' 0.82572282384477 'w' 1 'Mp' 1.0000000000000000E+015 'Np' 1.0000000000000000E+010 'Np2' 1.0000000000000000E+010 'RayleighAlpha' 0 'RayleighBeta' 0 'Gref' 127887.950957078"""
        s_i.call_commands(com)
        material = [
            mat for mat in g_i.Materials[:] if mat.TypeName.value == "PlateMat2D"
        ][-1]

    elif material_type == "Anchor":
        material = g_i.anchormat()

    elif material_type == "Geogrid":
        material = g_i.geogridmat()

    elif material_type == "Embedded":
        material = g_i.embeddedbeammat()

    material = setMaterial(material, material_properties)

    return material


class tkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):

        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
        current_file_path = os.path.dirname(os.path.abspath(__file__))
        if "azure.tcl" in os.listdir(current_file_path):
            self.tk.call("source", os.path.join(current_file_path, "azure.tcl"))
            self.tk.call("set_theme", "dark")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.bind("<Home>", self.return_main_page)
        self.frames = {}

        for F in (
            StartPage,
            BoredPile,
            DiaghragmWall,
            ShearWall,
            Shotcrete,
            Anchor,
            Strut,
            SoilNail,
            Loading,
        ):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def return_main_page(self, event):
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        self.winfo_toplevel().title(frame.title)
        frame.tkraise()
        self.bind("<Return>", frame.enter_event)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.title = "İksa Sistemleri Plaxis Makrosu"
        # label of frame Layout 2
        label = ttk.Label(self, text="Lütfen İksa Sistemi Seçiniz", font=H1_font)

        # putting the grid in its place by using
        # grid
        label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        button1 = ttk.Button(
            self,
            text="Fore Kazık",
            command=lambda: controller.show_frame(BoredPile),
            width=25,
        )
        button1.grid(row=1, column=1, padx=10, pady=10)

        button2 = ttk.Button(
            self,
            text="Diyafram Duvar",
            command=lambda: controller.show_frame(DiaghragmWall),
            width=25,
        )
        button2.grid(row=1, column=2, padx=10, pady=10)

        button3 = ttk.Button(
            self,
            text="Betonarme Perde Duvar",
            command=lambda: controller.show_frame(ShearWall),
            width=25,
        )
        button3.grid(row=2, column=1, padx=10, pady=10)

        button4 = ttk.Button(
            self,
            text="Shotcrete",
            command=lambda: controller.show_frame(Shotcrete),
            width=25,
        )
        button4.grid(row=2, column=2, padx=10, pady=10)

        button5 = ttk.Button(
            self,
            text="Ankraj",
            command=lambda: controller.show_frame(Anchor),
            width=25,
        )
        button5.grid(row=3, column=1, padx=10, pady=10)

        button6 = ttk.Button(
            self,
            text="Strut",
            command=lambda: controller.show_frame(Strut),
            width=25,
        )
        button6.grid(row=3, column=2, padx=10, pady=10)

        button7 = ttk.Button(
            self,
            text="Zemin Çivisi",
            command=lambda: controller.show_frame(SoilNail),
            width=25,
        )
        button7.grid(row=4, column=1, padx=10, pady=10)

        # style = ttk.Style()
        # style.configure("TButton", background="green")
        button8 = ttk.Button(
            self,
            text="Sürşarj Ekle",
            command=lambda: controller.show_frame(Loading),
            width=25,
            # style="TButton",
        )

        button8.grid(row=4, column=2, padx=10, pady=10)

    def enter_event(self, event):
        pass


class BoredPile(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.title = "Fore Kazık İksa Sistemi"
        self.row_no = 0
        self.diameter_input, _ = add_labeled_input(self, "Fore kazık çapı(m)")
        self.distance_input, _ = add_labeled_input(self, "Fore kazık net aralığı(m)")
        self.length_input, _ = add_labeled_input(self, "Kazık boyu(m)")
        self.starting_x_input, _ = add_labeled_input(
            self, "Başlangıç koordinatı(x ekseni)"
        )
        self.starting_y_input, _ = add_labeled_input(
            self, "Başlangıç koordinatı(y ekseni)"
        )
        self.soil_density_input, _ = add_labeled_input(
            self, "Ortalama zemin birim hacim ağırlığı(kN/m3)"
        )
        concrete_classes = ["C25", "C30", "C35", "C30", "C45", "C50"]
        self.cc_options, _, _ = add_labeled_dropdown(
            self, "Beton Sınıfı", concrete_classes
        )

        self.pile_created = 0

    def get_data(self):
        diameter = convert_float(self.diameter_input.get())
        distance = convert_float(self.distance_input.get())
        cc = self.cc_options.get()
        starting_x = convert_float(self.starting_x_input.get())
        starting_y = convert_float(self.starting_y_input.get())
        length = convert_float(self.length_input.get())
        soil_density = convert_float(self.soil_density_input.get())

        return diameter, distance, length, cc, starting_x, starting_y, soil_density

    def calc_modulus(self, diameter, distance, cc):
        E_dict = {"C25": 30e6, "C30": 32e6, "C35": 33e6, "C45": 36e6, "C50": 37e6}
        E = E_dict[cc]

        I = 3.14 * (diameter ** 4) / 64
        A = 3.14 * (diameter / 2) ** 2
        S = diameter + distance
        EA = E * A / S  # kN/m
        EI = E * I / S  # kN.m2/m
        d_real = (12 * EI / EA) ** 0.5

        return EA, EI, d_real

    def add_pile(self):
        try:
            g_i.gotostructures()
            (
                diameter,
                distance,
                length,
                cc,
                starting_x,
                starting_y,
                soil_density,
            ) = self.get_data()
            EA, EI, d_real = self.calc_modulus(diameter, distance, cc)
            pile_properties = {
                "EA": EA,
                "EA": EA,
                "EI": EI,
                "w": max((24.5 - soil_density) * d_real, 0),
                "nu": 0.2,
                "IsIsotropic": True,
                "MaterialName": f"Kazık_{self.pile_created+1}",
            }
            plate_material = create_material("Plate", pile_properties)
            pile_line = g_i.line(
                (starting_x, starting_y), (starting_x, starting_y - length)
            )[-1]
            g_i.plate(pile_line, "Material", plate_material)
            interface_line = g_i.line(
                (starting_x, starting_y), (starting_x, starting_y - length - 0.5)
            )[-1]
            g_i.posinterface(interface_line)
            g_i.neginterface(interface_line)
            self.pile_created += 1
        except:
            pass

    def enter_event(self, event):
        self.add_pile()


class Wall(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.row_no = 0
        self.starting_x_input, _ = add_labeled_input(
            self, "Başlangıç koordinatı(x ekseni)"
        )
        self.starting_y_input, _ = add_labeled_input(
            self, "Başlangıç koordinatı(y ekseni)"
        )
        concrete_classes = ["C25", "C30", "C35", "C30", "C45", "C50"]
        self.cc_options, _, _ = add_labeled_dropdown(
            self, "Beton Sınıfı", concrete_classes
        )
        self.wall_thickness, _ = add_labeled_input(self, "Duvar Kalınlığı(cm)")
        self.wall_length, _ = add_labeled_input(self, "Duvar Uzunluğu(m)")
        self.wall_density, _ = add_labeled_input(
            self, "Duvar Birim Hacim Ağırlığı(kN/m3)", 25
        )
        self.poisson_ratio, _ = add_labeled_input(self, "v(nu)", 0.2)
        self.soil_density, _ = add_labeled_input(
            self, "Ortalama zemin birim hacim ağırlığı(kN/m3)"
        )

    def get_data(self):
        data = {
            "starting_x": convert_float(self.starting_x_input.get()),
            "starting_y": convert_float(self.starting_y_input.get()),
            "wall_thickness": convert_float(self.wall_thickness.get()),
            "cc": self.cc_options.get(),
            "wall_length": convert_float(self.wall_length.get()),
            "wall_density": convert_float(self.wall_density.get()),
            "soil_density": convert_float(self.soil_density.get()),
            "poisson_ratio": convert_float(self.poisson_ratio.get()),
        }

        return data

    def calc_params(self, data):
        cc = data["cc"]
        wall_density = data["wall_density"]
        soil_density = data["soil_density"]
        nu = data["poisson_ratio"]
        thickness = data["wall_thickness"] / 100
        E_dict = {"C25": 30e6, "C30": 32e6, "C35": 33e6, "C45": 36e6, "C50": 37e6}
        E = E_dict[cc]

        I = (thickness ** 3) / 12
        A = thickness
        EA = E * A  # kN/m
        EI = E * I  # kN.m2/m
        w = thickness * (wall_density - soil_density)

        props = {
            "MaterialName": f"{self.wall_type}_{self.wall_created+1}",
            "EA": EA,
            "EI": EI,
            "w": w,
            "nu": nu,
            "IsIsotropic": True,
        }

        return props

    def create_wall(self):
        g_i.gotostructures()
        input_data = self.get_data()
        material_props = self.calc_params(input_data)
        starting_x = input_data["starting_x"]
        starting_y = input_data["starting_y"]
        length = input_data["wall_length"]
        plate_material = create_material("Plate", material_props)
        wall_line = g_i.line(
            (starting_x, starting_y), (starting_x, starting_y - length)
        )[-1]
        g_i.plate(wall_line, "Material", plate_material)
        interface_line = g_i.line(
            (starting_x, starting_y), (starting_x, starting_y - length - 0.5)
        )[-1]
        g_i.posinterface(interface_line)
        g_i.neginterface(interface_line)
        self.wall_created += 1

    def enter_event(self, event):
        try:
            self.create_wall()
        except Exception as e:
            print(e)


class DiaghragmWall(Wall, tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        Wall.__init__(self, parent)
        self.title = "Diyafram Duvar İksa Sistemi"
        self.wall_created = 0
        self.wall_type = "Diyafram"


class ShearWall(Wall, tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        Wall.__init__(self, parent)
        self.title = "Betonarme Perde Duvar İksa Sistemi"
        self.wall_created = 0
        self.wall_type = "Perde"


class Strut(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.title = "Strut İksa Sistemi"
        self.row_no = 0
        self.element_type, _, _ = add_labeled_dropdown(
            self, "Eleman Tipi", ["Node to node anchor", "Fixed end anchor"], width=20
        )
        self.starting_x_input, _ = add_labeled_input(
            self, "Başlangıç koordinatı(x ekseni)"
        )
        self.starting_y_input, _ = add_labeled_input(
            self, "Başlangıç koordinatı(y ekseni)"
        )
        self.strut_length, _ = add_labeled_input(self, "Strut Uzunluğu(m)")
        self.strut_diameter, _ = add_labeled_input(self, "Strut Dış Çapı(m)")
        self.strut_thickness, _ = add_labeled_input(self, "Strut Et Kalınlığı(m)")
        self.L_spacing, _ = add_labeled_input(self, "Yatay Aralık(m)")
        self.elastic_modulus, _ = add_labeled_input(
            self, "Elastisite Modülü(kPa)", 200e6
        )

        self.strut_created = 0

    def get_data(self):
        data = {
            "x": convert_float(self.starting_x_input.get()),
            "y": convert_float(self.starting_y_input.get()),
            "length": convert_float(self.strut_length.get()),
            "diameter": convert_float(self.strut_diameter.get()),
            "thickness": convert_float(self.strut_thickness.get()),
            "elastic_modulus": convert_float(self.elastic_modulus.get()),
            "L_spacing": convert_float(self.L_spacing.get()),
            "element_type": self.element_type.get(),
        }

        return data

    def calc_props(self, data):
        diameter = data["diameter"]
        thickness = data["thickness"]
        elastic_modulus = data["elastic_modulus"]
        L_spacing = data["L_spacing"]

        area = 0.25 * 3.14 * (diameter ** 2 - (diameter - 2 * thickness) ** 2)
        props = {
            "EA": elastic_modulus * area,
            "Lspacing": L_spacing,
            "MaterialName": f"Strut Mat_{self.strut_created+1}",
        }

        return props

    def create_element(self, data):
        material_props = self.calc_props(data)
        x = data["x"]
        y = data["y"]
        length = data["length"]
        strut_mat = create_material("Anchor", material_props)
        if data["element_type"] == "Node to node anchor":
            line = g_i.line((x, y), (x + length, y))[-1]
            g_i.n2nanchor(line, "Material", strut_mat)
        elif data["element_type"] == "Fixed end anchor":
            point = g_i.point(x, y)
            g_i.fixedendanchor(point, "Material", strut_mat, "Direction_x", length)

    def add_strut(self):
        input_data = self.get_data()
        self.create_element(input_data)
        self.strut_created += 1

    def enter_event(self, event):
        try:
            self.add_strut()
        except Exception as e:
            print(e)


class Shotcrete(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.title = "Shotcrete İksa Sistemi"
        self.row_no = 0
        self.starting_x_input, _ = add_labeled_input(
            self, "Başlangıç koordinatı(x ekseni)"
        )
        self.starting_y_input, _ = add_labeled_input(
            self, "Başlangıç koordinatı(y ekseni)"
        )
        self.slope_angle, _ = add_labeled_input(self, "Eğim Açısı(Derece)", 270)
        self.wall_thickness, _ = add_labeled_input(self, "Kalınlık(cm)")
        self.wall_length, _ = add_labeled_input(self, "Uzunluk(m)")
        self.elastic_modulus, _ = add_labeled_input(
            self, "Elastisite Modülü(kPa)", 20e6
        )
        self.wall_density, _ = add_labeled_input(
            self, "Birim Hacim Ağırlığı(kN/m3)", 25
        )
        self.poisson_ratio, _ = add_labeled_input(self, "v(nu)", 0.2)
        self.soil_density, _ = add_labeled_input(
            self, "Ortalama zemin birim hacim ağırlığı(kN/m3)"
        )
        self.wall_created = 0

    def get_data(self):
        data = {
            "starting_x": convert_float(self.starting_x_input.get()),
            "starting_y": convert_float(self.starting_y_input.get()),
            "wall_thickness": convert_float(self.wall_thickness.get()),
            "slope_angle": convert_float(self.slope_angle.get()),
            "elastic_modulus": convert_float(self.elastic_modulus.get()),
            "wall_length": convert_float(self.wall_length.get()),
            "wall_density": convert_float(self.wall_density.get()),
            "soil_density": convert_float(self.soil_density.get()),
            "poisson_ratio": convert_float(self.poisson_ratio.get()),
        }

        return data

    def calc_params(self, data):
        E = data["elastic_modulus"]
        wall_density = data["wall_density"]
        soil_density = data["soil_density"]
        nu = data["poisson_ratio"]
        thickness = data["wall_thickness"] / 100

        I = (thickness ** 3) / 12
        A = thickness
        EA = E * A  # kN/m
        EI = E * I  # kN.m2/m
        w = thickness * (wall_density - soil_density)

        props = {
            "MaterialName": f"Shotcrete_{self.wall_created+1}",
            "EA": EA,
            "EI": EI,
            "w": w,
            "nu": nu,
            "IsIsotropic": True,
        }

        return props

    def create_wall(self):
        g_i.gotostructures()
        input_data = self.get_data()
        material_props = self.calc_params(input_data)
        starting_x = input_data["starting_x"]
        starting_y = input_data["starting_y"]
        length = input_data["wall_length"]
        angle = input_data["slope_angle"]
        plate_material = create_material("Plate", material_props)
        y_end = starting_y + sin(radians(angle)) * length
        y_end_interface = starting_y + sin(radians(angle)) * (length + 0.5)
        x_end = starting_x + cos(radians(angle)) * length
        x_end_interface = starting_x + cos(radians(angle)) * (length + 0.5)
        wall_line = g_i.line((starting_x, starting_y), (x_end, y_end))[-1]
        g_i.plate(wall_line, "Material", plate_material)
        interface_line = g_i.line(
            (starting_x, starting_y), (x_end_interface, y_end_interface)
        )[-1]
        g_i.posinterface(interface_line)
        g_i.neginterface(interface_line)
        self.wall_created += 1

    def enter_event(self, event):
        try:
            self.create_wall()
        except Exception as e:
            print(e)


class SoilNail(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.title = "Zemin Çivisi İksa Sistemi"
        self.row_no = 0
        self.x_coordinate, _ = add_labeled_input(self, "X Koordinatı")
        self.y_coordinate, _ = add_labeled_input(self, "Y Koordinatı")
        self.angle, _ = add_labeled_input(self, "Açı")
        self.diameter, _ = add_labeled_input(self, "Çap(cm)")
        self.length, _ = add_labeled_input(self, "Uzunluk(m)")
        self.L_spacing, _ = add_labeled_input(self, "Yatay Aralık(m)")
        self.elastic_modulus, _ = add_labeled_input(
            self, "Elastisite Modülü(kPa)", 10e6
        )
        self.excavation_width, _ = add_labeled_input(self, "Kazı Genişliği(m)")
        self.nail_created = 0

    def get_data(self):
        data = {
            "x_coordinate": convert_float(self.x_coordinate.get()),
            "y_coordinate": convert_float(self.y_coordinate.get()),
            "angle": convert_float(self.angle.get()),
            "excavation_width": convert_float(self.excavation_width.get()),
            "L_spacing": convert_float(self.L_spacing.get()),
            "diameter": convert_float(self.diameter.get()),
            "length": convert_float(self.length.get()),
            "elastic_modulus": convert_float(self.elastic_modulus.get()),
        }

        return data

    def calc_props(self, data):
        E = data["elastic_modulus"]
        diameter = data["diameter"] / 100
        L_spacing = data["L_spacing"]
        props = {
            "MaterialName": f"Zemin Çivisi_{self.nail_created+1}",
            "EA1": E * 3.14 * 0.25 * (diameter ** 2) / L_spacing,
            "EA2": E * 3.14 * 0.25 * (diameter ** 2) / L_spacing,
        }

        return props

    def add_nail(self):
        data = self.get_data()
        props = self.calc_props(data)

        g_i.gotostructures()
        data = self.get_data()
        x0 = data["x_coordinate"]
        y0 = data["y_coordinate"]
        y_end = y0 + sin(radians(data["angle"])) * data["length"]
        x_end = x0 + cos(radians(data["angle"])) * data["length"]
        line = g_i.line((x0, y0), (x_end, y_end))[-1]
        material = create_material("Geogrid", props)
        g_i.geogrid(line, "Material", material)
        if data["excavation_width"] != 0:
            g_i.line((x0, y0 - 0.5), (x0 + data["excavation_width"], y0 - 0.5))[-1]

        self.nail_created += 1

    def enter_event(self, event):
        try:
            self.add_nail()
        except Exception as e:
            print(e)


class Anchor(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.title = "Ankraj Duvar İksa Sistemi"

        self.tabControl = ttk.Notebook(self)

        self.tab1 = self.general_params_tab()
        self.tabControl.add(self.tab1, text="Genel Parametreler")

        self.tab2 = self.unbound_params_tab()
        self.tabControl.add(self.tab2, text="Serbest Bölge Parametreleri")

        self.tab3 = self.bound_params_tab()
        self.tabControl.add(self.tab3, text="Kök Bölgesi Parametreleri")

        self.tabControl.pack(expand=1, fill="both")

        self.anchor_created = 0

    def general_params_tab(self):
        tab = ttk.Frame(self.tabControl)
        tab.row_no = 0
        self.x_coordinate, _ = add_labeled_input(tab, "X Koordinatı")
        self.y_coordinate, _ = add_labeled_input(tab, "Y Koordinatı")
        self.angle, _ = add_labeled_input(tab, "Ankraj Açısı")
        self.excavation_width, _ = add_labeled_input(tab, "Kazı Genişliği(m)")

        return tab

    def unbound_params_tab(self):
        tab = ttk.Frame(self.tabControl)
        tab.row_no = 0
        tab.get_data = self.get_data

        self.tie_type, _, _ = add_labeled_dropdown(
            tab,
            "Halat Tipi",
            ["Grade 250", "Grade 270", "Diğer"],
            0,
            width=20,
        )
        (
            self.tie_diameter,
            self.tie_diameter_label,
            self.tie_diameter_menu,
        ) = add_labeled_dropdown(
            tab, "Halat Anma Çapı(in)", ["3/8", "7/16", "1/2", "0.6"], 2, width=20
        )
        self.tie_area, self.tie_area_label = add_labeled_input(
            tab, "Halat Kesit Alanı(cm2)"
        )
        toggle_widget(self.tie_area, False)
        toggle_widget(self.tie_area_label, False)
        self.L_spacing, _ = add_labeled_input(tab, "Serbest Bölge Yatay Aralığı(m)")
        self.unbound_length, _ = add_labeled_input(tab, "Serbest Bölge Uzunluğu(m)")
        self.anchor_number, _ = add_labeled_input(tab, "Ankraj Adedi")

        return tab

    def bound_params_tab(self):
        tab = ttk.Frame(self.tabControl)
        tab.row_no = 0
        tab.get_data = self.get_data
        self.bound_E, _ = add_labeled_input(tab, "Elastisite Modülü(kPa)", 10e6)
        self.bound_length, _ = add_labeled_input(tab, "Kök Bölgesi Uzunluğu(m)")
        self.bound_diameter, _ = add_labeled_input(tab, "Kök Bölgesi Çapı(cm)")
        self.bound_type, _, _ = add_labeled_dropdown(
            tab,
            "Kök Bölgesi Eleman Tipi",
            ["Geogrid", "Embedded beam row"],
            1,
            width=20,
        )

        self.T_max, self.T_max_label = add_labeled_input(
            tab, "Max. Sürtünme Direnci(kN/m)"
        )
        self.T_min, self.T_min_label = add_labeled_input(
            tab, "Min. Sürtünme Direnci(kN/m)"
        )
        self.gamma, self.gamma_label = add_labeled_input(
            tab, "Kök Bölgesi Birim Hacim Ağırlığı(kN/m3)", 23.5
        )

        return tab

    def anchor_props(self, data):
        tie_area = data["tie_area"]
        anchor_number = data["anchor_number"]
        L_spacing = data["L_spacing"]
        bound_type = data["bound_type"]
        bound_diameter = data["bound_diameter"]
        T_max = data["T_max"]
        T_min = data["T_min"]
        bound_E = data["bound_E"]
        gamma = data["gamma"]

        unbound_props = {
            "EA": 200e2 * tie_area * anchor_number,
            "Lspacing": L_spacing,
            "MaterialName": f"Serbest Bölge Mat_{self.anchor_created+1}",
        }

        if bound_type == "Geogrid":
            bound_props = {
                "MaterialName": f"Kök Bölge Mat_{self.anchor_created+1}",
                "EA1": bound_E * 3.14 * 0.25 * (bound_diameter ** 2) / L_spacing,
                "EA2": bound_E * 3.14 * 0.25 * (bound_diameter ** 2) / L_spacing,
            }
        else:
            bound_props = {
                "E": bound_E,
                "Diameter": bound_diameter,
                "Lspacing": L_spacing,
                "w": gamma,
                "MaterialName": f"Kök Bölge Mat_{self.anchor_created+1}",
                "Tstart": T_max,
                "Tend": T_min,
            }

        return unbound_props, bound_props

    def calc_tie_area(self):
        grade_250 = {"3/8": 0.08, "7/16": 0.108, "1/2": 0.144, "0.6": 0.216}
        grade_270 = {"3/8": 0.085, "7/16": 0.115, "1/2": 0.153, "0.6": 0.217}

        tie_type = self.tie_type.get()
        tie_diameter = self.tie_diameter.get()
        if tie_type == "Grade 250":
            tie_area = 6.4516 * grade_250[tie_diameter]
        elif tie_type == "Grade 270":
            tie_area = 6.4516 * grade_270[tie_diameter]
        else:
            tie_area = convert_float(self.tie_area.get())

        return tie_area

    def get_data(self):
        data = {
            "x_coordinate": convert_float(self.x_coordinate.get()),
            "y_coordinate": convert_float(self.y_coordinate.get()),
            "angle": convert_float(self.angle.get()),
            "anchor_number": convert_float(self.anchor_number.get()),
            "tie_area": convert_float(self.tie_area.get()),
            "excavation_width": convert_float(self.excavation_width.get()),
            "L_spacing": convert_float(self.L_spacing.get()),
            "unbound_length": convert_float(self.unbound_length.get()),
            "bound_length": convert_float(self.bound_length.get()),
            "bound_diameter": convert_float(self.bound_diameter.get()),
            "bound_type": self.bound_type.get(),
            "T_max": convert_float(self.T_max.get()),
            "T_min": convert_float(self.T_min.get()),
            "tie_area": self.calc_tie_area(),
            "bound_E": convert_float(self.bound_E.get()),
            "gamma": convert_float(self.gamma.get()),
        }

        try:
            if data["tie_type"] == "Diğer":
                toggle_widget(self.tie_diameter_menu, False)
                toggle_widget(self.tie_diameter_label, False)
                toggle_widget(self.tie_area, True)
                toggle_widget(self.tie_area_label, True)

            else:
                toggle_widget(self.tie_diameter_menu, True)
                toggle_widget(self.tie_diameter_label, True)
                toggle_widget(self.tie_area, False)
                toggle_widget(self.tie_area_label, False)
        except:
            pass
        try:
            if data["bound_type"] == "Geogrid":
                toggle_widget(self.T_max_label, False)
                toggle_widget(self.T_min_label, False)
                toggle_widget(self.gamma_label, False)
                toggle_widget(self.T_max, False)
                toggle_widget(self.T_min, False)
                toggle_widget(self.gamma, False)
            else:
                toggle_widget(self.T_max_label, True)
                toggle_widget(self.T_min_label, True)
                toggle_widget(self.gamma_label, True)
                toggle_widget(self.T_max, True)
                toggle_widget(self.T_min, True)
                toggle_widget(self.gamma, True)
        except:
            pass

        return data

    def create_element(self, elem_type, line, mat_props):
        if elem_type == "Node-to-node anchor":
            material = create_material("Anchor", mat_props)
            g_i.n2nanchor(line, "Material", material)
        elif elem_type == "Geogrid":
            material = create_material("Geogrid", mat_props)
            g_i.geogrid(line, "Material", material)
        else:
            material = create_material("Embedded", mat_props)
            embeddedbeamrow = g_i.embeddedbeamrow(line, "Material", material)
            embeddedbeamrow.Behaviour = "Grout body"

    def add_anchor(self):
        g_i.gotostructures()
        data = self.get_data()
        x0 = data["x_coordinate"]
        y0 = data["y_coordinate"]
        unbound_props, bound_props = self.anchor_props(data)
        y_unbound = y0 + sin(radians(data["angle"])) * data["unbound_length"]
        y_bound = y_unbound + sin(radians(data["angle"])) * data["bound_length"]
        x_unbound = x0 + cos(radians(data["angle"])) * data["unbound_length"]
        x_bound = x_unbound + cos(radians(data["angle"])) * data["bound_length"]
        line_unbound = g_i.line((x0, y0), (x_unbound, y_unbound))[-1]
        self.create_element("Node-to-node anchor", line_unbound, unbound_props)
        line_bound = g_i.line((x_unbound, y_unbound), (x_bound, y_bound))[-1]
        self.create_element(data["bound_type"], line_bound, bound_props)
        if data["excavation_width"] != 0:
            g_i.line((x0, y0 - 0.5), (x0 + data["excavation_width"], y0 - 0.5))[-1]

        self.anchor_created += 1

    def enter_event(self, event):
        print("Anchor Event")
        try:
            self.add_anchor()
        except Exception as e:
            print(e)


class Loading(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.title = "Sürşarj Yükü Ekleme"
        self.row_no = 0
        self.x_coordinate, _ = add_labeled_input(self, "X Koordinatı")
        self.y_coordinate, _ = add_labeled_input(self, "Y Koordinatı")
        self.length, _ = add_labeled_input(self, "Sürşarj Uzunluğu")
        self.loading_options, _, _ = add_labeled_dropdown(
            self, "Sürşarj Tipi", ["Trafik Yükü", "Bina Yükü"], 1
        )
        self.floor_number, self.floor_number_label = add_labeled_input(
            self, "Kat Sayısı"
        )
        self.unit_load, self.unit_load_label = add_labeled_input(
            self, "Kat Başına Yük(kPa)", 15
        )

    def get_data(self):
        data = {
            "x": convert_float(self.x_coordinate.get()),
            "y": convert_float(self.y_coordinate.get()),
            "length": convert_float(self.length.get()),
            "loading_type": self.loading_options.get(),
            "floor_number": convert_float(self.floor_number.get()),
            "unit_load": convert_float(self.unit_load.get()),
        }

        try:
            if data["loading_type"] == "Trafik Yükü":
                data["load"] = data["unit_load"]
            else:
                data["load"] = data["unit_load"] * data["floor_number"]
        except:
            data["load"] = ""
        try:
            if data["loading_type"] == "Trafik Yükü":
                toggle_widget(self.floor_number_label, False)
                toggle_widget(self.floor_number, False)
                self.unit_load_label.configure(text="Trafik Yükü(kPa)")
            else:
                toggle_widget(self.floor_number_label, True)
                toggle_widget(self.floor_number, True)
                self.unit_load_label.configure(text="Kat Başına Yükü(kPa)")
        except:
            pass

        return data

    def add_surcharge(self):
        data = self.get_data()
        x = data["x"]
        y = data["y"]
        length = data["length"]
        load = data["load"]

        g_i.lineload((x, y), (x + length, y), "qy_start", -1 * load)

    def enter_event(self, event):
        try:
            self.add_surcharge()
        except Exception as e:
            print(e)


# Driver Code
app = tkinterApp()
app.mainloop()
