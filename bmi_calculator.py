import tkinter as tk
from tkinter import messagebox
import customtkinter as ct


class BMIApp:
    """
    BMI Calculator Application.
    BMI stands for Body Mass Index, and it is a measure used to estimate whether a person has a healthy body weight for their height.
    It is calculated by dividing a person's weight in kilograms by the square of their height in meters (BMI = weight / (height^2)).
    The result of this calculation categorizes individuals into different weight status categories,
    which are commonly used to assess health risks associated with weight.

    Here are the typical BMI categories and their interpretations:
        • BMI below 18.5: Underweight
        • BMI between 18.5 and 24.9: Normal weight
        • BMI between 25.0 and 29.9: Overweight
        • BMI of 30 or higher: Obesity
    """
    def __init__(self, root):
        """Initialize the BMI App."""
        self.root = root
        self.root.geometry("400x300")
        self.root.title("BMI Calculator")
        self.setup_ui()

    def setup_ui(self):
        """Setup the UI components."""
        self.create_labels()
        self.create_entries()
        self.create_comboboxes()
        self.create_button()
        self.create_result_label()
        self.create_category_label()

    def create_labels(self):
        """Create weight and height labels."""
        self.weight_label = ct.CTkLabel(self.root, text="Weight", font=FONT_LABEL, text_color="#fff")
        self.weight_label.grid(row=1, column=0, padx=20, pady=20, sticky="w")

        self.height_label = ct.CTkLabel(self.root, text="Height", font=FONT_LABEL, text_color="#fff")
        self.height_label.grid(row=2, column=0, padx=20, pady=20, sticky="w")

    def create_entries(self):
        """Create weight and height entry fields."""
        self.weight_entry = ct.CTkEntry(self.root, font=FONT_LABEL, text_color="#fff", bg_color="#000")
        self.weight_entry.grid(row=1, column=1, padx=20, pady=20)

        self.height_entry = ct.CTkEntry(self.root, font=FONT_LABEL, text_color="#fff", bg_color="#000")
        self.height_entry.grid(row=2, column=1, padx=20, pady=20)

    def create_comboboxes(self):
        """Create weight and height unit comboboxes."""
        self.unit_var1 = ct.StringVar(self.root)
        self.unit_var1.set("kg")
        self.weight_option = ct.CTkComboBox(
            self.root,
            font=FONT_LABEL,
            text_color="#000",
            fg_color="#FFF",
            dropdown_hover_color="#06911F",
            values=["kg", "lbs"],
            variable=self.unit_var1,
            width=80,
        )
        self.weight_option.grid(row=1, column=2, padx=20, pady=20)

        self.unit_var2 = ct.StringVar(self.root)
        self.unit_var2.set("cm")
        self.height_option = ct.CTkComboBox(
            self.root,
            font=FONT_LABEL,
            text_color="#000",
            fg_color="#FFF",
            dropdown_hover_color="#06911F",
            values=["cm", "ft"],
            variable=self.unit_var2,
            width=80,
        )
        self.height_option.grid(row=2, column=2, padx=20, pady=20)

    def create_button(self):
        """Create calculate button."""
        self.calculate_button = ct.CTkButton(
            self.root,
            text="Calculate BMI",
            font=FONT_LABEL,
            text_color="#FFF",
            fg_color="#06911F",
            hover_color="#06911F",
            bg_color="#000",
            cursor="hand2",
            corner_radius=5,
            width=200,
            command=self.calculate_bmi,
        )
        self.calculate_button.grid(row=3, columnspan=3, pady=10)

    def create_result_label(self):
        """Create result label."""
        self.result_label = ct.CTkLabel(self.root, text="", font=FONT_RESULT, text_color="#fff")
        self.result_label.grid(row=4, columnspan=3, padx=10, pady=10)

    def create_category_label(self):
        """Create category label."""
        self.category_label = ct.CTkLabel(
            self.root, text="Category:", font=FONT_RESULT, text_color="#fff", width=20, pady=10
        )
        self.category_label.grid(row=5, columnspan=3)
        self.category_label.grid_forget()  # Initially hide the label

    def calculate_bmi(self):
        """Calculate BMI based on user inputs."""
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())

            if self.unit_var1.get() == "lbs":
                weight *= 0.453592
            if self.unit_var2.get() == "ft":
                height *= 30.48

            bmi = weight / ((height / 100) ** 2)
            self.result_label.configure(text=f"Your BMI is: {bmi:.1f}")

            if bmi < 18.5:
                self.category_label.configure(text="Category: Underweight")
            elif 18.5 <= bmi < 24.9:
                self.category_label.configure(text="Category: Normal weight")
            elif 24.9 <= bmi < 29.9:
                self.category_label.configure(text="Category: Overweight")
            else:
                self.category_label.configure(text="Category: Obesity")

            self.category_label.grid(row=5, columnspan=3)  # Show the label
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number!")
        except ZeroDivisionError:
            messagebox.showerror("Error", "Height cannot be 0!")
            self.category_label.grid_forget()  # Hide the label if there's an error


if __name__ == "__main__":
    root = tk.Tk()
    FONT_TITLE = ("Arial", 30, "bold")
    FONT_LABEL = ("Arial", 18, "bold")
    FONT_RESULT = ("Arial", 24, "bold")
    app = BMIApp(root)
    root.mainloop()
