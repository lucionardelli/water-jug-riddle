import tkinter as tk

from jug_riddle import Jug, JugAction, JugRiddle, UnsolvableRiddle, solve


class WaterJugGUI:
    """
    A GUI application for solving the Water Jug Riddle.
    Allows the user to input jug capacities and a goal, and interactively solve the riddle or use auto-solve
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Water Jug Riddle")

        # Create frames for input and riddle steps
        self.input_frame = InputFrame(self.root, self.show_riddle_frame)
        self.riddle_frame = None

        # Start with the input frame
        self.input_frame.display_input()

    def show_riddle_frame(self, jug1_capacity, jug2_capacity, goal):
        """
        Switch to the riddle frame to display the riddle-solving interface.

        Args:
            jug1_capacity (int): Capacity of Jug 1.
            jug2_capacity (int): Capacity of Jug 2.
            goal (int): The goal amount of water to achieve.
        """
        self.input_frame.frame.pack_forget()
        self.riddle_frame = RiddleFrame(self.root, jug1_capacity, jug2_capacity, goal)
        self.riddle_frame.display_riddle()


class InputFrame:
    """
    A frame for user input of jug capacities and goal.

    Args:
        root (tk.Tk): The root tkinter window.
        switch_to_riddle (function): A function to switch to the riddle frame.
    """

    def __init__(self, root, switch_to_riddle):
        self.root = root
        self.switch_to_riddle = switch_to_riddle
        self.frame = tk.Frame(self.root)

        # Labels and Entry widgets for jug capacities and goal
        tk.Label(self.frame, text="Jug 1 Capacity:").grid(row=0, column=0)
        self.jug1_capacity_entry = tk.Entry(self.frame)
        self.jug1_capacity_entry.grid(row=0, column=1)

        tk.Label(self.frame, text="Jug 2 Capacity:").grid(row=1, column=0)
        self.jug2_capacity_entry = tk.Entry(self.frame)
        self.jug2_capacity_entry.grid(row=1, column=1)

        tk.Label(self.frame, text="Goal:").grid(row=2, column=0)
        self.goal_entry = tk.Entry(self.frame)
        self.goal_entry.grid(row=2, column=1)

        # Button to start the riddle
        self.start_button = tk.Button(
            self.frame, text="Start", command=self.start_riddle
        )
        self.start_button.grid(row=3, columnspan=2)

    def display_input(self):
        # Pack the input frame to display it
        self.frame.pack()

    def start_riddle(self):
        # Get the values from the Entry widgets
        jug1_capacity = int(self.jug1_capacity_entry.get())
        jug2_capacity = int(self.jug2_capacity_entry.get())
        goal = int(self.goal_entry.get())

        # Call the switch function to show the riddle frame
        self.switch_to_riddle(jug1_capacity, jug2_capacity, goal)


class RiddleFrame:
    """
    A frame for solving (manually or automatically) the Water Jug Riddle.

    Args:
        root (tk.Tk): The root tkinter window.
        jug1_capacity (int): Capacity of Jug 1.
        jug2_capacity (int): Capacity of Jug 2.
        goal (int): The goal amount of water to achieve.
    """

    def __init__(self, root, jug1_capacity, jug2_capacity, goal):
        self.root = root
        self.riddle = JugRiddle(jug1_capacity, jug2_capacity, goal)
        self.unsolvable = False
        self.current_state = 0
        self.frame = tk.Frame(self.root)
        self.frame.pack(expand=True, fill="both")
        self.chose_mode = True
        self.action_jug = None

    def draw_jug(self, canvas, capacity, current_water):
        """
        Draws thw jug in the given canvas. The jug is drawn as a rectangle with
        white and blue colors representing how full the jug is.
        The jug is all white when empty, and the blue is drawn bottom up in relation
        on how full the jug is.
        """
        water_level = 200 - (current_water * 200 / capacity)
        canvas.create_rectangle(20, 0, 80, water_level, fill="white")
        canvas.create_rectangle(20, water_level, 80, 200, fill="blue")
        canvas.create_text(50, 190, text=f"{current_water}/{capacity}")
        canvas.pack(side="left", padx=10)

    def display_stepper(self):
        # Buttons for moving through states
        if 0 < self.current_state:
            back_state = "normal"
        else:
            back_state = "disabled"
        tk.Button(
            self.frame, text="<<", command=self.previous_action, state=back_state
        ).pack(side="left", padx=10)

        if self.current_state == 0:
            action_msg = "Initial State"
        elif len(self.riddle) == 0:
            action_msg = "No actions yet"
        else:
            action_msg = f"Action {self.current_state} / {len(self.riddle)}"
        tk.Message(self.frame, text=action_msg, font="Arial 8").pack(
            side="left", padx=10
        )

        if len(self.riddle) <= self.current_state:
            next_state = "disabled"
        else:
            next_state = "normal"
        tk.Button(
            self.frame, text=">>", command=self.next_action, state=next_state
        ).pack(side="left", padx=10)

    def display_message_area(self):
        # Create text widget to show the actions taken there
        text_area = tk.Text(self.frame, height=5, width=52)
        if self.unsolvable:
            text_area.insert(tk.END, "*** RIDDLE IS UNSOLVABLE! ***")
        for idx, (action, jug) in enumerate(
            self.riddle._actions[0 : self.current_state]
        ):
            text_area.insert(tk.END, f"Step {idx+1}: {action.name} JUG {jug.value}\n")
        text_area.pack(side="left", padx=10, pady=5)

    def display_manual_controls(self):
        tk.Radiobutton(
            self.frame,
            text="Jug 2",
            variable=self.action_jug,
            indicatoron=False,
            value=Jug.JUG_2.name,
            width=8,
        ).pack(side="right")
        tk.Radiobutton(
            self.frame,
            text="Jug 1",
            variable=self.action_jug,
            indicatoron=False,
            value=Jug.JUG_1.name,
            width=8,
        ).pack(side="right")

        tk.Button(self.frame, text="Fill", command=self.fill_action).pack(side="right")
        tk.Button(self.frame, text="Empty", command=self.empty_action).pack(
            side="right"
        )
        tk.Button(self.frame, text="Transfer", command=self.transfer_action).pack(
            side="right"
        )

    def display_riddle(self):
        # Create two Canvas widgets to draw the jugs
        jug1_canvas = tk.Canvas(self.frame, width=100, height=200, bg="white")
        jug2_canvas = tk.Canvas(self.frame, width=100, height=200, bg="white")

        self.draw_jug(
            jug1_canvas,
            self.riddle.jug_1_capacity,
            self.riddle._states[self.current_state].jug_1,
        )
        self.draw_jug(
            jug2_canvas,
            self.riddle.jug_2_capacity,
            self.riddle._states[self.current_state].jug_2,
        )

        # Buttons for solving or playing
        if self.chose_mode:
            tk.Button(
                self.frame, text="Solve Manually", command=self.play_riddle
            ).pack()
            tk.Button(
                self.frame, text="Solve Automatically", command=self.solve_riddle
            ).pack()
        else:
            self.display_stepper()
            self.display_message_area()
            if self.action_jug is not None:
                self.display_manual_controls()

        # Pack the riddle frame to display it
        self.frame.pack()

    def fill_action(self):
        self.riddle.take_action(Jug[self.action_jug.get()], JugAction.FILL)
        self.current_state += 1
        self.refresh()

    def empty_action(self):
        self.riddle.take_action(Jug[self.action_jug.get()], JugAction.EMPTY)
        self.current_state += 1
        self.refresh()

    def transfer_action(self):
        self.riddle.take_action(Jug[self.action_jug.get()], JugAction.TRANSFER)
        self.current_state += 1
        self.refresh()

    def refresh(self):
        # Force a refresh of the frame
        self.frame.update()
        self.frame.update_idletasks()
        # Clear the frame to remove previous jugs and buttons
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.display_riddle()

    def previous_action(self):
        self.current_state = max(self.current_state - 1, 0)
        if self.action_jug is not None:
            # We are playing manually. We need to modify the sate of the riddle.
            self.riddle.undo_last_action()
        self.refresh()

    def next_action(self):
        self.current_state = min(self.current_state + 1, len(self.riddle))
        self.refresh()

    def solve_riddle(self):
        self.chose_mode = False
        try:
            self.riddle = solve(self.riddle)
        except UnsolvableRiddle:
            self.unsolvable = True
        self.current_state = 0  # Reset the current state
        self.refresh()

    def play_riddle(self):
        self.chose_mode = False
        self.action_jug = tk.StringVar(value=Jug.JUG_1.name)
        self.refresh()


def water_jug_riddle_ui():
    """Run the Water Jug Riddle GUI application."""
    root = tk.Tk()
    WaterJugGUI(root)
    root.mainloop()
