import os
import random
import csv
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# --- 1. Configuration ---
DATASETS = ["MNIST", "FashionMNIST", "SVHN", "CIFAR10", "Imagenet"]
RESULT_FILE = "humaneval_results.csv"

class HumanEvalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Generative Model Semantic Evaluation Tool")
        self.root.geometry("1000x700")
        
        # Get absolute path of current script directory
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.tasks = self._prepare_tasks()
        
        if not self.tasks:
            print("Error: No valid images found in current directory!")
            print(f"Please check if these folders exist: {DATASETS}")
            
        self.current_idx = 0
        self._setup_ui()
        if self.tasks:
            self._load_task()

    def _prepare_tasks(self):
        """Scan folders for image sequences"""
        tasks = []
        for ds in DATASETS:
            ds_path = os.path.join(self.base_dir, ds)
            if not os.path.exists(ds_path):
                print(f"Skipping: Folder '{ds}' not found.")
                continue
            
            for class_dir in sorted(os.listdir(ds_path)):
                class_path = os.path.join(ds_path, class_dir)
                if not os.path.isdir(class_path): continue
                
                # Extract Class ID from folder name (e.g., 'class_0' -> '0')
                try:
                    class_id = class_dir.split('_')[1]
                except IndexError:
                    continue

                # Locate Reference Image (exp_0)
                ref_img = os.path.join(class_path, f"sample_{class_id}_exp_0.png")
                
                if not os.path.exists(ref_img):
                    print(f"Warning: Missing ref image exp_0 in {class_dir}")
                    continue

                # Locate Interpolated Images (exp_1 to exp_5)
                for i in range(1, 6):
                    target_img = os.path.join(class_path, f"sample_{class_id}_exp_{i}.png")
                    if os.path.exists(target_img):
                        tasks.append({
                            "dataset": ds,
                            "class": class_dir,
                            "exp_level": i,
                            "ref_path": ref_img,
                            "target_path": target_img
                        })
        
        random.shuffle(tasks) # Shuffle for unbiased evaluation
        return tasks

    def _setup_ui(self):
        # Progress Tracking
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=800, mode="determinate")
        self.progress.pack(pady=20)
        
        self.info_label = tk.Label(self.root, text="Ready", font=("Verdana", 12, "bold"))
        self.info_label.pack()

        # Image Display Area
        img_frame = tk.Frame(self.root)
        img_frame.pack(pady=20)

        # Labels for Images
        tk.Label(img_frame, text="[ Original Image ]", font=("Verdana", 10)).grid(row=0, column=0)
        tk.Label(img_frame, text="[ Latte ]", font=("Verdana", 10)).grid(row=0, column=1)

        self.ref_canvas = tk.Label(img_frame, relief="ridge", bd=3)
        self.ref_canvas.grid(row=1, column=0, padx=30, pady=10)
        
        self.target_canvas = tk.Label(img_frame, relief="ridge", bd=3)
        self.target_canvas.grid(row=1, column=1, padx=30, pady=10)

        # Scoring Area
        score_frame = tk.LabelFrame(self.root, text=" Semantic Preservation Score ", padx=20, pady=20)
        score_frame.pack(pady=20)
        
        guide_text = "1: Identity Lost | 2: Heavily Distorted | 3: Recognizable but Modded | 4: Minor Change | 5: Identity Preserved"
        desc = tk.Label(score_frame, text=guide_text, fg="#555555", font=("Verdana", 9, "italic"))
        desc.pack(side=tk.TOP, pady=5)

        btn_container = tk.Frame(score_frame)
        btn_container.pack(side=tk.TOP)

        for i in range(1, 6):
            btn = tk.Button(btn_container, text=f"Score {i}", font=("Verdana", 11), width=12,
                            bg="#f0f0f0", command=lambda s=i: self._submit_score(s))
            btn.pack(side=tk.LEFT, padx=10, pady=10)

    def _load_task(self):
        if self.current_idx >= len(self.tasks):
            self.info_label.config(text="Evaluation Complete! Data saved to CSV.", fg="#007700")
            return

        task = self.tasks[self.current_idx]
        self.info_label.config(text=f"Dataset: {task['dataset']} | Progress: {self.current_idx+1}/{len(self.tasks)}", fg="black")
        self.progress['value'] = (self.current_idx / len(self.tasks)) * 100

        # High-quality Resizing for Display
        display_size = (320, 320)
        ref_img = Image.open(task['ref_path']).convert("RGB").resize(display_size, Image.LANCZOS)
        tar_img = Image.open(task['target_path']).convert("RGB").resize(display_size, Image.LANCZOS)
        
        self.ref_photo = ImageTk.PhotoImage(ref_img)
        self.tar_photo = ImageTk.PhotoImage(tar_img)
        
        self.ref_canvas.config(image=self.ref_photo)
        self.target_canvas.config(image=self.tar_photo)

    def _submit_score(self, score):
        if self.current_idx >= len(self.tasks): return
        
        task = self.tasks[self.current_idx]
        
        # Write Result to CSV
        file_exists = os.path.isfile(RESULT_FILE)
        with open(RESULT_FILE, "a", newline="", encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["Dataset", "Class", "Exp_Level", "Score"])
            writer.writerow([task['dataset'], task['class'], task['exp_level'], score])
        
        # Advance to next image
        self.current_idx += 1
        self._load_task()

if __name__ == "__main__":
    root = tk.Tk()
    app = HumanEvalGUI(root)
    root.mainloop()
