# ============================================================
#  gui.py  —  Smart Emergency Response Routing System
#  Fully resizable, clean dark UI, Compare All dialog
# ============================================================

import tkinter as tk
from tkinter import ttk
import time, sys, os, copy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from grid import Grid, Node, EMPTY, START, END, OBSTACLE, TRAFFIC
from utils import format_stats
from algorithms.bfs    import bfs
from algorithms.dfs    import dfs
from algorithms.greedy import greedy
from algorithms.astar  import astar

# ══════════════════════════════════════════════════════════════
#  COLOUR TOKENS  — all 5 cell states are clearly distinct
# ══════════════════════════════════════════════════════════════
C = {
    # backgrounds
    "bg":        "#0D1117",
    "panel":     "#161B22",
    "card":      "#1C2128",
    "border":    "#30363D",

    # ── cell colours (5 clearly distinct states) ────────────
    "empty":     "#1A2030",   # very dark blue-grey
    "start":     "#23D160",   # vivid green
    "end":       "#FF3860",   # vivid red
    "obstacle":  "#353D4A",   # medium grey-blue (visible but muted)
    "traffic":   "#FF9F43",   # warm amber
    "explored":  "#1F6FEB",   # strong royal blue  ← was steel-blue, now darker/stronger
    "path":      "#00D4FF",   # bright cyan  ← was gold/yellow, now unmistakably different
    "grid_line": "#151C27",

    # text
    "t1": "#E6EDF3",
    "t2": "#8B949E",
    "t3": "#58A6FF",

    # accents
    "green":  "#23D160",
    "red":    "#FF3860",
    "amber":  "#FF9F43",
    "blue":   "#1F6FEB",
    "cyan":   "#00D4FF",
    "purple": "#BD93F9",
}

ALGO_MAP = {
    "A*  —  Optimal + Heuristic":          ("A*",     astar),
    "Greedy  —  Heuristic Only":           ("Greedy", greedy),
    "BFS  —  Breadth-First (Unweighted)":  ("BFS",    bfs),
    "DFS  —  Depth-First (Non-optimal)":   ("DFS",    dfs),
}
ALGO_KEYS = list(ALGO_MAP.keys())

MODES = [
    ("Start  🚑",    "start"),
    ("End  🏥",      "end"),
    ("Obstacle  ■",  "obstacle"),
    ("Traffic  ▲",   "traffic"),
    ("Erase",        "erase"),
]

GRID_ROWS   = 22
GRID_COLS   = 30
MIN_CELL    = 16
ANIM_MS     = 12


# ══════════════════════════════════════════════════════════════
#  HELPER  — snapshot grid state for Compare (no deep-copy of
#  cell objects; just remember type/cost per position)
# ══════════════════════════════════════════════════════════════
def snapshot_grid(g: Grid) -> list[list[tuple]]:
    """Return a 2-D list of (cell_type, cost) for every node."""
    return [
        [(g.get_node(r, c).cell_type, g.get_node(r, c).cost)
         for c in range(g.cols)]
        for r in range(g.rows)
    ]

def apply_snapshot(g: Grid, snap: list[list[tuple]]):
    """Restore cell_type / cost from snapshot without resetting search state."""
    g.start_node = None
    g.end_node   = None
    for r in range(g.rows):
        for c in range(g.cols):
            ct, cost = snap[r][c]
            node = g.get_node(r, c)
            node.cell_type = ct
            node.cost      = cost
            if ct == START:
                g.start_node = node
            elif ct == END:
                g.end_node = node


