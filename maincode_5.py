import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
import pymysql

# Connect to MySQL
db = pymysql.connect(
    host="localhost",
    user="root",
    password="Hresy@wa2",
    database="CarRentalSystem"
)

cursor = db.cursor()
cursor.execute("SELECT Model, DailyPrice, PlateNo, `Condition`, Mileage FROM Vehicle WHERE Availability = TRUE")
car_data = cursor.fetchall()
cars = []
for model, price, plate_no, condition, mileage in car_data:
    if "maruti" in model.lower() or "hyundai" in model.lower():
        continue  # Skip Maruti and Hyundai
    image_file = model.lower().replace(" ", "") + ".webp"  
    cars.append({
        "name": model,
        "image": image_file,
        "price": float(price),
        "plate_no": plate_no,
        "condition": condition,
        "mileage": mileage
    })
cars = cars[:4]  # Keep only first 4 cars

class CarRentalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Car Rental System")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f2f5")

        # Header
        self.header = tk.Label(self.root, text="Car Rental System", font=("Segoe UI", 28, "bold"), fg="#2c3e50", bg="#f0f2f5")
        self.header.pack(pady=20)

        # Car display frame
        self.car_list_frame = tk.Frame(self.root, bg="#f0f2f5")
        self.car_list_frame.pack(pady=10)

        self.car_images = []
        self.car_labels = []
        self.car_buttons = []

        for car in cars:
            car_item = self.create_car_item(car)
            self.car_images.append(car_item['image'])
            self.car_labels.append(car_item['label'])
            self.car_buttons.append(car_item['button'])

        # Scrollable booking section
        self.booking_frame = tk.Frame(self.root, bg="#f0f2f5")
        self.booking_frame.pack(pady=20, fill="both", expand=True)

        self.canvas = tk.Canvas(self.booking_frame, bg="#f0f2f5", highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.booking_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_window = tk.Frame(self.canvas, bg="#f0f2f5")
        self.canvas.create_window((0, 0), window=self.scrollable_window, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.setup_booking_fields()

        # Footer
        self.footer = tk.Label(self.root, text="© 2024 Car Rental System", font=("Segoe UI", 10), fg="#888", bg="#f0f2f5")
        self.footer.pack(pady=10)

    def setup_booking_fields(self):
        fields = [
            ("Customer Name:", "name_entry"),
            ("Driving Licence:", "licence_entry"),
            ("House No:", "house_no_entry"),
            ("City:", "city_entry"),
            ("Country:", "country_entry"),
            ("Contact No:", "contact_no_entry"),
            ("Address:", "address_entry"),
            ("Pickup Date (YYYY-MM-DD):", "pickup_entry"),
            ("Return Date (YYYY-MM-DD):", "return_entry")
        ]

        for label_text, var_name in fields:
            label = tk.Label(self.scrollable_window, text=label_text, font=("Segoe UI", 12), bg="#f0f2f5", anchor="w")
            label.pack(fill="x", padx=10, pady=(10, 0))
            entry = tk.Entry(self.scrollable_window, font=("Segoe UI", 12), bd=1, relief="solid", bg="#ffffff", fg="#333333")
            entry.pack(fill="x", padx=10)
            setattr(self, var_name, entry)

        # Car selection
        self.car_label = tk.Label(self.scrollable_window, text="Select Car:", font=("Segoe UI", 12), bg="#f0f2f5")
        self.car_label.pack(pady=(10, 0))
        self.car_select = tk.StringVar(self.scrollable_window)
        self.car_select.set(cars[0]['name'])
        self.car_menu = tk.OptionMenu(self.scrollable_window, self.car_select, *[car['name'] for car in cars])
        self.car_menu.config(font=("Segoe UI", 12), bg="#ffffff", fg="#333333", bd=1, relief="solid")
        self.car_menu.pack()

        # Booking button
        self.book_button = tk.Button(self.scrollable_window, text="Book Now", command=self.book_car,
                                     font=("Segoe UI", 14, "bold"), bg="#009688", fg="white",
                                     activebackground="#00796B", activeforeground="white", relief="flat", bd=0)
        self.book_button.pack(pady=20)

        self.scrollable_window.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def create_car_item(self, car):
        frame = tk.Frame(self.car_list_frame, bg="#ffffff", bd=2, relief="ridge")
        frame.pack(side="left", padx=15, pady=10)

        try:
            img = Image.open(car["image"])
            img = img.resize((280, 180))
            img_tk = ImageTk.PhotoImage(img)
            img_label = tk.Label(frame, image=img_tk, bg="#ffffff")
            img_label.image = img_tk
            img_label.pack()
        except Exception:
            img_label = tk.Label(frame, text="Image Not Available", bg="#ffffff", fg="#888888")
            img_label.pack()

        name_label = tk.Label(frame, text=car["name"], font=("Segoe UI", 14, "bold"), bg="#ffffff")
        name_label.pack()

        plate_label = tk.Label(frame, text=f"Plate No: {car['plate_no']}", bg="#ffffff")
        plate_label.pack()

        condition_label = tk.Label(frame, text=f"Condition: {car['condition']}", bg="#ffffff")
        condition_label.pack()

        mileage_label = tk.Label(frame, text=f"Mileage: {car['mileage']} km", bg="#ffffff")
        mileage_label.pack()

        price_label = tk.Label(frame, text=f"${car['price']}/day", font=("Segoe UI", 12, "bold"), fg="#009688", bg="#ffffff")
        price_label.pack()

        button = tk.Button(frame, text="Select", command=lambda: self.select_car(car),
                           bg="#00796B", fg="white", font=("Segoe UI", 11, "bold"),
                           relief="flat", activebackground="#004d40")
        button.pack(pady=5)

        return {"image": img_label, "label": name_label, "button": button}

    def select_car(self, car):
        self.car_select.set(car['name'])

    def book_car(self):
        name = self.name_entry.get()
        licence = self.licence_entry.get()
        house_no = self.house_no_entry.get()
        city = self.city_entry.get()
        country = self.country_entry.get()
        contact_no = self.contact_no_entry.get()
        address = self.address_entry.get()
        pickup = self.pickup_entry.get()
        return_ = self.return_entry.get()
        car_model = self.car_select.get()

        if not all([name, licence, house_no, city, country, contact_no, address, pickup, return_]):
            messagebox.showerror("Error", "Please fill all fields.")
            return

        try:
            cursor.execute("SELECT VehicleID FROM Vehicle WHERE Model = %s", (car_model,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Error", "Selected car not found.")
                return
            vehicle_id = result[0]

            name_parts = name.strip().split(" ")
            fname = name_parts[0]
            lname = name_parts[1] if len(name_parts) > 1 else ""

            cursor.execute("""
                INSERT INTO Customer (FName, LName, HouseNo, City, Country, Address, ContactNo, DrivingLicence)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (fname, lname, house_no, city, country, address, contact_no, licence))
            cust_id = cursor.lastrowid

            try:
                d1 = datetime.strptime(pickup, "%Y-%m-%d")
                d2 = datetime.strptime(return_, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid dates in YYYY-MM-DD format.")
                return

            num_days = (d2 - d1).days
            if num_days < 1:
                raise ValueError("Return date must be after pickup date.")

            cursor.execute("""
                INSERT INTO Reservation (CustID, VehicleID, PickupDate, ReturnDate, NoOfDays, PickupLocation)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (cust_id, vehicle_id, pickup, return_, num_days, "Main Branch"))

            db.commit()
            messagebox.showinfo("Success", f"{car_model} booked successfully for {name}!")
        except Exception as e:
            messagebox.showerror("Booking Failed", str(e))

# Run the app
root = tk.Tk()
app = CarRentalApp(root)
root.mainloop()
