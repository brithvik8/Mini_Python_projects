import os
import threading
from tkinter import filedialog, messagebox
import customtkinter
from services.pdf_service import PDFService

# Initialize CustomTkinter styling parameters
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")  # Using blue as base theme fallback

# Custom Theme Colors
PRIMARY_PURPLE = "#463671"
HOVER_PURPLE = "#362957"
LIGHT_PURPLE = "#A78BFA"
ROW_SELECT_PURPLE = "#2D204E"

class MergeFrame(customtkinter.CTkFrame):
    """Frame wrapping PDF Merging user interface components."""
    def __init__(self, parent, service: PDFService, update_status_func):
        super().__init__(parent, fg_color="transparent")
        self.service = service
        self.update_status = update_status_func
        self.selected_files = []
        self.selected_index = -1
        
        self._init_layout()

    def _init_layout(self):
        # Header
        self.lbl_title = customtkinter.CTkLabel(
            self, text="Merge PDF Documents", font=("Helvetica", 20, "bold")
        )
        self.lbl_title.pack(anchor="w", pady=(10, 15))
        
        # Files List Box Frame
        self.list_frame = customtkinter.CTkFrame(self)
        self.list_frame.pack(fill="both", expand=True, pady=5)
        
        # Left side inside list frame: Scrollable list of files
        self.scrollable_frame = customtkinter.CTkScrollableFrame(
            self.list_frame, label_text="Selected PDF Files (Order of Merging)"
        )
        self.scrollable_frame.pack(side="left", fill="both", expand=True, padx=(5, 10), pady=5)
        
        # Right side inside list frame: Action buttons for reordering
        self.btn_control_frame = customtkinter.CTkFrame(self.list_frame, width=120, fg_color="transparent")
        self.btn_control_frame.pack(side="right", fill="y", padx=5, pady=5)
        
        self.btn_add = customtkinter.CTkButton(
            self.btn_control_frame, text="+ Add PDFs", fg_color=PRIMARY_PURPLE, hover_color=HOVER_PURPLE, command=self.add_files
        )
        self.btn_add.pack(fill="x", pady=5)
        
        self.btn_move_up = customtkinter.CTkButton(
            self.btn_control_frame, text="Move Up", fg_color=PRIMARY_PURPLE, hover_color=HOVER_PURPLE, command=self.move_up, state="disabled"
        )
        self.btn_move_up.pack(fill="x", pady=5)
        
        self.btn_move_down = customtkinter.CTkButton(
            self.btn_control_frame, text="Move Down", fg_color=PRIMARY_PURPLE, hover_color=HOVER_PURPLE, command=self.move_down, state="disabled"
        )
        self.btn_move_down.pack(fill="x", pady=5)
        
        self.btn_remove = customtkinter.CTkButton(
            self.btn_control_frame, text="Remove", command=self.remove_file, fg_color="#991B1B", hover_color="#7F1D1D", state="disabled"
        )
        self.btn_remove.pack(fill="x", pady=5)
        
        self.btn_clear = customtkinter.CTkButton(
            self.btn_control_frame, text="Clear All", command=self.clear_all, fg_color="#374151", hover_color="#4B5563"
        )
        self.btn_clear.pack(fill="x", pady=(20, 5))
        
        # Output selection section
        self.out_frame = customtkinter.CTkFrame(self)
        self.out_frame.pack(fill="x", pady=15)
        
        self.lbl_output = customtkinter.CTkLabel(self.out_frame, text="Output Path:", width=90, anchor="e")
        self.lbl_output.pack(side="left", padx=5, pady=10)
        
        self.txt_output = customtkinter.CTkEntry(
            self.out_frame, placeholder_text="Path to save merged PDF file"
        )
        self.txt_output.pack(side="left", fill="x", expand=True, padx=5, pady=10)
        
        self.btn_browse = customtkinter.CTkButton(
            self.out_frame, text="Browse", width=80, fg_color=PRIMARY_PURPLE, hover_color=HOVER_PURPLE, command=self.browse_output
        )
        self.btn_browse.pack(side="right", padx=5, pady=10)
        
        # Process Run Button
        self.btn_merge = customtkinter.CTkButton(
            self, text="Merge PDFs", height=40, font=("Helvetica", 14, "bold"), fg_color=PRIMARY_PURPLE, hover_color=HOVER_PURPLE, command=self.run_merge
        )
        self.btn_merge.pack(fill="x", pady=(5, 10))
        
        # Progress Indicator
        self.progress = customtkinter.CTkProgressBar(self, progress_color=PRIMARY_PURPLE)
        self.progress.pack(fill="x", pady=5)
        self.progress.set(0)
        self.progress.pack_forget() # Hide initially

    def add_files(self):
        paths = filedialog.askopenfilenames(
            title="Select PDF Files", filetypes=[("PDF Files", "*.pdf")]
        )
        if paths:
            for path in paths:
                normalized = os.path.abspath(path)
                if normalized not in self.selected_files:
                    self.selected_files.append(normalized)
            self.update_list_display()
            self.update_status(f"Added {len(paths)} PDF file(s).")

    def update_list_display(self):
        # Clear child widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        for i, filepath in enumerate(self.selected_files):
            bg = ROW_SELECT_PURPLE if i == self.selected_index else "transparent"
            row = customtkinter.CTkFrame(self.scrollable_frame, fg_color=bg, corner_radius=4)
            row.pack(fill="x", pady=2, padx=2)
            
            # Setup row selection click triggers
            def bind_click(w, idx=i):
                w.bind("<Button-1>", lambda e: self.select_row(idx))
                
            lbl_index = customtkinter.CTkLabel(
                row, text=f"{i+1}.", font=("Helvetica", 11, "bold"), width=30, anchor="w"
            )
            lbl_index.pack(side="left", padx=5, pady=5)
            bind_click(lbl_index)
            
            lbl_name = customtkinter.CTkLabel(
                row, text=os.path.basename(filepath), anchor="w"
            )
            lbl_name.pack(side="left", fill="x", expand=True, padx=5, pady=5)
            bind_click(lbl_name)
            
            bind_click(row)
            
        self._toggle_control_buttons()

    def select_row(self, index: int):
        self.selected_index = index
        self.update_list_display()

    def _toggle_control_buttons(self):
        if self.selected_index != -1 and len(self.selected_files) > 0:
            self.btn_remove.configure(state="normal")
            self.btn_move_up.configure(state="normal" if self.selected_index > 0 else "disabled")
            self.btn_move_down.configure(state="normal" if self.selected_index < len(self.selected_files) - 1 else "disabled")
        else:
            self.btn_remove.configure(state="disabled")
            self.btn_move_up.configure(state="disabled")
            self.btn_move_down.configure(state="disabled")

    def move_up(self):
        idx = self.selected_index
        if idx > 0:
            self.selected_files[idx], self.selected_files[idx-1] = self.selected_files[idx-1], self.selected_files[idx]
            self.selected_index = idx - 1
            self.update_list_display()

    def move_down(self):
        idx = self.selected_index
        if idx < len(self.selected_files) - 1:
            self.selected_files[idx], self.selected_files[idx+1] = self.selected_files[idx+1], self.selected_files[idx]
            self.selected_index = idx + 1
            self.update_list_display()

    def remove_file(self):
        if self.selected_index != -1:
            del self.selected_files[self.selected_index]
            self.selected_index = -1
            self.update_list_display()
            self.update_status("Removed file from merge queue.")

    def clear_all(self):
        self.selected_files.clear()
        self.selected_index = -1
        self.update_list_display()
        self.update_status("Cleared merge queue.")

    def browse_output(self):
        path = filedialog.asksaveasfilename(
            title="Save Merged PDF", defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")]
        )
        if path:
            self.txt_output.delete(0, customtkinter.END)
            self.txt_output.insert(0, os.path.abspath(path))

    def run_merge(self):
        if len(self.selected_files) < 2:
            messagebox.showerror("Input Error", "Please add at least 2 PDF files to merge.")
            return
            
        out_path = self.txt_output.get().strip()
        if not out_path:
            messagebox.showerror("Input Error", "Please specify a target file output path.")
            return

        self.btn_merge.configure(state="disabled")
        self.progress.pack(fill="x", pady=5)
        self.progress.set(0.1)
        self.update_status("Merging PDFs...")

        def thread_task():
            try:
                self.progress.set(0.4)
                self.service.merge_pdfs(self.selected_files, out_path)
                self.progress.set(1.0)
                self.update_status("Successfully merged PDF documents.")
                messagebox.showinfo("Success", f"PDFs successfully merged into:\n{out_path}")
            except Exception as ex:
                self.update_status("Merge failed.")
                messagebox.showerror("Error", f"Failed to merge files:\n{str(ex)}")
            finally:
                self.progress.pack_forget()
                self.btn_merge.configure(state="normal")

        threading.Thread(target=thread_task, daemon=True).start()