# ══════════════════════════════════════════════════════════════
#  COMPARE DIALOG
# ══════════════════════════════════════════════════════════════
class CompareDialog(tk.Toplevel):
    """
    Runs all 4 algorithms silently on a fresh copy of the grid
    and displays their statistics side-by-side in a clean table.
    """
    def __init__(self, parent, grid_model: Grid):
        super().__init__(parent)
        self.title("Algorithm Comparison")
        self.configure(bg=C["bg"])
        self.resizable(True, True)
        self.grab_set()   # modal

        tk.Label(
            self,
            text="Algorithm Comparison  —  Same Start / End / Obstacles",
            font=("Segoe UI", 12, "bold"),
            bg=C["bg"], fg=C["t1"],
        ).pack(pady=(18, 4), padx=24, anchor="w")

        tk.Label(
            self,
            text="All 4 algorithms run on identical grid. BFS/DFS ignore traffic cost.",
            font=("Segoe UI", 9),
            bg=C["bg"], fg=C["t2"],
        ).pack(padx=24, anchor="w")

        tk.Frame(self, bg=C["border"], height=1).pack(fill="x", padx=24, pady=12)

        # ── run all 4 and collect stats ──────────────────────
        snap     = snapshot_grid(grid_model)
        rows_n   = grid_model.rows
        cols_n   = grid_model.cols

        results = []
        for label, (name, fn) in ALGO_MAP.items():
            tmp = Grid(rows_n, cols_n)
            apply_snapshot(tmp, snap)
            t0 = time.perf_counter()
            try:
                path, visited = fn(tmp)
            except Exception as e:
                path, visited = [], []
            elapsed = time.perf_counter() - t0
            stats = format_stats(name, path, visited, elapsed)
            results.append(stats)

        # ── table ────────────────────────────────────────────
        headers = ["Algorithm", "Path Found", "Path Cells",
                   "Path Cost", "Nodes Explored", "Time"]
        col_keys = ["algorithm", "path_found", "path_length",
                    "path_cost", "nodes_explored", "time"]

        tbl_frame = tk.Frame(self, bg=C["panel"], padx=20, pady=16)
        tbl_frame.pack(fill="both", expand=True, padx=24, pady=(0, 8))

        # header row
        for ci, hdr in enumerate(headers):
            tk.Label(
                tbl_frame, text=hdr,
                font=("Segoe UI", 9, "bold"),
                bg=C["panel"], fg=C["t2"],
                padx=14, pady=6, anchor="w",
            ).grid(row=0, column=ci, sticky="ew", padx=2)

        tk.Frame(tbl_frame, bg=C["border"], height=1).grid(
            row=1, column=0, columnspan=len(headers), sticky="ew", pady=(0, 4))

        # accent colours per algorithm
        algo_colors = {
            "A*":     C["cyan"],
            "Greedy": C["purple"],
            "BFS":    C["green"],
            "DFS":    C["amber"],
        }

        # data rows
        for ri, stats in enumerate(results):
            row_bg = C["card"] if ri % 2 == 0 else C["panel"]
            name   = stats["algorithm"]
            color  = algo_colors.get(name, C["t1"])

            for ci, key in enumerate(col_keys):
                raw = stats[key]
                if key == "path_found":
                    text  = "✓  Yes" if raw else "✗  No"
                    fg    = C["green"] if raw else C["red"]
                elif key == "algorithm":
                    text = raw
                    fg   = color
                elif key == "path_cost":
                    text = str(raw)
                    fg   = C["amber"]
                elif key == "nodes_explored":
                    text = str(raw)
                    fg   = C["blue"]
                elif key == "time":
                    text = str(raw)
                    fg   = C["cyan"]
                else:
                    text = str(raw)
                    fg   = C["t1"]

                tk.Label(
                    tbl_frame, text=text,
                    font=("Segoe UI", 10, "bold" if ci == 0 else "normal"),
                    bg=row_bg, fg=fg,
                    padx=14, pady=10, anchor="w",
                ).grid(row=ri + 2, column=ci, sticky="ew", padx=2, pady=1)

        for ci in range(len(headers)):
            tbl_frame.columnconfigure(ci, weight=1)

        # ── summary note ─────────────────────────────────────
        tk.Frame(self, bg=C["border"], height=1).pack(fill="x", padx=24)
        note = (
            "A* guarantees the lowest-cost path (g+h).  "
            "Greedy is fast but may miss optimal (h only).  "
            "BFS guarantees fewest hops (no weights).  "
            "DFS is non-optimal — for comparison only."
        )
        tk.Label(
            self, text=note,
            font=("Segoe UI", 8, "italic"),
            bg=C["bg"], fg=C["t2"],
            wraplength=700, justify="left",
        ).pack(padx=24, pady=10, anchor="w")

        tk.Button(
            self, text="Close",
            bg=C["card"], fg=C["t1"],
            font=("Segoe UI", 10),
            relief="flat", padx=20, pady=6,
            cursor="hand2",
            command=self.destroy,
        ).pack(pady=(0, 16))

        self.update_idletasks()
        w, h = self.winfo_reqwidth(), self.winfo_reqheight()
        pw   = parent.winfo_x() + parent.winfo_width()  // 2
        ph   = parent.winfo_y() + parent.winfo_height() // 2
        self.geometry(f"{max(w,780)}x{max(h,340)}+{pw - max(w,780)//2}+{ph - max(h,340)//2}")


