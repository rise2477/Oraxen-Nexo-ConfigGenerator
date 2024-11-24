import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from zipfile import ZipFile
import os
import yaml
from collections import defaultdict

root = tk.Tk()
root.title("File Uploader")
root.geometry("500x700")
root.configure(bg="#252526")

font_style = ("Segoe UI", 12)

option_var = tk.StringVar()

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("Zip files", "*.zip")])
    if file_path:
        read_zip(file_path)

def read_zip(file_path):
    try:
        with ZipFile(file_path, 'r') as zip_file:
            files = zip_file.namelist()
            
            option_label.pack(pady=5)
            option_menu.pack(pady=5)
            
            item_list.delete(0, tk.END)
            for file in files:
                item_list.insert(tk.END, file)
                
    except Exception as e:
        messagebox.showerror("Error", f"Cannot read zip file: {e}")

def show_icon_inputs():
    ascent_label.pack()
    ascent_entry.pack()
    height_label.pack()
    height_entry.pack()

def show_material_input():
    material_label.pack()
    material_entry.pack()

def hide_inputs():
    ascent_label.pack_forget()
    ascent_entry.pack_forget()
    height_label.pack_forget()
    height_entry.pack_forget()
    material_label.pack_forget()
    material_entry.pack_forget()

def option_selected(*args):
    selected_type = option_var.get()
    hide_inputs()
    if selected_type == "Icons":
        show_icon_inputs()
    elif selected_type == "Items(3d)":
        show_material_input()

def process_files():
    selected_type = option_var.get() or "Icons"
    output = {}
    
    if selected_type == "Items(2d)":
        for item in item_list.get(0, tk.END):
            if item.lower().endswith((".png", ".jpg", ".jpeg")):
                item_name_key = os.path.splitext(os.path.basename(item))[0]
                item_name_display = item_name_key.replace("_", " ").title()
                
                file_data = {
                    "itemname": item_name_display,
                    "material": "PAPER",
                    "Pack": {
                        "generate_model": True,
                        "parent_model": "item/generated",
                        "textures": [f"{item}"]
                    }
                }
                output[item_name_key] = file_data
            elif item.lower().endswith(("_chestplate.png", "_helmet.png", "_leggings.png", "_boots.png")):
                prefix = item_name_key.split('_')[0]
                color = color_map[prefix]
                
                file_data = {
                    "itemname": item_name_display,
                    "material": "LEATHER_HELMET",
                    "Pack": {
                        "generate_model": True,
                        "parent_model": "item/generated",
                        "textures": [f"{item}"]
                    },
                    "color": color
                }
                output[item_name_key] = file_data
    elif selected_type == "Blocks":
        for item in item_list.get(0, tk.END):
            if item.lower().endswith((".png", ".jpg", ".jpeg")):
                item_name_key = os.path.splitext(os.path.basename(item))[0]
                item_name_display = item_name_key.replace("_", " ").title()
                file_data = {
                    "displayname": item_name_display,
                    "material": "PAPER",
                    "Pack": {
                      "generate_model": True,
                      "parent_model": "block/cube_all",
                      "textures": [f"{item}"]
                    }
                }
                output[item_name_key] = file_data 
    elif selected_type == "Items(3d)":
        material = material_entry.get() or "PAPER"
        color_map = defaultdict(lambda: "0,0,0")
        
        for item in item_list.get(0, tk.END):
            item_name_key = os.path.splitext(os.path.basename(item))[0]
            item_name_display = item_name_key.replace("_", " ").title()
            
            if item.lower().endswith(".json"):
                file_data = {
                    "itemname": item_name_display,
                    "material": material,
                    "Pack": {
                        "generate_model": False,
                        "model": f"{item}"
                    }
                }
                output[item_name_key] = file_data
            elif item.lower().endswith(("_chestplate.png", "_helmet.png", "_leggings.png", "_boots.png")):
                prefix = item_name_key.split('_')[0]
                color = color_map[prefix]
                
                file_data = {
                    "itemname": item_name_display,
                    "material": "LEATHER_HELMET",
                    "Pack": {
                        "generate_model": True,
                        "parent_model": "item/generated",
                        "textures": [f"{item}"]
                    },
                    "color": color
                }
                output[item_name_key] = file_data     
    elif selected_type == "Icons":
        try:
            ascent_value = int(ascent_entry.get())
            height_value = int(height_entry.get())
            
            for item in item_list.get(0, tk.END):
                if item.lower().endswith((".png", ".jpg", ".jpeg")):
                    item_name_key = os.path.splitext(os.path.basename(item))[0]
                    
                    file_data = {
                        "texture": f"{item}",
                        "ascent": ascent_value,
                        "height": height_value
                    }
                    output[item_name_key] = file_data
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for Ascent and Height.")
            return 
    else:
        messagebox.showinfo("Information", "Please select a valid type to process files.")
        return

    yaml_output = yaml.dump(output, allow_unicode=True, sort_keys=False)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, yaml_output)

frame_top = tk.Frame(root, bg="#252526", padx=20, pady=20)
frame_top.pack(pady=20)

btn_select = tk.Button(frame_top, text="Select your ZIP", command=select_file, bg="#0078d4", fg="white", font=font_style, relief="flat", width=20, bd=0, highlightthickness=0)
btn_select.pack(pady=10)

option_label = tk.Label(frame_top, text="File Readed!", bg="#252526", font=font_style, fg="white")

style = ttk.Style()
style.configure("TCombobox", 
                relief="flat", 
                padding=5, 
                font=font_style,
                background="#252526", 
                foreground="#000000", 
                focuscolor="none")

option_menu = ttk.Combobox(frame_top, textvariable=option_var, values=["Icons", "Items(2d)", "Items(3d)", "Blocks"], state="readonly", font=font_style, style="TCombobox")
option_menu.set("Icons")
option_menu.bind("<<ComboboxSelected>>", option_selected)
option_menu.pack(pady=5)

option_label = tk.Label(frame_top, text="Please Select Type First Default is Not Working", bg="#252526", font=font_style, fg="red")
option_label.pack(pady=5)

item_list = tk.Listbox(frame_top, width=50, height=10, font=font_style, bg="#333333", bd=1, relief="solid", highlightthickness=0, fg="white")
item_list.pack(pady=10)

input_frame = tk.Frame(root, bg="#252526")
input_frame.pack(pady=5)

ascent_label = tk.Label(input_frame, text="Ascent:", bg="#252526", font=font_style, fg="white")
ascent_entry = tk.Entry(input_frame, font=font_style)

height_label = tk.Label(input_frame, text="Height:", bg="#252526", font=font_style, fg="white")
height_entry = tk.Entry(input_frame, font=font_style)

material_label = tk.Label(input_frame, text="Material:", bg="#252526", font=font_style, fg="white")
material_entry = tk.Entry(input_frame, font=font_style)

frame_bottom = tk.Frame(root, bg="#252526")
frame_bottom.pack(pady=5)

btn_process = tk.Button(frame_bottom, text="Generate Config", command=process_files, bg="#28a745", fg="white", font=font_style, relief="flat", width=20, bd=0, highlightthickness=0)
btn_process.pack(pady=10)

output_text = tk.Text(frame_bottom, width=60, height=10, font=font_style, wrap=tk.WORD, bg="#333333", bd=1, relief="solid", highlightthickness=0, fg="white")
output_text.pack(pady=10)

root.mainloop()