class SplitFrame(customtkinter.CTkFrame):
    """Frame wrapping PDF Extraction and splitting GUI elements."""
    def __init__(self, parent, service: PDFService, update_status_func):
        super().__init__(parent, fg_color="transparent")
        self.service = service
        self.update_status = update_status_func
        
        self._init_layout()

    def _init_layout(self):
        # Header
        self.lbl_title = customtkinter.CTkLabel(
            self, text="Split or Extract PDF Pages", font=("Helvetica", 20, "bold")
        )
        self.lbl_title.pack(anchor="w", pady=(10, 15))
        
        # File selector card
        self.file_frame = customtkinter.CTkFrame(self)
        self.file_frame.pack(fill="x", pady=10)
        
        self.lbl_file = customtkinter.CTkLabel(self.file_frame, text="Select PDF:", width=90, anchor="e")
        self.lbl_file.pack(side="left", padx=5, pady=10)
        
        self.txt_file = customtkinter.CTkEntry(self.file_frame, placeholder_text="Path to the PDF file to split")
        self.txt_file.pack(side="left", fill="x", expand=True, padx=5, pady=10)
        
        self.btn_file_browse = customtkinter.CTkButton(
            self.file_frame, text="Browse", width=80, fg_color=PRIMARY_PURPLE, hover_color=HOVER_PURPLE, command=self.browse_input
        )
        self.btn_file_browse.pack(side="right", padx=5, pady=10)
        
        # Split options configuration
        self.options_frame = customtkinter.CTkTabview(self)
        self.options_frame.pack(fill="both", expand=True, pady=10)
        
        self.tab_range = self.options_frame.add("Extract Ranges")
        self.tab_all = self.options_frame.add("Split All Pages")
        
        # Configure tab selector color
        self.options_frame._segmented_button.configure(selected_color=PRIMARY_PURPLE, selected_hover_color=HOVER_PURPLE)
        
        # Setup Tab 1: Extract Range Layout
        self.lbl_ranges = customtkinter.CTkLabel(
            self.tab_range, text="Page Ranges (e.g. 1-3, 5, 8-10):", anchor="w"
        )
        self.lbl_ranges.pack(fill="x", padx=10, pady=(10, 5))
        
        self.txt_ranges = customtkinter.CTkEntry(
            self.tab_range, placeholder_text="Enter page selections (1-indexed)"
        )
        self.txt_ranges.pack(fill="x", padx=10, pady=5)
        
        # Output File path selection
        self.out_range_frame = customtkinter.CTkFrame(self.tab_range, fg_color="transparent")
        self.out_range_frame.pack(fill="x", padx=5, pady=10)
        
        self.lbl_out_range = customtkinter.CTkLabel(self.out_range_frame, text="Save As:", width=80, anchor="e")
        self.lbl_out_range.pack(side="left", padx=5)
        
        self.txt_out_range = customtkinter.CTkEntry(self.out_range_frame, placeholder_text="Path for saving extracted PDF")
        self.txt_out_range.pack(side="left", fill="x", expand=True, padx=5)
        
        self.btn_out_range_browse = customtkinter.CTkButton(
            self.out_range_frame, text="Browse", width=80, fg_color=PRIMARY_PURPLE, hover_color=HOVER_PURPLE, command=self.browse_range_output
        )
        self.btn_out_range_browse.pack(side="right", padx=5)
        
        self.btn_run_range = customtkinter.CTkButton(
            self.tab_range, text="Extract Selected Pages", height=35, fg_color=PRIMARY_PURPLE, hover_color=HOVER_PURPLE, command=self.run_range_extract
        )
        self.btn_run_range.pack(fill="x", padx=10, pady=(20, 10))
        
        # Setup Tab 2: Split All Pages Layout
        self.lbl_dir_info = customtkinter.CTkLabel(
            self.tab_all, text="Splits every page of the PDF into separate single-page PDF files.", anchor="w"
        )
        self.lbl_dir_info.pack(fill="x", padx=10, pady=(15, 5))
        
        self.dir_frame = customtkinter.CTkFrame(self.tab_all, fg_color="transparent")
        self.dir_frame.pack(fill="x", padx=5, pady=10)
        
        self.lbl_dir = customtkinter.CTkLabel(self.dir_frame, text="Output Folder:", width=90, anchor="e")
        self.lbl_dir.pack(side="left", padx=5)
        
        self.txt_dir = customtkinter.CTkEntry(self.dir_frame, placeholder_text="Directory path to save split page files")
        self.txt_dir.pack(side="left", fill="x", expand=True, padx=5)
        
        self.btn_dir_browse = customtkinter.CTkButton(
            self.dir_frame, text="Browse", width=80, fg_color=PRIMARY_PURPLE, hover_color=HOVER_PURPLE, command=self.browse_dir_output
        )
        self.btn_dir_browse.pack(side="right", padx=5)
        
        self.btn_run_all = customtkinter.CTkButton(
            self.tab_all, text="Split All Pages", fg_color=PRIMARY_PURPLE, hover_color=HOVER_PURPLE, height=35, command=self.run_split_all
        )
        self.btn_run_all.pack(fill="x", padx=10, pady=(25, 10))
        
        # Progress Indicator
        self.progress = customtkinter.CTkProgressBar(self, progress_color=PRIMARY_PURPLE)
        self.progress.pack(fill="x", pady=5)
        self.progress.set(0)
        self.progress.pack_forget()

    def browse_input(self):
        path = filedialog.askopenfilename(
            title="Select PDF to Split", filetypes=[("PDF Files", "*.pdf")]
        )
        if path:
            self.txt_file.delete(0, customtkinter.END)
            self.txt_file.insert(0, os.path.abspath(path))

    def browse_range_output(self):
        path = filedialog.asksaveasfilename(
            title="Save Extracted Pages As", defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")]
        )
        if path:
            self.txt_out_range.delete(0, customtkinter.END)
            self.txt_out_range.insert(0, os.path.abspath(path))

    def browse_dir_output(self):
        path = filedialog.askdirectory(title="Select Output Folder")
        if path:
            self.txt_dir.delete(0, customtkinter.END)
            self.txt_dir.insert(0, os.path.abspath(path))

    def run_range_extract(self):
        in_path = self.txt_file.get().strip()
        ranges = self.txt_ranges.get().strip()
        out_path = self.txt_out_range.get().strip()
        
        if not in_path or not os.path.exists(in_path):
            messagebox.showerror("Input Error", "Please select a valid input PDF file.")
            return
        if not ranges:
            messagebox.showerror("Input Error", "Please specify page ranges (e.g. 1-3, 5).")
            return
        if not out_path:
            messagebox.showerror("Input Error", "Please choose a file output path.")
            return

        self.btn_run_range.configure(state="disabled")
        self.progress.pack(fill="x", pady=5)
        self.progress.set(0.2)
        self.update_status("Extracting PDF pages...")

        def thread_task():
            try:
                self.progress.set(0.5)
                self.service.split_pdf(in_path, ranges, out_path)
                self.progress.set(1.0)
                self.update_status("Pages successfully extracted.")
                messagebox.showinfo("Success", f"Pages successfully extracted into:\n{out_path}")
            except Exception as ex:
                self.update_status("Extraction failed.")
                messagebox.showerror("Error", f"Failed to extract pages:\n{str(ex)}")
            finally:
                self.progress.pack_forget()
                self.btn_run_range.configure(state="normal")

        threading.Thread(target=thread_task, daemon=True).start()

    def run_split_all(self):
        in_path = self.txt_file.get().strip()
        out_dir = self.txt_dir.get().strip()
        
        if not in_path or not os.path.exists(in_path):
            messagebox.showerror("Input Error", "Please select a valid input PDF file.")
            return
        if not out_dir:
            messagebox.showerror("Input Error", "Please specify a destination directory folder.")
            return

        self.btn_run_all.configure(state="disabled")
        self.progress.pack(fill="x", pady=5)
        self.progress.set(0.2)
        self.update_status("Splitting all pages...")

        def thread_task():
            try:
                self.progress.set(0.5)
                paths = self.service.split_all_pages(in_path, out_dir)
                self.progress.set(1.0)
                self.update_status(f"Successfully split PDF into {len(paths)} files.")
                messagebox.showinfo("Success", f"Successfully split PDF into {len(paths)} files in folder:\n{out_dir}")
            except Exception as ex:
                self.update_status("Splitting failed.")
                messagebox.showerror("Error", f"Failed to split pages:\n{str(ex)}")
            finally:
                self.progress.pack_forget()
                self.btn_run_all.configure(state="normal")

        threading.Thread(target=thread_task, daemon=True).start()