# ══════════════════════════════════════════════════════════════
#  MAIN APPLICATION
# ══════════════════════════════════════════════════════════════
class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Smart Emergency Response Routing System")
        self.configure(bg=C["bg"])
        self.minsize(860, 560)

        # Make window fully resizable and grid canvas stretches
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.grid_model   = Grid(GRID_ROWS, GRID_COLS)
        self.draw_mode    = tk.StringVar(value="start")
        self.algo_var     = tk.StringVar(value=ALGO_KEYS[0])
        self.speed_var    = tk.IntVar(value=ANIM_MS)
        self.is_animating = False
        self._anim_job    = None
        self._drag_mode   = None

        # cell_size is recomputed on every resize
        self._cell_size   = 24
        # canvas rectangle ids
        self._cell_ids: list[list[int]] = []
        # overlay text ids for start/end emoji
        self._overlays: dict[tuple, int] = {}

        self._build_ui()
        self.bind("<Configure>", self._on_window_resize)
        self._schedule_initial_draw()

    def _schedule_initial_draw(self):
        self.after(50, self._rebuild_canvas)

    # ══════════════════════════════════════════════════════════
    #  UI CONSTRUCTION
    # ══════════════════════════════════════════════════════════

    def _build_ui(self):
        self._build_header()

        body = tk.Frame(self, bg=C["bg"])
        body.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        body.rowconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)

        self._build_sidebar(body)
        self._build_canvas_frame(body)

    def _build_header(self):
        hdr = tk.Frame(self, bg=C["panel"], height=52)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_propagate(False)
        hdr.columnconfigure(1, weight=1)

        # left title
        lf = tk.Frame(hdr, bg=C["panel"])
        lf.grid(row=0, column=0, padx=18, pady=10, sticky="w")
        tk.Label(lf, text="⚕", font=("Segoe UI Emoji", 16),
                 bg=C["panel"], fg=C["green"]).pack(side="left", padx=(0, 8))
        tk.Label(lf, text="Emergency Response",
                 font=("Segoe UI", 13, "bold"),
                 bg=C["panel"], fg=C["t1"]).pack(side="left")
        tk.Label(lf, text=" · Routing System",
                 font=("Segoe UI", 13),
                 bg=C["panel"], fg=C["t2"]).pack(side="left")

        # right legend
        rf = tk.Frame(hdr, bg=C["panel"])
        rf.grid(row=0, column=2, padx=18, sticky="e")
        legend = [
            ("Start",    C["start"]),
            ("End",      C["end"]),
            ("Traffic",  C["traffic"]),
            ("Obstacle", C["obstacle"]),
            ("Explored", C["explored"]),
            ("Path",     C["path"]),
        ]
        for lbl, col in legend:
            chip = tk.Frame(rf, bg=C["bg"], padx=7, pady=2)
            chip.pack(side="left", padx=3)
            tk.Frame(chip, bg=col, width=10, height=10).pack(side="left", padx=(0, 4))
            tk.Label(chip, text=lbl, font=("Segoe UI", 8),
                     bg=C["bg"], fg=col).pack(side="left")

    def _build_sidebar(self, parent):
        sb = tk.Frame(parent, bg=C["panel"], width=210)
        sb.grid(row=0, column=0, sticky="ns", padx=(0, 10), pady=8)
        sb.pack_propagate(False)
        sb.grid_propagate(False)

        def sec(text):
            tk.Label(sb, text=text, font=("Segoe UI", 8, "bold"),
                     bg=C["panel"], fg=C["t2"],
                     anchor="w").pack(fill="x", padx=14, pady=(12, 3))

        # Algorithm
        sec("ALGORITHM")
        self._style_ttk()
        cb = ttk.Combobox(sb, textvariable=self.algo_var,
                          values=ALGO_KEYS, state="readonly",
                          font=("Segoe UI", 9), style="Dark.TCombobox")
        cb.pack(fill="x", padx=14, pady=(0, 4))

        # Draw Mode
        sec("DRAW MODE")
        mode_colors = {
            "start":    C["green"],
            "end":      C["red"],
            "obstacle": C["t2"],
            "traffic":  C["amber"],
            "erase":    C["t2"],
        }
        for label, val in MODES:
            fg = mode_colors.get(val, C["t1"])
            tk.Radiobutton(
                sb, text=label, variable=self.draw_mode, value=val,
                bg=C["panel"], fg=fg,
                selectcolor=C["card"],
                activebackground=C["panel"], activeforeground=fg,
                font=("Segoe UI", 10), cursor="hand2",
            ).pack(anchor="w", padx=14, pady=2)

        # Speed
        sec("ANIMATION SPEED")
        sf = tk.Frame(sb, bg=C["panel"])
        sf.pack(fill="x", padx=14)
        tk.Label(sf, text="Fast", font=("Segoe UI", 8),
                 bg=C["panel"], fg=C["t2"]).pack(side="left")
        tk.Label(sf, text="Slow", font=("Segoe UI", 8),
                 bg=C["panel"], fg=C["t2"]).pack(side="right")
        tk.Scale(sb, from_=2, to=80, orient="horizontal",
                 variable=self.speed_var,
                 bg=C["panel"], fg=C["t1"],
                 troughcolor=C["card"],
                 highlightthickness=0, showvalue=False,
                 ).pack(fill="x", padx=14)

        tk.Frame(sb, bg=C["border"], height=1).pack(fill="x", padx=14, pady=10)

        # Buttons
        self.run_btn = self._btn(sb, "▶   Run Algorithm", C["green"], C["bg"], self._on_run)
        self.run_btn.pack(fill="x", padx=14, pady=(0, 6))

        self._btn(sb, "⧖   Compare All 4", C["blue"], C["t1"], self._on_compare
                  ).pack(fill="x", padx=14, pady=(0, 6))

        self._btn(sb, "↺   Clear Path", C["card"], C["t1"], self._on_clear_path
                  ).pack(fill="x", padx=14, pady=(0, 6))

        self._btn(sb, "✕   Reset Grid", C["card"], C["red"], self._on_reset
                  ).pack(fill="x", padx=14, pady=(0, 6))

        tk.Frame(sb, bg=C["border"], height=1).pack(fill="x", padx=14, pady=10)

        # Stats
        sec("STATISTICS")
        stats_wrap = tk.Frame(sb, bg=C["panel"])
        stats_wrap.pack(fill="x", padx=14)

        self.stat_labels = {}
        rows = [
            ("algorithm",      "Algorithm",  C["cyan"]),
            ("path_found",     "Path Found", C["t1"]),
            ("path_length",    "Path Cells", C["t1"]),
            ("path_cost",      "Path Cost",  C["amber"]),
            ("nodes_explored", "Explored",   C["blue"]),
            ("time",           "Time",       C["green"]),
        ]
        for key, label, color in rows:
            row = tk.Frame(stats_wrap, bg=C["card"], pady=5, padx=10)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=label, font=("Segoe UI", 9),
                     bg=C["card"], fg=C["t2"]).pack(side="left")
            val = tk.Label(row, text="—", font=("Segoe UI", 9, "bold"),
                           bg=C["card"], fg=color)
            val.pack(side="right")
            self.stat_labels[key] = val

        tk.Frame(sb, bg=C["border"], height=1).pack(fill="x", padx=14, pady=8)

        self.status_var = tk.StringVar(value="Place start node (🚑)")
        tk.Label(sb, textvariable=self.status_var,
                 font=("Segoe UI", 9, "italic"),
                 bg=C["panel"], fg=C["t2"],
                 wraplength=185, justify="left",
                 ).pack(padx=14, pady=(0, 10), anchor="w")

    def _build_canvas_frame(self, parent):
        cf = tk.Frame(parent, bg=C["bg"])
        cf.grid(row=0, column=1, sticky="nsew", pady=8)
        cf.rowconfigure(0, weight=1)
        cf.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(
            cf, bg=C["bg"],
            highlightthickness=2,
            highlightbackground=C["border"],
            cursor="crosshair",
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.canvas.bind("<Button-1>",        self._on_click)
        self.canvas.bind("<B1-Motion>",       self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)

    # ══════════════════════════════════════════════════════════
    #  RESIZE HANDLING
    # ══════════════════════════════════════════════════════════

    _last_size = (0, 0)

    def _on_window_resize(self, event):
        if event.widget is not self:
            return
        new_size = (event.width, event.height)
        if new_size == self._last_size:
            return
        self._last_size = new_size
        if self._anim_job:
            self.after_cancel(self._anim_job)
            self._anim_job = None
            self.is_animating = False
            self.run_btn.config(state="normal", text="▶   Run Algorithm")
        self.after(80, self._rebuild_canvas)

    def _compute_cell_size(self) -> int:
        self.update_idletasks()
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        if cw < 10 or ch < 10:
            return self._cell_size
        cs = min(cw // GRID_COLS, ch // GRID_ROWS)
        return max(cs, MIN_CELL)

    def _rebuild_canvas(self):
        """Destroy all canvas items and redraw at new cell size."""
        self.canvas.delete("all")
        self._cell_ids   = []
        self._overlays   = {}
        self._cell_size  = self._compute_cell_size()
        cs = self._cell_size

        for r in range(GRID_ROWS):
            row_ids = []
            for c in range(GRID_COLS):
                x1 = c * cs + 1
                y1 = r * cs + 1
                x2 = x1 + cs - 1
                y2 = y1 + cs - 1
                rid = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=C["empty"], outline=C["grid_line"], width=1,
                )
                row_ids.append(rid)
            self._cell_ids.append(row_ids)

        self._redraw_all_cells()

    def _redraw_all_cells(self):
        for node in self.grid_model.all_nodes():
            self._paint_cell(node.row, node.col)

    # ══════════════════════════════════════════════════════════
    #  CELL PAINTING
    # ══════════════════════════════════════════════════════════

    # Map cell_type → colour constant key
    _TYPE_COLOR = {
        START:    "start",
        END:      "end",
        OBSTACLE: "obstacle",
        TRAFFIC:  "traffic",
        EMPTY:    "empty",
    }

    def _base_color(self, node: Node) -> str:
        return C[self._TYPE_COLOR.get(node.cell_type, "empty")]

    def _paint_cell(self, row: int, col: int, override: str | None = None):
        """Paint one cell. override bypasses the node's own colour (for animation)."""
        if not self._cell_ids:
            return
        node  = self.grid_model.get_node(row, col)
        color = override if override else self._base_color(node)
        self.canvas.itemconfig(self._cell_ids[row][col], fill=color)
        self._update_overlay(node, color)

    def _update_overlay(self, node: Node, fill: str):
        key = (node.row, node.col)
        cs  = self._cell_size
        if node.cell_type in (START, END):
            emoji = "🚑" if node.cell_type == START else "🏥"
            fs    = max(8, cs - 10)
            if key not in self._overlays:
                cx = node.col * cs + cs // 2 + 1
                cy = node.row * cs + cs // 2 + 1
                tid = self.canvas.create_text(
                    cx, cy, text=emoji,
                    font=("Segoe UI Emoji", fs),
                )
                self._overlays[key] = tid
        else:
            if key in self._overlays:
                self.canvas.delete(self._overlays.pop(key))

    def _clear_explored_visuals(self):
        """
        Redraw every cell back to its base colour.
        Traffic / obstacle / start / end are preserved exactly.
        """
        for node in self.grid_model.all_nodes():
            self._paint_cell(node.row, node.col)

    # ══════════════════════════════════════════════════════════
    #  MOUSE INPUT
    # ══════════════════════════════════════════════════════════

    def _canvas_to_grid(self, event):
        cs = self._cell_size
        if cs == 0:
            return None
        r = event.y // cs
        c = event.x // cs
        if 0 <= r < GRID_ROWS and 0 <= c < GRID_COLS:
            return r, c
        return None

    def _on_click(self, event):
        if self.is_animating:
            return
        pos = self._canvas_to_grid(event)
        if pos is None:
            return
        self._drag_mode = self.draw_mode.get()
        self._apply_draw(*pos)

    def _on_drag(self, event):
        if self.is_animating or self._drag_mode is None:
            return
        pos = self._canvas_to_grid(event)
        if pos and self._drag_mode in ("obstacle", "traffic", "erase"):
            self._apply_draw(*pos)

    def _on_release(self, event):
        self._drag_mode = None

    def _apply_draw(self, r: int, c: int):
        mode = self._drag_mode or self.draw_mode.get()
        g    = self.grid_model
        if mode == "start":
            # clear old start overlay
            if g.start_node:
                self._paint_cell(g.start_node.row, g.start_node.col)
            g.set_start(r, c)
            self._status("Start placed. Now place End node.")
        elif mode == "end":
            if g.end_node:
                self._paint_cell(g.end_node.row, g.end_node.col)
            g.set_end(r, c)
            self._status("End placed. Draw obstacles / traffic, then Run.")
        elif mode == "obstacle":
            g.set_obstacle(r, c)
        elif mode == "traffic":
            g.set_traffic(r, c)
        elif mode == "erase":
            node = g.get_node(r, c)
            if node.is_start:
                g.start_node = None
            elif node.is_end:
                g.end_node = None
            node.reset_type()
        self._paint_cell(r, c)

    # ══════════════════════════════════════════════════════════
    #  BUTTON HANDLERS
    # ══════════════════════════════════════════════════════════

    def _on_run(self):
        if self.is_animating:
            return
        ready, msg = self.grid_model.is_ready()
        if not ready:
            self._status(f"⚠  {msg}")
            return

        self._cancel_animation()
        self._clear_explored_visuals()

        label = self.algo_var.get()
        algo_name, algo_fn = ALGO_MAP[label]

        self._status(f"Running {algo_name}…")
        self.run_btn.config(state="disabled", text="⏳  Running…")
        self.update_idletasks()

        t0 = time.perf_counter()
        try:
            path, visited = algo_fn(self.grid_model)
        except Exception as e:
            self._status(f"Error: {e}")
            self.run_btn.config(state="normal", text="▶   Run Algorithm")
            return
        elapsed = time.perf_counter() - t0

        stats = format_stats(algo_name, path, visited, elapsed)
        self._update_stats(stats)

        if not path:
            self._status("⚠  No path found — destination unreachable.")
            self.run_btn.config(state="normal", text="▶   Run Algorithm")
            return

        self._animate(visited, path, algo_name)

    def _on_compare(self):
        if self.is_animating:
            return
        ready, msg = self.grid_model.is_ready()
        if not ready:
            self._status(f"⚠  {msg}")
            return
        CompareDialog(self, self.grid_model)

    def _on_clear_path(self):
        self._cancel_animation()
        self.grid_model.reset_search_state()
        self._clear_explored_visuals()
        self._reset_stats()
        self._status("Path cleared. Ready to run again.")

    def _on_reset(self):
        self._cancel_animation()
        self.grid_model.reset_grid()
        self._clear_explored_visuals()
        self._reset_stats()
        self._status("Grid reset. Place start node (🚑).")
        self.run_btn.config(state="normal", text="▶   Run Algorithm")

    # ══════════════════════════════════════════════════════════
    #  ANIMATION ENGINE
    # ══════════════════════════════════════════════════════════

    def _animate(self, visited: list[Node], path: list[Node], name: str):
        self.is_animating = True
        delay = self.speed_var.get()

        skip = {self.grid_model.start_node, self.grid_model.end_node}

        # Build animation frames — explored then path
        anim_v = [n for n in visited if n not in skip]
        anim_p = [n for n in path    if n not in skip]

        total_v = len(anim_v)

        def step_v(i):
            if i >= total_v:
                self._status(f"{name}: explored {total_v} nodes. Drawing path…")
                self._anim_job = self.after(delay * 4, lambda: step_p(0))
                return
            n = anim_v[i]
            # Only paint explored if the cell is not traffic/obstacle
            # Traffic cells get a BLENDED colour so they're still
            # recognisable as traffic while showing they were explored.
            if n.cell_type == TRAFFIC:
                self._paint_cell(n.row, n.col, "#C97A30")  # dark amber = traffic+explored
            else:
                self._paint_cell(n.row, n.col, C["explored"])
            self._anim_job = self.after(delay, lambda: step_v(i + 1))

        def step_p(i):
            if i >= len(anim_p):
                self.is_animating = False
                self.run_btn.config(state="normal", text="▶   Run Algorithm")
                total_e = len(visited)
                plen    = len(path)
                pcost   = sum(n.cost for n in path)
                self._status(
                    f"{name} done: {plen} cells, cost {pcost}, "
                    f"total {total_e} explored."
                )
                return
            n = anim_p[i]
            # Path is ALWAYS cyan — drawn on top of everything including traffic
            self._paint_cell(n.row, n.col, C["path"])
            self._anim_job = self.after(delay * 2, lambda: step_p(i + 1))

        step_v(0)

    def _cancel_animation(self):
        if self._anim_job is not None:
            self.after_cancel(self._anim_job)
            self._anim_job = None
        self.is_animating = False
        self.run_btn.config(state="normal", text="▶   Run Algorithm")

    # ══════════════════════════════════════════════════════════
    #  STATS
    # ══════════════════════════════════════════════════════════

    def _update_stats(self, stats: dict):
        self.stat_labels["algorithm"     ].config(text=stats["algorithm"])
        self.stat_labels["path_found"    ].config(
            text="✓ Yes" if stats["path_found"] else "✗ No",
            fg=C["green"] if stats["path_found"] else C["red"],
        )
        self.stat_labels["path_length"   ].config(text=f'{stats["path_length"]} cells')
        self.stat_labels["path_cost"     ].config(text=str(stats["path_cost"]))
        self.stat_labels["nodes_explored"].config(text=str(stats["nodes_explored"]))
        self.stat_labels["time"          ].config(text=stats["time"])

    def _reset_stats(self):
        for lbl in self.stat_labels.values():
            lbl.config(text="—", fg=C["t2"])

    def _status(self, msg: str):
        self.status_var.set(msg)
        self.update_idletasks()

    # ══════════════════════════════════════════════════════════
    #  TTK STYLE
    # ══════════════════════════════════════════════════════════

    def _style_ttk(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("Dark.TCombobox",
                    fieldbackground=C["card"],
                    background=C["card"],
                    foreground=C["t1"],
                    selectbackground=C["card"],
                    selectforeground=C["t1"],
                    bordercolor=C["border"],
                    arrowcolor=C["green"],
                    )

    def _btn(self, parent, text, bg, fg, cmd):
        return tk.Button(
            parent, text=text, bg=bg, fg=fg,
            font=("Segoe UI", 10, "bold"),
            relief="flat", bd=0, padx=10, pady=8,
            cursor="hand2",
            activebackground=C["border"],
            activeforeground=fg,
            command=cmd,
        )