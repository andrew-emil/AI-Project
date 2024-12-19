import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import numpy as np
from knapsack_solver_0_1 import KnapsackGA01
from knapsack_solver_unbounded import KnapsackUnbounded
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class KnapsackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Knapsack Problem Solver")
        self.root.minsize(600, 400)

        # Define color scheme
        self.bg_color = "#2c2c2c"
        self.fg_color = "#ffffff"
        self.button_color = "#444444"
        self.button_hover = "#666666"
        self.error_color = "#aa3333"
        self.success_color = "#33aa33"

        self.root.configure(bg=self.bg_color)
        self.entries = []
        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        """Create main widgets for the GUI."""
        # Header Label
        header_label = tk.Label(self.root, text="Knapsack Problem Solver", font=("Arial", 16, "bold"),
                                bg=self.bg_color, fg=self.fg_color)
        header_label.pack(pady=10)

        # Inputs for number of items and capacity
        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Number of Items:", bg=self.bg_color, fg=self.fg_color).grid(row=0, column=0, padx=5)
        self.num_items_entry = tk.Entry(input_frame, bg=self.button_color, fg=self.fg_color, insertbackground=self.fg_color)
        self.num_items_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Capacity:", bg=self.bg_color, fg=self.fg_color).grid(row=1, column=0, padx=5)
        self.capacity_entry = tk.Entry(input_frame, bg=self.button_color, fg=self.fg_color, insertbackground=self.fg_color)
        self.capacity_entry.grid(row=1, column=1, padx=5)

        # Buttons
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Generate Tables", bg=self.button_color, fg=self.fg_color,
                activebackground=self.button_hover, command=self.generate_table).pack(side="left", padx=5)
        tk.Button(button_frame, text="Quit", bg=self.error_color, fg=self.fg_color,
                activebackground="#bb4444", command=self.close_window).pack(side="right", padx=5)

        # Frame for dynamically added item entries
        self.item_frame = tk.Frame(self.root, bg=self.bg_color)
        self.item_frame.pack(pady=10)

        # Frame for displaying solutions
        self.solution_frame = tk.Frame(self.root, bg=self.bg_color)
        self.solution_frame.pack(pady=10)

    def generate_table(self):
        """Generate input fields for item weights and values."""
        num_items = self.validate_data(self.num_items_entry.get(), "Number of Items")
        if num_items is None:
            return

        # Clear previous entries
        for widget in self.item_frame.winfo_children():
            widget.destroy()
        self.entries.clear()

        # Create input fields for each item
        tk.Label(self.item_frame, text="Enter Weights and Values:", bg=self.bg_color, fg=self.fg_color,
                font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=4, pady=10)

        for i in range(num_items):
            tk.Label(self.item_frame, text=f"Item {i + 1}:", bg=self.bg_color, fg=self.fg_color).grid(row=i + 1, column=0, padx=5)
            tk.Label(self.item_frame, text="Weight:", bg=self.bg_color, fg=self.fg_color).grid(row=i + 1, column=1, padx=5)
            weight_entry = tk.Entry(self.item_frame, bg=self.button_color, fg=self.fg_color, insertbackground=self.fg_color)
            weight_entry.grid(row=i + 1, column=2, padx=5)

            tk.Label(self.item_frame, text="Value:", bg=self.bg_color, fg=self.fg_color).grid(row=i + 1, column=3, padx=5)
            value_entry = tk.Entry(self.item_frame, bg=self.button_color, fg=self.fg_color, insertbackground=self.fg_color)
            value_entry.grid(row=i + 1, column=4, padx=5)

            # Store weight and value entry fields
            self.entries.append((weight_entry, value_entry))

        # Add Calculate Button
        tk.Button(self.item_frame, text="Calculate", bg=self.success_color, fg=self.fg_color,
                activebackground="#55aa55", command=self.calculate).grid(row=num_items + 1, column=0, columnspan=5, pady=10)

    def calculate(self):
        """Calculate solutions for the knapsack problem."""
        num_items = self.validate_data(self.num_items_entry.get(), "Number of Items")
        capacity = self.validate_data(self.capacity_entry.get(), "Capacity")
        if num_items is None or capacity is None:
            return

        items = []
        for i, (weight_entry, value_entry) in enumerate(self.entries):
            weight = self.validate_data(weight_entry.get(), f"Weight of Item {i + 1}")
            value = self.validate_data(value_entry.get(), f"Value of Item {i + 1}")
            if weight is None or value is None:
                return
            items.append((weight, value))

        # Solve Knapsack problem (0/1 and Unbounded)
        solution_0_1 = self.solve_knapsack_01(items, capacity)
        solution_unbounded = self.solve_knapsack_unbounded(items, capacity)
        
        
        fitness_values_01 = solution_0_1[-1]
        fitness_values_unbounded = solution_unbounded[-1]
        # last_200_fitness_values_01 = fitness_values_01[-200:]
        # last_200_fitness_values_unbounded = fitness_values_unbounded[-200:]
        

        self.display_solution(solution_0_1, solution_unbounded, fitness_values_01=fitness_values_01, fitness_values_unbounded=fitness_values_unbounded)
        
    def create_plots(self, fitness_01_values, fitness_unbounded_values):
        # Simulate data for plots
        generations = range(1, 201)

        # Create fitness progress plot
        plt.figure(figsize=(10, 6))
        plt.plot(generations, fitness_01_values, label="Knapsack 0/1", color="blue")
        plt.plot(generations, fitness_unbounded_values, label="Knapsack Unbounded", color="green")
        plt.title("Fitness Progress Over Generations")
        plt.xlabel("Generations")
        plt.ylabel("Fitness Value")
        plt.legend()
        plt.grid(True)
        plt.savefig("fitness_progress.png")

        # Simulate data for execution time
        algorithms = ["Knapsack 0/1", "Knapsack Unbounded"]
        execution_time = [1.5, 2.3]  # in seconds

        # Create execution time comparison bar chart
        plt.figure(figsize=(8, 5))
        plt.bar(algorithms, execution_time, color=["blue", "green"])
        plt.title("Execution Time Comparison")
        plt.ylabel("Time (seconds)")
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.savefig("execution_time_comparison.png")

    def display_solution(self, solution_0_1, solution_unbounded,fitness_values_01,  fitness_values_unbounded):
        self.create_plots(fitness_01_values=fitness_values_01, fitness_unbounded_values=fitness_values_unbounded)
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
        """Validate input data as a positive integer."""
        try:
            value = int(data)
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            messagebox.showerror("Input Error", f"Invalid input for {field_name}. Please enter a positive integer.")
            return None

    def solve_knapsack_01(self, items, capacity):
        obj = KnapsackGA01(items, capacity)
        result = obj.evolution(generations=200, population_size=100, mutation_rate=0.01)
        return result

    def solve_knapsack_unbounded(self, items, capacity):
        obj = KnapsackUnbounded(items, capacity)
        result = obj.evolution(generations=200, population_size=100, mutation_rate=0.01)
        return result

    def close_window(self):
        self.root.destroy()

#Main application
if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(500, 350)
    KnapsackGUI(root)