class RotateFrame(customtkinter.CTkFrame):
    """Frame wrapping PDF Rotation user interface layouts."""
    def __init__(self, parent, service: PDFService, update_status_func):
        super().__init__(parent, fg_color="transparent")
        self.service = service
        self.update_status = update_status_func
        
        self._init_layout()

    def _init_layout(self):
        # Header
        self.lbl_title = customtkinter.CTkLabel(
            self, text="Rotate PDF Document Pages", font=("Helvetica", 20, "bold")
        )
        self.lbl_title.pack(anchor="w", pady=(10, 15))
        
        # Input selection card
        self.file_frame = customtkinter.CTkFrame(self)
        self.file_frame.pack(fill="x", pady=10)
        
        self.lbl_file = customtkinter.CTkLabel(self.file_frame, text="Select PDF:", width=90, anchor="e")
        self.lbl_file.pack(side="left", padx=5, pady=10)
        
        self.txt_file = customtkinter.CTkEntry(self.file_frame, placeholder_text="Path to the PDF file to rotate")
        self.txt_file.pack(side="left", fill="x", expand=True, padx=5, pady=10)
        
        self.btn_file_browse = customtkinter.CTkButton(
            self.file_frame, text="Browse", width=80, fg_color=PRIMARY_PURPLE, hover_color=HOVER_PURPLE, command=self.browse_input
        )
        self.btn_file_browse.pack(side="right", padx=5, pady=10)
        
        # Control parameters card
        self.control_frame = customtkinter.CTkFrame(self)
        self.control_frame.pack(fill="x", pady=10)
        
        self.lbl_angle = customtkinter.CTkLabel(self.control_frame, text="Rotation Angle:", width=95, anchor="e")
        self.lbl_angle.pack(side="left", padx=5, pady=10)
        
        self.cb_angle = customtkinter.CTkComboBox(self.control_frame, values=["90°", "180°", "270°"], state="readonly")
        self.cb_angle.pack(side="left", padx=5, pady=10)
        self.cb_angle.set("90°")
        
        # Save output selection
        self.out_frame = customtkinter.CTkFrame(self)
        self.out_frame.pack(fill="x", pady=10)
        
        self.lbl_out = customtkinter.CTkLabel(self.out_frame, text="Save As:", width=90, anchor="e")
        self.lbl_out.pack(side="left", padx=5, pady=10)
        
        self.txt_out = customtkinter.CTkEntry(self.out_frame, placeholder_text="Output rotated PDF path")
        self.txt_out.pack(side="left", fill="x", expand=True, padx=5, pady=10)
        
        self.btn_out_browse = customtkinter.CTkButton(
            self.out_frame, text="Browse", width=80, fg_color=PRIMARY_PURPLE, hover_color=HOVER_PURPLE, command=self.browse_output
        )
        self.btn_out_browse.pack(side="right", padx=5, pady=10)
        
        # Execute button
        self.btn_rotate = customtkinter.CTkButton(
            self, text="Rotate PDF Pages", height=40, font=("Helvetica", 14, "bold"), fg_color=PRIMARY_PURPLE, hover_color=HOVER_PURPLE, command=self.run_rotate
        )
        self.btn_rotate.pack(fill="x", pady=(20, 10))
        
        # Progress Indicator
        self.progress = customtkinter.CTkProgressBar(self, progress_color=PRIMARY_PURPLE)
        self.progress.pack(fill="x", pady=5)
        self.progress.set(0)
        self.progress.pack_forget()

    def browse_input(self):
        path = filedialog.askopenfilename(
            title="Select PDF File to Rotate", filetypes=[("PDF Files", "*.pdf")]
        )
        if path:
            self.txt_file.delete(0, customtkinter.END)
            self.txt_file.insert(0, os.path.abspath(path))

    def browse_output(self):
        path = filedialog.asksaveasfilename(
            title="Save Rotated PDF As", defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")]
        )
        if path:
            self.txt_out.delete(0, customtkinter.END)
            self.txt_out.insert(0, os.path.abspath(path))

    def run_rotate(self):
        in_path = self.txt_file.get().strip()
        angle_str = self.cb_angle.get().replace("°", "")
        out_path = self.txt_out.get().strip()
        
        if not in_path or not os.path.exists(in_path):
            messagebox.showerror("Input Error", "Please select a valid input PDF file.")
            return
        if not out_path:
            messagebox.showerror("Input Error", "Please specify an output target path.")
            return
            
        try:
            angle = int(angle_str)
        except ValueError:
            messagebox.showerror("Input Error", "Invalid rotation angle selected.")
            return

        self.btn_rotate.configure(state="disabled")
        self.progress.pack(fill="x", pady=5)
        self.progress.set(0.2)
        self.update_status(f"Rotating pages by {angle}°...")

        def thread_task():
            try:
                self.progress.set(0.5)
                self.service.rotate_pdf(in_path, out_path, angle)
                self.progress.set(1.0)
                self.update_status("Rotation complete.")
                messagebox.showinfo("Success", f"PDF pages successfully rotated and saved to:\n{out_path}")
            except Exception as ex:
                self.update_status("Rotation failed.")
                messagebox.showerror("Error", f"Failed to rotate PDF:\n{str(ex)}")
            finally:
                self.progress.pack_forget()
                self.btn_rotate.configure(state="normal")

        threading.Thread(target=thread_task, daemon=True).start()


