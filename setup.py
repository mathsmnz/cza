import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

# Initialize data variable and track file path
data = []
current_file_path = None

# Load data from JSON file
def load_from_file():
    global data, current_file_path
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            current_file_path = file_path
            refresh_treeviews()
            messagebox.showinfo("Load", f"Data loaded from {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load JSON file: {e}")

# Save data to JSON file
def save_to_file():
    global current_file_path
    if not current_file_path:
        current_file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    if current_file_path:
        try:
            with open(current_file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Save", f"Data saved to {os.path.basename(current_file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save JSON file: {e}")

# Refresh the group and combo Treeviews with current data
def refresh_treeviews():
    tree_groups.delete(*tree_groups.get_children())
    tree_combos.delete(*tree_combos.get_children())
    for group in data:
        tree_groups.insert("", "end", iid=group["group"], values=(group["group"], group["label"]))

# Show combos of selected group
def show_combos(group_id):
    tree_combos.delete(*tree_combos.get_children())
    for combo in next((g["combos"] for g in data if g["group"] == group_id), []):
        tree_combos.insert("", "end", values=(combo["label"], combo["associated"]))

# Add a new group
def add_group():
    new_group_id = f"Group {len(data) + 1}"
    new_label = "New Group"
    data.append({"group": new_group_id, "label": new_label, "combos": []})
    refresh_treeviews()

# Add a combo to the selected group
def add_combo():
    selected_group = tree_groups.selection()
    if selected_group:
        group_id = selected_group[0]
        for group in data:
            if group["group"] == group_id:
                group["combos"].append({"label": "New Combo", "associated": "Option"})
                show_combos(group_id)
                break
    else:
        messagebox.showwarning("Warning", "No group selected!")

# Delete selected group
def delete_group():
    selected_group = tree_groups.selection()
    if selected_group:
        group_id = selected_group[0]
        if messagebox.askyesno("Delete Group", f"Are you sure you want to delete group '{group_id}'?"):
            global data
            data = [group for group in data if group["group"] != group_id]
            refresh_treeviews()
            tree_combos.delete(*tree_combos.get_children())
    else:
        messagebox.showwarning("Warning", "No group selected!")

# Delete selected combo
def delete_combo():
    selected_combo = tree_combos.selection()
    selected_group = tree_groups.selection()
    if selected_group and selected_combo:
        group_id = selected_group[0]
        combo_index = tree_combos.index(selected_combo[0])
        for group in data:
            if group["group"] == group_id:
                del group["combos"][combo_index]
                show_combos(group_id)
                break
    else:
        messagebox.showwarning("Warning", "No combo selected!")

# Start editing a cell when double-clicked
def edit_cell(event):
    tree = event.widget
    item_id = tree.focus()
    col = tree.identify_column(event.x)

    # Treeview uses "#0" for the first column, so adjust the column index accordingly
    col_num = int(col[1:]) - 1
    x, y, width, height = tree.bbox(item_id, col)

    # Calculate the absolute position relative to the Treeview widget
    abs_x = tree.winfo_rootx() + tree.winfo_x() + x
    abs_y = tree.winfo_rooty() + tree.winfo_y() + y
    
    print(abs_x, tree.winfo_rootx(), tree.winfo_x(), x, sep = " ")
    print(abs_y, tree.winfo_rooty(), tree.winfo_y(), y, sep = " ")


    # Create an entry widget directly on top of the cell
    entry = tk.Entry(root)
    entry.place(x=abs_x, y=abs_y, width=width, height=height)

    # Get current cell value
    current_value = tree.item(item_id, "values")[col_num]
    entry.insert(0, current_value)
    entry.focus()

    def save_edit(event):
        new_value = entry.get()
        entry.destroy()
        
        # Update in Treeview and data
        values = list(tree.item(item_id, "values"))
        values[col_num] = new_value
        tree.item(item_id, values=values)
        
        # Update the corresponding data in the data list
        if tree == tree_groups:
            for group in data:
                if group["group"] == item_id:
                    if col_num == 1:
                        group["label"] = new_value
                    break
        elif tree == tree_combos:
            selected_group = tree_groups.selection()[0]
            combo_index = tree.index(item_id)
            for group in data:
                if group["group"] == selected_group:
                    if col_num == 0:
                        group["combos"][combo_index]["label"] = new_value
                    elif col_num == 1:
                        group["combos"][combo_index]["associated"] = new_value
                    break

    entry.bind("<Return>", save_edit)
    entry.bind("<FocusOut>", lambda e: entry.destroy())  # Destroy if focus is lost

# Create the main window
root = tk.Tk()
root.title("CZA Data Editor")

# Frames for layout organization
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create Treeview for groups
tree_groups = ttk.Treeview(left_frame, columns=("Group ID", "Label"), show="headings", selectmode="browse", height=15)
tree_groups.heading("Group ID", text="Group ID")
tree_groups.heading("Label", text="Label")
tree_groups.column("Group ID", width=100)
tree_groups.column("Label", width=200)
tree_groups.pack(fill=tk.Y, expand=True)
tree_groups.bind("<Double-1>", edit_cell)
tree_groups.bind("<<TreeviewSelect>>", lambda e: show_combos(tree_groups.selection()[0]))

# Create Treeview for combos
tree_combos = ttk.Treeview(right_frame, columns=("Label", "Associated Option"), show="headings", selectmode="browse", height=15)
tree_combos.heading("Label", text="Combo Label")
tree_combos.heading("Associated Option", text="Associated Option")
tree_combos.column("Label", width=150)
tree_combos.column("Associated Option", width=150)
tree_combos.pack(fill=tk.BOTH, expand=True)
tree_combos.bind("<Double-1>", edit_cell)

# Button frame for controls
btn_frame = tk.Frame(left_frame)
btn_frame.pack(pady=10, fill=tk.X)

# Buttons for actions
tk.Button(btn_frame, text="Load from File", command=load_from_file).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
tk.Button(btn_frame, text="Save to File", command=save_to_file).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
tk.Button(btn_frame, text="Add Group", command=add_group).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
tk.Button(btn_frame, text="Delete Group", command=delete_group).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
tk.Button(btn_frame, text="Add Combo", command=add_combo).grid(row=2, column=0, padx=5, pady=5, sticky="ew")
tk.Button(btn_frame, text="Delete Combo", command=delete_combo).grid(row=2, column=1, padx=5, pady=5, sticky="ew")

# Run the application
root.mainloop()
