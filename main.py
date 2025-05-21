from data.Tables import Table9_2A
from parsers import xtb_pdf_parser
from xml_utils import irs_xml_writer
import tkinter as tk
from tkinter import filedialog
from pathlib import Path


def parse_xtb_report(accumulator: Table9_2A, xtb_file_path: str):
    xtb_entries = xtb_pdf_parser.extract_table_9_2a_entries(xtb_file_path)
    list(map(accumulator.add_entry, xtb_entries))


def write_entries_to_file(accumulator: Table9_2A, input_file_path: str, output_file_path: str):
    irs_xml_writer.add_table_9_2A_to_file(
        input_file_path,
        output_file_path,
        accumulator
    )


# UI functions

def read_xtb_pdf_file_path():
    file_path = filedialog.askopenfilename(title="Select XTB PDF report")
    if file_path:
        print("XTB PDF report path:", file_path)
        xtb_file_path_var.set(file_path)
        check_all_selected()


def read_irs_xml_file_path():
    file_path = filedialog.askopenfilename(title="IRS original file")
    if file_path:
        print("IRS original file path:", file_path)
        irs_original_file_path_var.set(file_path)
        check_all_selected()


def submit():
    accumulator = Table9_2A()

    xtb_file_path = xtb_file_path_var.get()
    irs_original_file_path = irs_original_file_path_var.get()
    out_path = Path(irs_original_file_path)
    output_file_path = str(out_path.with_name(out_path.stem + '_modified' + out_path.suffix))

    parse_xtb_report(accumulator, xtb_file_path)
    write_entries_to_file(accumulator, irs_original_file_path, output_file_path)

    # show 'done' text
    done_label = tk.Label(root, text="Done, written to:" + output_file_path)
    done_label.pack(pady=15)


def check_all_selected():
    if xtb_file_path_var.get() and irs_original_file_path_var.get():
        if not submit_button.winfo_ismapped():
            submit_button.pack(pady=10)


# GUI setup
root = tk.Tk()
root.title("IRS helper")
root.geometry("1200x400")

# Variables to hold selected file paths
xtb_file_path_var = tk.StringVar()
irs_original_file_path_var = tk.StringVar()

# Input File 1
frame_input1 = tk.Frame(root)
frame_input1.pack(pady=5, fill='x')
btn_input1 = tk.Button(frame_input1, text="XTB pdf report path", command=read_xtb_pdf_file_path)
btn_input1.pack(side='left', padx=5)
label_input1 = tk.Label(frame_input1, textvariable=xtb_file_path_var, anchor='w')
label_input1.pack(side='left', fill='x', expand=True)

# Input File 2
frame_input2 = tk.Frame(root)
frame_input2.pack(pady=5, fill='x')
btn_input2 = tk.Button(frame_input2, text="IRS report XML file path", command=read_irs_xml_file_path)
btn_input2.pack(side='left', padx=5)
label_input2 = tk.Label(frame_input2, textvariable=irs_original_file_path_var, anchor='w')
label_input2.pack(side='left', fill='x', expand=True)

# Submit button (initially hidden)
submit_button = tk.Button(root, text="Submit", command=submit)
# Don't pack it yet — will be packed when all files are selected

# Run the app
root.mainloop()
