import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from knapsack_solver_0_1 import KnapsackGA01
from knapsack_solver_unbounded import KnapsackUnbounded

class KnapsackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Knapsack Problem Solver")
        self.best_solution0_1 = ""
        self.best_profit0_1 = ""
        self.best_solution_unbounded = ""
        self.best_profit_unbounded = ""

        # Create labels and entry fields for number of items and capacity
        self.num_items_label = tk.Label(root, text="Number of items:")
        self.num_items_label.pack()
        self.num_items_entry = tk.Entry(root)
        self.num_items_entry.pack()
        self.solution_frame = tk.Frame(root, padx=15, pady=10)

        self.capacity_label = tk.Label(root, text="Capacity:")
        self.capacity_label.pack()
        self.capacity_entry = tk.Entry(root)
        self.capacity_entry.pack()
        
        self.button = tk.Button(root, text="Generate Tables" , padx=5, pady=5, bg="royalblue", foreground='white', activebackground='royalblue', activeforeground='white', command=self.generate_table)
        self.button.pack()
        
        self.item_frame = tk.Frame(root, padx=5, pady=5)
        self.item_frame.pack()
        
        
        
        self.solution_frame.pack()
        
        self.root.mainloop()

    def generate_table(self):
        num_items = self.validate_data(self.num_items_entry.get())
        
        if num_items == 0:
            messagebox.showerror("ERROR", "Please enter a number of items bigger than zero")
            return

        # Clear the item frame
        for widget in self.item_frame.winfo_children():
            widget.destroy()

        for i in range(num_items):
            item_label = tk.Label(self.item_frame, text=f"Item {i+1}:")
            item_label.grid(row=i, column=0)

            weight_label = tk.Label(self.item_frame, text="Weight:")
            weight_label.grid(row=i, column=1)
            weight_entry = tk.Entry(self.item_frame)
            weight_entry.grid(row=i, column=2)

            value_label = tk.Label(self.item_frame, text="Value:")
            value_label.grid(row=i, column=3)
            value_entry = tk.Entry(self.item_frame)
            value_entry.grid(row=i, column=4)
        
        self.button = tk.Button(self.item_frame, text="Calculate" , padx=5, pady=5, bg="royalblue", foreground='white', activebackground='royalblue', activeforeground='white', command=self.calculate,justify='left')
        self.button.grid(row=num_items, column=2)


    def calculate(self):
        num_items = self.validate_data(self.num_items_entry.get())
        capacity = self.validate_data(self.capacity_entry.get())
        items = []

        for i in range(num_items):
            weight_entry = self.item_frame.grid_slaves(row=i, column=2)[0]
            value_entry = self.item_frame.grid_slaves(row=i, column=4)[0]
            weight = self.validate_data(weight_entry.get())
            if weight == None:
                return
            value = self.validate_data(value_entry.get())
            if value == None:
                return
            items.append((weight, value))

        knapsack_ga_01 = KnapsackGA01(items, capacity)
        knapsack_unbounded = KnapsackUnbounded(items, capacity)
        best_solution, best_profit = knapsack_ga_01.evolution(generations=100, population_size=50, mutation_rate=0.01)
        solution_0_1 = [best_solution, best_profit]
        best_solution, best_profit = knapsack_unbounded.evolution(generations=200, population_size=75, mutation_rate=0.001)
        solution_unbounded = [best_solution, best_profit]
        
        #print the output in the GUI
        self.generate_solution(solution_0_1=solution_0_1, solution_unbounded=solution_unbounded)

    def generate_solution(self, solution_0_1: list, solution_unbounded: list):
        # Extract the best profits and solutions
        self.best_profit0_1 = solution_0_1[1]
        self.best_solution0_1 = solution_0_1[0]
        self.best_profit_unbounded = solution_unbounded[1]
        self.best_solution_unbounded = solution_unbounded[0]

        # Clear previous content in the frame (if any)
        for widget in self.solution_frame.winfo_children():
            widget.destroy()
        
        
        # table header
        tk.Label(self.solution_frame, text="Knapsack 0/1", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10, pady=10)
        ttk.Separator(self.solution_frame, orient='vertical').grid(row=0, column=1, rowspan=10, sticky="ns", padx=10)
        tk.Label(self.solution_frame, text="Knapsack Unbounded", font=("Arial", 14, "bold")).grid(row=0, column=2, padx=10, pady=10)
        
        # Knapsack 0/1 Solution (Left)
        tk.Label(self.solution_frame, text="Best Profit:").grid(row=1, column=0, sticky="w", padx=10)
        tk.Label(self.solution_frame, text=str(self.best_profit0_1)).grid(row=2, column=0, sticky="w", padx=10)

        tk.Label(self.solution_frame, text="Best Solution:").grid(row=3, column=0, sticky="w", padx=10)
        tk.Label(self.solution_frame, text=str(self.best_solution0_1)).grid(row=4, column=0, sticky="w", padx=10)

        # Knapsack Unbounded Solution (Right)
        tk.Label(self.solution_frame, text="Best Profit:").grid(row=1, column=2, sticky="w", padx=10)
        tk.Label(self.solution_frame, text=str(self.best_profit_unbounded)).grid(row=2, column=2, sticky="w", padx=10)

        tk.Label(self.solution_frame, text="Best Solution:").grid(row=3, column=2, sticky="w", padx=10)
        tk.Label(self.solution_frame, text=str(self.best_solution_unbounded)).grid(row=4, column=2, sticky="w", padx=10)

    def validate_data(self, data: str):
        try:
            num = int(data)
            
            if num < 0:
                raise ValueError("Number must be greater than or equal to 0")
            
            return num

        except ValueError as e:
            if e != "Number must be greater than or equal to 0":
                messagebox.showerror("ERROR", "Invalid input: Please enter a valid number")
            else:
                messagebox.showerror("ERROR", f"Invalid input: {str(e)}")