class PDFMergerApp(customtkinter.CTk):
    """Main window desktop layout housing sidebar navigation and status outputs."""
    def __init__(self):
        super().__init__()
        
        # Configure Main Window
        self.title("Professional PDF Merger & Splitter")
        self.geometry("900x600")
        self.minsize(800, 500)
        
        # Initialize Backend Engine
        self.service = PDFService()
        self.current_frame = None

        self._build_interface()
        self.show_frame("merge") # Mount default view

    def _build_interface(self):
        # Configure Grid Layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Sidebar Frame Setup
        self.sidebar = customtkinter.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(4, weight=1) # Push theme selection to bottom
        
        # Sidebar Title logo (Styled with light purple)
        self.lbl_logo = customtkinter.CTkLabel(
            self.sidebar, text="PDF Utility Suite", font=("Helvetica", 18, "bold"), text_color=LIGHT_PURPLE
        )
        self.lbl_logo.grid(row=0, column=0, padx=20, pady=(20, 25))
        
        # Navigation Buttons
        self.btn_merge_tab = customtkinter.CTkButton(
            self.sidebar, text="Merge PDFs", font=("Helvetica", 13), border_spacing=10,
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            anchor="w", command=lambda: self.show_frame("merge")
        )
        self.btn_merge_tab.grid(row=1, column=0, sticky="ew", padx=10, pady=2)
        
        self.btn_split_tab = customtkinter.CTkButton(
            self.sidebar, text="Split PDF", font=("Helvetica", 13), border_spacing=10,
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            anchor="w", command=lambda: self.show_frame("split")
        )
        self.btn_split_tab.grid(row=2, column=0, sticky="ew", padx=10, pady=2)
        
        self.btn_rotate_tab = customtkinter.CTkButton(
            self.sidebar, text="Rotate Pages", font=("Helvetica", 13), border_spacing=10,
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            anchor="w", command=lambda: self.show_frame("rotate")
        )
        self.btn_rotate_tab.grid(row=3, column=0, sticky="ew", padx=10, pady=2)
        
        # Theme Selector at bottom
        self.theme_frame = customtkinter.CTkFrame(self.sidebar, fg_color="transparent")
        self.theme_frame.grid(row=5, column=0, padx=10, pady=15, sticky="ew")
        
        self.lbl_theme = customtkinter.CTkLabel(self.theme_frame, text="Appearance Mode:", font=("Helvetica", 11))
        self.lbl_theme.pack(anchor="w", padx=10, pady=2)
        
        self.opt_theme = customtkinter.CTkOptionMenu(
            self.theme_frame, values=["Dark", "Light", "System"],
            fg_color=PRIMARY_PURPLE, button_color=PRIMARY_PURPLE, button_hover_color=HOVER_PURPLE,
            command=self.change_theme_mode
        )
        self.opt_theme.pack(fill="x", padx=10, pady=2)
        
        # Main Work Content Area (Right Hand Panel)
        self.content_container = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.content_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)
        
        # Status Bar Footer
        self.status_bar = customtkinter.CTkFrame(self, height=25, corner_radius=0)
        self.status_bar.grid(row=1, column=0, columnspan=2, sticky="ew")
        
        self.lbl_status = customtkinter.CTkLabel(
            self.status_bar, text="Ready", font=("Helvetica", 11), text_color="#9CA3AF"
        )
        self.lbl_status.pack(side="left", padx=15, pady=2)

    def show_frame(self, frame_name: str):
        # Reset navigation buttons design focus
        self.btn_merge_tab.configure(fg_color="transparent")
        self.btn_split_tab.configure(fg_color="transparent")
        self.btn_rotate_tab.configure(fg_color="transparent")
        
        # Destroy current content view frame
        if self.current_frame:
            self.current_frame.destroy()
            
        if frame_name == "merge":
            self.btn_merge_tab.configure(fg_color=PRIMARY_PURPLE)
            self.current_frame = MergeFrame(self.content_container, self.service, self.update_status_bar)
        elif frame_name == "split":
            self.btn_split_tab.configure(fg_color=PRIMARY_PURPLE)
            self.current_frame = SplitFrame(self.content_container, self.service, self.update_status_bar)
        elif frame_name == "rotate":
            self.btn_rotate_tab.configure(fg_color=PRIMARY_PURPLE)
            self.current_frame = RotateFrame(self.content_container, self.service, self.update_status_bar)
            
        if self.current_frame:
            self.current_frame.grid(row=0, column=0, sticky="nsew")
            self.update_status_bar(f"Switched view to {frame_name.upper()} panel.")

    def change_theme_mode(self, mode: str):
        customtkinter.set_appearance_mode(mode)
        self.update_status_bar(f"Updated GUI Theme to: {mode}")

    def update_status_bar(self, text: str):
        self.lbl_status.configure(text=text)
