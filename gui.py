import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from knapsack_solver_0_1 import KnapsackGA01
from knapsack_solver_unbounded import KnapsackUnbounded

class KnapsackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Knapsack Problem Solver")

        self.bg_color = "#2c2c2c"
        self.fg_color = "#ffffff"
        self.button_color = "#444444"
        self.button_hover = "#666666"
        self.highlight_color = "#888888"

        # Configure the root window
        self.root.configure(bg=self.bg_color)

        # Data containers
        self.entries = []

        # Labels and entry fields for number of items and capacity
        tk.Label(root, text="Number of items:", bg=self.bg_color, fg=self.fg_color).pack(pady=(10, 0))
        self.num_items_entry = tk.Entry(root, bg=self.button_color, fg=self.fg_color, insertbackground=self.fg_color)
        self.num_items_entry.pack()

        tk.Label(root, text="Capacity:", bg=self.bg_color, fg=self.fg_color).pack(pady=(10, 0))
        self.capacity_entry = tk.Entry(root, bg=self.button_color, fg=self.fg_color, insertbackground=self.fg_color)
        self.capacity_entry.pack()

        # Buttons
        tk.Button(root, text="Generate Tables", bg=self.button_color,padx=5, fg=self.fg_color, activebackground=self.button_hover,
                command=self.generate_table).pack(pady=10, padx=5)

        self.item_frame = tk.Frame(root, bg=self.bg_color, padx=10, pady=10)
        self.item_frame.pack()

        # Quit button
        tk.Button(root, text="Quit", bg="#aa3333",fg=self.fg_color, activebackground="#bb4444",
                command=self.close_window, padx=7).pack(pady=10, padx=7)

        self.solution_frame = tk.Frame(root, bg=self.bg_color, padx=15, pady=10)
        self.solution_frame.pack()

        self.root.mainloop()

    def generate_table(self):
        num_items = self.validate_data(self.num_items_entry.get(), "Number of items")
        if num_items is None:
            return

        # Clear the item frame
        for widget in self.item_frame.winfo_children():
            widget.destroy()
        self.entries.clear()

        # Create weight and value entry fields dynamically
        for i in range(num_items):
            tk.Label(self.item_frame, text=f"Item {i + 1}:", bg=self.bg_color, fg=self.fg_color).grid(row=i, column=0, padx=5, pady=5, sticky="w")

            tk.Label(self.item_frame, text="Weight:", bg=self.bg_color, fg=self.fg_color).grid(row=i, column=1, padx=5)
            weight_entry = tk.Entry(self.item_frame, bg=self.button_color, fg=self.fg_color, insertbackground=self.fg_color)
            weight_entry.grid(row=i, column=2, padx=5)

            tk.Label(self.item_frame, text="Value:", bg=self.bg_color, fg=self.fg_color).grid(row=i, column=3, padx=5)
            value_entry = tk.Entry(self.item_frame, bg=self.button_color, fg=self.fg_color, insertbackground=self.fg_color)
            value_entry.grid(row=i, column=4, padx=5)

            # Append weight and value entries to the list
            self.entries.append((weight_entry, value_entry))

        calculate_button = tk.Button(
            self.item_frame, text="Calculate", bg=self.button_color, fg=self.fg_color, activebackground=self.button_hover,
            command=self.calculate
        )
        calculate_button.grid(row=num_items, column=0, columnspan=5, pady=10, sticky="ew")

    def calculate(self):
        # Validate the number of items and capacity
        num_items = self.validate_data(self.num_items_entry.get(), "Number of items")
        capacity = self.validate_data(self.capacity_entry.get(), "Capacity")
        if num_items is None or capacity is None:
            return

        items = []
        for i, (weight_entry, value_entry) in enumerate(self.entries):
            weight = self.validate_data(weight_entry.get(), f"Weight of item {i + 1}")
            value = self.validate_data(value_entry.get(), f"Value of item {i + 1}")
            if weight is None or value is None:
                return
            items.append((weight, value))

        # Solve Knapsack problems
        knapsack_ga_01 = KnapsackGA01(items, capacity)
        knapsack_unbounded = KnapsackUnbounded(items, capacity)

        solution_0_1 = knapsack_ga_01.evolution(generations=100, population_size=50, mutation_rate=0.01)
        solution_unbounded = knapsack_unbounded.evolution(generations=200, population_size=75, mutation_rate=0.001)

        # Display solutions
        self.display_solution(solution_0_1, solution_unbounded)

    def display_solution(self, solution_0_1, solution_unbounded):
        solutionMsg = ""
        # Clear previous content in the solution frame
        for widget in self.solution_frame.winfo_children():
            widget.destroy()

        # Table header
        tk.Label(self.solution_frame, text="Knapsack 0/1", font=("Arial", 14, "bold"), bg=self.bg_color, fg=self.fg_color).grid(row=0, column=0, padx=10, pady=10)
        ttk.Separator(self.solution_frame, orient='vertical').grid(row=0, column=1, rowspan=10, sticky="ns", padx=10)
        tk.Label(self.solution_frame, text="Knapsack Unbounded", font=("Arial", 14, "bold"), bg=self.bg_color, fg=self.fg_color).grid(row=0, column=2, padx=10, pady=10)

        for i in range(len(solution_0_1[0])):
            solutionMsg += f"item {i+1} : {solution_0_1[0][i]}\n"

        # Knapsack 0/1 Solution
        tk.Label(self.solution_frame, text="Best Profit:", bg=self.bg_color, fg=self.fg_color).grid(row=1, column=0, sticky="w", padx=10)
        tk.Label(self.solution_frame, text=str(solution_0_1[1]), bg=self.bg_color, fg=self.fg_color).grid(row=2, column=0, sticky="w", padx=10)

        tk.Label(self.solution_frame, text="Best Solution:", bg=self.bg_color, fg=self.fg_color).grid(row=3, column=0, sticky="w", padx=10)
        tk.Message(self.solution_frame, text=solutionMsg, bg=self.bg_color, fg=self.fg_color).grid(row=4, column=0, sticky="w", padx=10)
        
        solutionMsg = ""
        for i in range(len(solution_unbounded[0])):
            solutionMsg += f"item {i+1} : {solution_unbounded[0][i]}\n"

        # Knapsack Unbounded Solution
        tk.Label(self.solution_frame, text="Best Profit:", bg=self.bg_color, fg=self.fg_color).grid(row=1, column=2, sticky="w", padx=10)
        tk.Label(self.solution_frame, text=str(solution_unbounded[1]), bg=self.bg_color, fg=self.fg_color).grid(row=2, column=2, sticky="w", padx=10)

        tk.Label(self.solution_frame, text="Best Solution:", bg=self.bg_color, fg=self.fg_color).grid(row=3, column=2, sticky="w", padx=10)
        tk.Message(self.solution_frame, text=solutionMsg, bg=self.bg_color, fg=self.fg_color).grid(row=4, column=2, sticky="w", padx=10)

    def validate_data(self, data, field_name):
        try:
            num = int(data)
            if num <= 0:
                raise ValueError
            return num
        except ValueError:
            messagebox.showerror("ERROR", f"Invalid input for {field_name}: Please enter a valid positive integer")
            return None

    def close_window(self):
        self.root.destroy()


#Main application
if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(500, 350)
    KnapsackGUI(root)