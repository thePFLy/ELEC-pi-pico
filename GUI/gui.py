import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # window
        self.title("Elec - project")
        self.geometry(f"{600}x{390}")

        # configure grid
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        # create sidebar
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Elec - project", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        

        # create main entry + button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Minimal distance")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, command = self.sidebar_button_event,text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.main_button_1.configure(text="Change minimal distance")

        # create slider + progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.slider_2 = customtkinter.CTkSlider(master=self.slider_progressbar_frame, from_=20, to=400, number_of_steps=380,orientation="vertical", command=self.slider_event)
        self.slider_2.grid(row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")


        # create numbers displayer
        # displayer of distance
        self.distance_displayer: str = '0'
        self.label_distance = customtkinter.CTkLabel(self.master, text=self.distance_displayer, font=customtkinter.CTkFont(size=100, weight="bold"))
        self.label_distance.place(relx=0.53, rely=0.4, anchor='center')

        # change distance displayer
        self.distance_change_displayer: str = '50'
        self.label_distance = customtkinter.CTkLabel(self.master, text=self.distance_change_displayer, font=customtkinter.CTkFont(size=50, weight="bold"), text_color='#3579ae')
        self.label_distance.place(relx=0.8, rely=0.4, anchor='center')
        self.distance_change_displayer_format: str = 'cm'
        self.label_distance_format = customtkinter.CTkLabel(self.master, text=self.distance_change_displayer_format, font=customtkinter.CTkFont(size=20, weight="normal"), text_color='#3579ae')
        self.label_distance_format.place(relx=0.8, rely=0.5, anchor='center')


    def slider_event(self, value):
        self.entry.delete(0, len(self.entry.get()))
        value_int = int(value)
        self.entry.insert(0, str(value_int))
        

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)


    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


    def sidebar_button_event(self):
        if self.entry.get().isnumeric() and 20 <= int(self.entry.get()) <= 400:
            self.distance_change_displayer = self.entry.get()
            self.label_distance.configure(text=self.distance_change_displayer)
            self.slider_2.set(int(self.entry.get()))
        else:
            print("no valid arg entered")
            pass


if __name__ == "__main__":
    app = App()
    app.mainloop()