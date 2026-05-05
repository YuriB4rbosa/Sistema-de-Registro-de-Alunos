import tkinter as tk
from tkinter import ttk
from .estilos import (BRANCO, CINZA_BG, CINZA_CARD, CINZA_BORDA,
                       CINZA_LABEL, PRETO_TEXTO, AZUL_MEDIO,
                       FONT_TITULO, FONT_LABEL, FONT_ENTRY, FONT_BTN)


def make_btn(parent, text, bg, fg, cmd, borda=None, pack=True, side="left",
             padx=(0, 6), pady=6):
    """Cria um botão padronizado do sistema."""
    b = tk.Button(parent, text=text, font=FONT_BTN,
                  bg=bg, fg=fg, activebackground=bg,
                  relief="solid", bd=1,
                  highlightthickness=1,
                  highlightbackground=borda or bg,
                  cursor="hand2", padx=14, pady=pady,
                  command=cmd)
    if pack:
        b.pack(side=side, padx=padx)
    return b


def make_card(parent, title, icon=""):
    
    outer = tk.Frame(parent, bg=BRANCO, bd=1, relief="solid",
                     highlightthickness=1, highlightbackground=CINZA_BORDA)
    outer.pack(fill="x", pady=(0, 12))

    hdr = tk.Frame(outer, bg=CINZA_CARD)
    hdr.pack(fill="x")
    tk.Frame(hdr, bg=AZUL_MEDIO, width=3).pack(side="left", fill="y")
    tk.Label(hdr, text=f"{icon}  {title}" if icon else title,
             font=FONT_TITULO, bg=CINZA_CARD, fg=PRETO_TEXTO,
             padx=12, pady=8).pack(side="left")

    body = tk.Frame(outer, bg=BRANCO)
    body.pack(fill="both", padx=14, pady=12)
    return body


def make_field(parent, label, row, col, colspan=1, width=22, required=True):
    
    tk.Label(parent, text=label + (" *" if required else ""),
             font=("Segoe UI", 8, "bold"), bg=BRANCO,
             fg=CINZA_LABEL).grid(
        row=row * 2, column=col, columnspan=colspan,
        sticky="w", padx=(0, 8), pady=(6, 2))

    e = tk.Entry(parent, font=FONT_ENTRY, width=width,
                 bd=1, relief="solid", bg=BRANCO, fg=PRETO_TEXTO,
                 insertbackground=AZUL_MEDIO,
                 highlightthickness=1, highlightbackground=CINZA_BORDA,
                 highlightcolor=AZUL_MEDIO)
    e.grid(row=row * 2 + 1, column=col, columnspan=colspan,
           sticky="ew", padx=(0, 8), pady=(0, 2))
    return e


def make_scrolled_tree(parent, columns, headings_cfg):
    
    tree = ttk.Treeview(parent, columns=columns,
                         show="headings", selectmode="browse")
    for col, (lbl, w) in headings_cfg.items():
        tree.heading(col, text=lbl, anchor="w")
        tree.column(col, width=w, minwidth=30, anchor="w")

    vsb = ttk.Scrollbar(parent, orient="vertical",   command=tree.yview)
    hsb = ttk.Scrollbar(parent, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)

    tree.tag_configure("par",   background=BRANCO)
    tree.tag_configure("impar", background="#FAFAF8")
    return tree


def make_toast(root, msg, bg, fg, duration=3000):
    
    t = tk.Toplevel(root)
    t.overrideredirect(True)
    t.attributes("-topmost", True)
    t.configure(bg=bg)
    x = root.winfo_x() + root.winfo_width()  - 345
    y = root.winfo_y() + root.winfo_height() - 72
    t.geometry(f"325x44+{x}+{y}")
    tk.Label(t, text=msg, font=FONT_LABEL,
             bg=bg, fg=fg, padx=14, pady=10).pack(fill="both")
    t.after(duration, t.destroy)