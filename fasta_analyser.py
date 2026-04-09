import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np


def analyze_fasta():
    file_path = filedialog.askopenfilename()

    if not file_path:
        return

    sequences = {}
    name = ""
    seq = ""

    with open(file_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if name:
                    sequences[name] = seq
                name = line
                seq = ""
            else:
                seq += line
        if name:
            sequences[name] = seq

    output_box.delete("1.0", tk.END)

    lengths = []
    gc_values = []
    at_values = []
    names = []
    short_names = []

    output_box.insert(tk.END, f"Total sequences: {len(sequences)}\n\n")

    for i, (name, seq) in enumerate(sequences.items()):
        length = len(seq)
        gc = (seq.count("G") + seq.count("C")) / length * 100
        at = (seq.count("A") + seq.count("T")) / length * 100

        lengths.append(length)
        gc_values.append(gc)
        at_values.append(at)
        names.append(name)
        short_names.append(f"Seq {i+1}")  # Short labels for x-axis

        output_box.insert(tk.END, f"{name}\n")
        output_box.insert(tk.END, f"Length: {length}\n")
        output_box.insert(tk.END, f"GC%: {round(gc, 2)}\n")
        output_box.insert(tk.END, f"AT%: {round(at, 2)}\n\n")

    plot_graphs(short_names, names, lengths, gc_values, at_values)


def plot_graphs(short_names, full_names, lengths, gc_values, at_values):
    fig, axs = plt.subplots(2, 1, figsize=(10, 9))
    fig.subplots_adjust(hspace=0.6)  # Extra vertical space between subplots

    x = np.arange(len(short_names))

    # Graph 1: Sequence Lengths
    bars = axs[0].bar(x, lengths, color="steelblue", width=0.5)
    axs[0].set_title("Sequence Lengths", fontsize=13, pad=10)
    axs[0].set_ylabel("Length")
    axs[0].set_xticks(x)
    axs[0].set_xticklabels(short_names)
    axs[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{int(v):,}"))

    # Tooltip-style: show full name on hover via annotation
    for bar, full in zip(bars, full_names):
        axs[0].annotate(
            full[:40] + "..." if len(full) > 40 else full,
            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 4),
            textcoords="offset points",
            ha="center", va="bottom",
            fontsize=6, color="dimgray",
            wrap=True
        )

    # Graph 2: GC% vs AT%
    width = 0.35
    axs[1].bar(x - width / 2, gc_values, width=width, label="GC%", color="steelblue")
    axs[1].bar(x + width / 2, at_values, width=width, label="AT%", color="darkorange")
    axs[1].set_title("GC% vs AT%", fontsize=13, pad=10)
    axs[1].set_ylabel("Percentage")
    axs[1].set_xticks(x)
    axs[1].set_xticklabels(short_names)
    axs[1].set_ylim(0, 100)
    axs[1].legend()

    # Add a shared legend/note at the bottom mapping Seq N → full name
    legend_lines = [f"Seq {i+1}: {name[:80]}" for i, name in enumerate(full_names)]
    fig.text(
        0.5, 0.01,
        "\n".join(legend_lines),
        ha="center", va="bottom",
        fontsize=6.5, color="gray",
        family="monospace"
    )

    plt.tight_layout(rect=[0, 0.08, 1, 1])  # Leave room for bottom legend
    plt.show()


# UI Setup
root = tk.Tk()
root.title("FASTA Analyzer with Graphs")

label = tk.Label(root, text="FASTA Analyzer", font=("Arial", 16))
label.pack(pady=5)

btn = tk.Button(root, text="Upload FASTA File", command=analyze_fasta)
btn.pack(pady=10)

output_box = tk.Text(root, height=20, width=60)
output_box.pack()

root.mainloop()