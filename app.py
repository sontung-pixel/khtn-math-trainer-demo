import json
import re
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk


APP_NAME = "KHTN Math Trainer - Demo"


PROBLEMS = [
    {
        "id": "foundation-divisor",
        "source": "Luyện nền",
        "title": "Tạo phương trình ước số",
        "problem": "Tìm các cặp số nguyên (x, y) thỏa mãn:\nxy + 2x + 3y = 7.",
        "goal": "Thêm bớt để đưa phương trình về dạng tích bằng một hằng số.",
        "steps": [
            {
                "prompt": "Bạn hãy biến đổi phương trình thành một tích.",
                "kind": "factor",
                "answers": ["(x+3)(y+2)=13", "(y+2)(x+3)=13"],
                "hint": "Hãy so sánh xy + 2x + 3y với (x + 3)(y + 2).",
                "official": "Ta có xy + 2x + 3y = 7 tương đương với (x + 3)(y + 2) = 13."
            },
            {
                "prompt": "Từ đó, hai thừa số có thể nhận những cặp giá trị nào?",
                "kind": "divisors13",
                "answers": ["(1,13),(13,1),(-1,-13),(-13,-1)"],
                "hint": "Đừng quên các ước âm của 13.",
                "official": "Vì x, y là các số nguyên nên (x + 3, y + 2) lần lượt bằng (1, 13), (13, 1), (-1, -13) hoặc (-13, -1)."
            },
            {
                "prompt": "Hãy ghi tất cả nghiệm của phương trình.",
                "kind": "solutions_foundation",
                "answers": ["(-2,11),(10,-1),(-4,-15),(-16,-3)"],
                "hint": "Từ mỗi cặp (x + 3, y + 2), trừ lần lượt 3 và 2.",
                "official": "Vậy phương trình có đúng bốn nghiệm nguyên: (-2, 11), (10, -1), (-4, -15), (-16, -3)."
            }
        ]
    },
    {
        "id": "khtn-2019",
        "source": "KHTN 2019",
        "title": "Chia hết để giới hạn ẩn",
        "problem": "Tìm các cặp số nguyên (x, y) thỏa mãn:\n(x² - x + 1)(y² + xy) = 3x - 1.",
        "goal": "Dùng quan hệ chia hết để giới hạn x trước, rồi mới tìm y.",
        "steps": [
            {
                "prompt": "Từ phương trình, bạn suy ra quan hệ chia hết nào?",
                "kind": "divides",
                "answers": ["x^2-x+1|3x-1"],
                "hint": "Vế trái chứa nhân tử x² - x + 1.",
                "official": "Từ phương trình, suy ra x² - x + 1 chia hết cho 3x - 1."
            },
            {
                "prompt": "Hãy tìm một hằng số mà x² - x + 1 phải là ước của nó.",
                "kind": "divides7",
                "answers": ["x^2-x+1|7"],
                "hint": "Nhân 3x - 1 với 3x - 2 rồi so sánh với 9(x² - x + 1).",
                "official": "Ta có (3x - 1)(3x - 2) = 9(x² - x + 1) - 7. Do đó x² - x + 1 chia hết cho 7."
            },
            {
                "prompt": "Suy ra x có thể nhận những giá trị nào?",
                "kind": "xvalues",
                "answers": ["x=-2,0,1,3"],
                "hint": "Vì x² - x + 1 > 0 nên nó chỉ có thể bằng 1 hoặc 7.",
                "official": "Vì x² - x + 1 > 0 nên x² - x + 1 thuộc {1, 7}. Suy ra x thuộc {-2, 0, 1, 3}."
            },
            {
                "prompt": "Thử từng giá trị và kết luận tất cả nghiệm.",
                "kind": "solutions_khtn",
                "answers": ["(1,1),(1,-2),(-2,1)"],
                "hint": "Thay từng giá trị x vào phương trình ban đầu và giải phương trình theo y.",
                "official": "Thử lại các giá trị trên, ta được đúng ba nghiệm nguyên: (1, 1), (1, -2), (-2, 1)."
            }
        ]
    },
    {
        "id": "language-practice",
        "source": "Kỹ năng",
        "title": "Viết một ý theo hai cách",
        "problem": "Cho a, b là các số nguyên dương nguyên tố cùng nhau và ab là số chính phương. Hãy nêu kết luận.",
        "goal": "Diễn đạt cùng một ý bằng Nháp nhanh hoặc Trình bày đi thi.",
        "steps": [
            {
                "prompt": "Bạn kết luận được gì về a và b?",
                "kind": "coprime_square",
                "answers": ["a,b đều là số chính phương"],
                "hint": "Xét số mũ của mỗi thừa số nguyên tố trong a và b.",
                "official": "Vì a và b là hai số nguyên dương nguyên tố cùng nhau, đồng thời ab là số chính phương nên a và b đều là các số chính phương."
            }
        ]
    }
]


def compact(text: str) -> str:
    text = text.lower().strip()
    replacements = {
        "²": "^2", "−": "-", "–": "-", "⇒": "=>", "⇔": "<=>",
        "chia hết cho": "chc", "nguyên tố cùng nhau": "ntc",
        "số chính phương": "scp", "thuộc": "in", " hoặc ": ","
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"\s+", "", text)
    return text


def extract_pairs(text: str):
    return {
        (int(a), int(b))
        for a, b in re.findall(r"\(?\s*(-?\d+)\s*[,;]\s*(-?\d+)\s*\)?", text)
    }


def extract_ints(text: str):
    return {int(x) for x in re.findall(r"(?<![\^\w])-?\d+", text.replace("²", "^2"))}


def interpret(text: str) -> str:
    raw = text.strip()
    c = compact(raw)
    if not raw:
        return "Bạn chưa nhập câu trả lời."
    if c in {"goiy", "hint", "ket", "kẹt"} or "gợiý" in c:
        return "Bạn đang yêu cầu một gợi ý."
    if "chc" in c or "|" in c:
        return "Bạn đang nêu một quan hệ chia hết."
    if "ntc" in c and ("scp" in c or "chínhphương" in c):
        return "Bạn đang dùng tính nguyên tố cùng nhau và tính chất số chính phương."
    if extract_pairs(raw):
        return f"Bạn đang đưa ra các cặp số: {sorted(extract_pairs(raw))}."
    if "=" in raw or "<=>" in c:
        return "Bạn đang thực hiện một phép biến đổi hoặc đưa ra giá trị của ẩn."
    return "Bạn đang đưa ra một bước giải bằng lời."


def is_correct(kind: str, text: str) -> tuple[bool, str]:
    c = compact(text)
    if kind == "factor":
        ok = ("(x+3)(y+2)=13" in c or "(y+2)(x+3)=13" in c)
    elif kind == "divisors13":
        ok = extract_pairs(text) >= {(1, 13), (13, 1), (-1, -13), (-13, -1)}
    elif kind == "solutions_foundation":
        ok = extract_pairs(text) >= {(-2, 11), (10, -1), (-4, -15), (-16, -3)}
    elif kind == "divides":
        left = "x^2-x+1"
        ok = (left + "|3x-1" in c) or ("3x-1chc" + left in c)
    elif kind == "divides7":
        left = "x^2-x+1"
        ok = (left + "|7" in c) or ("7chc" + left in c)
    elif kind == "xvalues":
        ok = extract_ints(text) >= {-2, 0, 1, 3}
    elif kind == "solutions_khtn":
        ok = extract_pairs(text) >= {(1, 1), (1, -2), (-2, 1)}
    elif kind == "coprime_square":
        has_both = ("a" in c and "b" in c)
        has_square = "scp" in c or "chínhphương" in c
        ok = has_both and has_square
    else:
        ok = False
    if ok:
        return True, "Bước này hợp lệ."
    return False, "Tôi chưa xác nhận được bước này. Hãy kiểm tra lại hoặc dùng một gợi ý nhẹ."


class ProgressStore:
    def __init__(self):
        self.path = Path.home() / ".khtn_math_demo_progress.json"
        self.data = {"steps": {}}
        try:
            self.data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            pass

    def get(self, problem_id):
        return int(self.data.get("steps", {}).get(problem_id, 0))

    def set(self, problem_id, step):
        self.data.setdefault("steps", {})[problem_id] = step
        try:
            self.path.write_text(json.dumps(self.data, ensure_ascii=False), encoding="utf-8")
        except OSError:
            pass


class MathTrainer(tk.Tk):
    BG = "#0d1321"
    PANEL = "#151d2f"
    PANEL_2 = "#1b2640"
    TEXT = "#edf2ff"
    MUTED = "#9eabc7"
    ACCENT = "#7c8cff"
    SUCCESS = "#50d890"
    WARNING = "#ffc857"
    DANGER = "#ff7085"

    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1120x720")
        self.minsize(920, 620)
        self.configure(bg=self.BG)
        self.store = ProgressStore()
        self.problem_index = 0
        self.step_index = 0
        self.mode = tk.StringVar(value="informal")
        self._style()
        self._build()
        self.load_problem(0)

    def _style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=self.BG)
        style.configure("Panel.TFrame", background=self.PANEL)
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=(12, 9))
        style.configure("Accent.TButton", background=self.ACCENT, foreground="white")
        style.map("Accent.TButton", background=[("active", "#95a1ff")])
        style.configure("Ghost.TButton", background=self.PANEL_2, foreground=self.TEXT)
        style.map("Ghost.TButton", background=[("active", "#263452")])
        style.configure("Horizontal.TProgressbar", troughcolor=self.PANEL_2, background=self.ACCENT)

    def _label(self, parent, text="", size=11, color=None, weight="normal", **kwargs):
        return tk.Label(parent, text=text, bg=kwargs.pop("bg", parent.cget("bg")),
                        fg=color or self.TEXT, font=("Segoe UI", size, weight), **kwargs)

    def _build(self):
        root = ttk.Frame(self)
        root.pack(fill="both", expand=True)

        sidebar = tk.Frame(root, bg="#10182a", width=270)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        self._label(sidebar, "KHTN", 24, self.ACCENT, "bold", bg="#10182a").pack(anchor="w", padx=24, pady=(24, 0))
        self._label(sidebar, "Math Trainer • Demo", 11, self.MUTED, bg="#10182a").pack(anchor="w", padx=24, pady=(0, 24))
        self.lesson_buttons = []
        for i, problem in enumerate(PROBLEMS):
            btn = tk.Button(sidebar, text=f"{i+1}. {problem['title']}", anchor="w",
                            command=lambda idx=i: self.load_problem(idx), relief="flat",
                            bg="#10182a", fg=self.TEXT, activebackground=self.PANEL_2,
                            activeforeground="white", font=("Segoe UI", 10), padx=22, pady=12,
                            cursor="hand2", wraplength=215, justify="left")
            btn.pack(fill="x")
            self.lesson_buttons.append(btn)
        self._label(sidebar, "Dữ liệu được lưu tự động trên máy.", 9, self.MUTED,
                    bg="#10182a", wraplength=210, justify="left").pack(side="bottom", anchor="w", padx=24, pady=20)

        main = tk.Frame(root, bg=self.BG)
        main.pack(side="left", fill="both", expand=True, padx=34, pady=24)

        header = tk.Frame(main, bg=self.BG)
        header.pack(fill="x")
        self.source_label = self._label(header, "", 9, self.ACCENT, "bold")
        self.source_label.pack(anchor="w")
        self.title_label = self._label(header, "", 22, weight="bold")
        self.title_label.pack(anchor="w", pady=(2, 12))
        self.progress = ttk.Progressbar(header, mode="determinate")
        self.progress.pack(fill="x")
        self.progress_label = self._label(header, "", 9, self.MUTED)
        self.progress_label.pack(anchor="e", pady=(4, 12))

        card = tk.Frame(main, bg=self.PANEL, highlightthickness=1, highlightbackground="#25304a")
        card.pack(fill="both", expand=True)
        self.problem_label = self._label(card, "", 14, weight="bold", bg=self.PANEL,
                                         justify="left", anchor="w", wraplength=720)
        self.problem_label.pack(fill="x", padx=24, pady=(22, 12))
        self.goal_label = self._label(card, "", 10, self.MUTED, bg=self.PANEL,
                                      justify="left", anchor="w", wraplength=720)
        self.goal_label.pack(fill="x", padx=24, pady=(0, 18))

        divider = tk.Frame(card, height=1, bg="#29344e")
        divider.pack(fill="x", padx=24)

        mode_row = tk.Frame(card, bg=self.PANEL)
        mode_row.pack(fill="x", padx=24, pady=(16, 8))
        self._label(mode_row, "Cách viết:", 10, self.MUTED, bg=self.PANEL).pack(side="left")
        tk.Radiobutton(mode_row, text="Nháp nhanh", variable=self.mode, value="informal",
                       command=self.update_mode_note, bg=self.PANEL, fg=self.TEXT,
                       selectcolor=self.PANEL_2, activebackground=self.PANEL,
                       activeforeground=self.TEXT, font=("Segoe UI", 10)).pack(side="left", padx=(12, 6))
        tk.Radiobutton(mode_row, text="Trình bày đi thi", variable=self.mode, value="official",
                       command=self.update_mode_note, bg=self.PANEL, fg=self.TEXT,
                       selectcolor=self.PANEL_2, activebackground=self.PANEL,
                       activeforeground=self.TEXT, font=("Segoe UI", 10)).pack(side="left")
        self.mode_note = self._label(mode_row, "", 9, self.MUTED, bg=self.PANEL)
        self.mode_note.pack(side="right")

        self.prompt_label = self._label(card, "", 11, weight="bold", bg=self.PANEL,
                                        justify="left", anchor="w", wraplength=720)
        self.prompt_label.pack(fill="x", padx=24, pady=(6, 8))
        self.answer = tk.Text(card, height=4, bg="#0f1728", fg=self.TEXT, insertbackground="white",
                              selectbackground=self.ACCENT, relief="flat", font=("Segoe UI", 12),
                              padx=14, pady=12, wrap="word", undo=True)
        self.answer.pack(fill="x", padx=24)
        self.answer.bind("<Control-Return>", lambda _: self.check_answer())

        actions = tk.Frame(card, bg=self.PANEL)
        actions.pack(fill="x", padx=24, pady=14)
        ttk.Button(actions, text="Kiểm tra bước này", style="Accent.TButton", command=self.check_answer).pack(side="left")
        ttk.Button(actions, text="Tôi kẹt", style="Ghost.TButton", command=self.show_hint).pack(side="left", padx=8)
        ttk.Button(actions, text="Xem app hiểu gì", style="Ghost.TButton", command=self.show_interpretation).pack(side="left")
        ttk.Button(actions, text="Viết câu chuẩn", style="Ghost.TButton", command=self.show_official).pack(side="right")

        self.feedback = self._label(card, "", 10, self.MUTED, bg=self.PANEL_2,
                                    justify="left", anchor="w", wraplength=720)
        self.feedback.pack(fill="x", padx=24, pady=(0, 22), ipady=12)

    def load_problem(self, index):
        self.problem_index = index
        problem = PROBLEMS[index]
        saved = self.store.get(problem["id"])
        self.step_index = min(saved, len(problem["steps"]) - 1)
        for i, btn in enumerate(self.lesson_buttons):
            btn.configure(bg=self.PANEL_2 if i == index else "#10182a",
                          fg="white" if i == index else self.TEXT)
        self.source_label.configure(text=problem["source"].upper())
        self.title_label.configure(text=problem["title"])
        self.problem_label.configure(text=problem["problem"])
        self.goal_label.configure(text="Mục tiêu: " + problem["goal"])
        self.answer.delete("1.0", "end")
        self.feedback.configure(text="Cứ viết theo cách bạn đang nghĩ. App sẽ kiểm tra từng bước.", fg=self.MUTED)
        self.render_step()
        self.update_mode_note()

    def render_step(self):
        problem = PROBLEMS[self.problem_index]
        step = problem["steps"][self.step_index]
        total = len(problem["steps"])
        self.prompt_label.configure(text=f"Bước {self.step_index + 1}: {step['prompt']}")
        self.progress["maximum"] = total
        self.progress["value"] = self.step_index
        self.progress_label.configure(text=f"{self.step_index}/{total} bước đã hoàn thành")

    def update_mode_note(self):
        if self.mode.get() == "informal":
            self.mode_note.configure(text="Viết tắt cũng được: chc, ntc, scp…")
        else:
            self.mode_note.configure(text="Viết đầy đủ như trong bài kiểm tra")

    def current_step(self):
        return PROBLEMS[self.problem_index]["steps"][self.step_index]

    def show_interpretation(self):
        text = self.answer.get("1.0", "end").strip()
        self.feedback.configure(text="App hiểu: " + interpret(text), fg=self.WARNING)

    def show_hint(self):
        self.feedback.configure(text="Gợi ý nhẹ: " + self.current_step()["hint"], fg=self.WARNING)

    def show_official(self):
        self.feedback.configure(text="Cách trình bày đi thi:\n" + self.current_step()["official"], fg=self.ACCENT)

    def check_answer(self):
        text = self.answer.get("1.0", "end").strip()
        if not text:
            self.feedback.configure(text="Bạn chưa nhập bước giải. Nếu đang kẹt, hãy bấm “Tôi kẹt” nhé.", fg=self.WARNING)
            return
        ok, reason = is_correct(self.current_step()["kind"], text)
        if not ok:
            self.feedback.configure(text=f"App hiểu: {interpret(text)}\n\n{reason}", fg=self.DANGER)
            return
        problem = PROBLEMS[self.problem_index]
        if self.step_index + 1 < len(problem["steps"]):
            official = self.current_step()["official"]
            self.step_index += 1
            self.store.set(problem["id"], self.step_index)
            self.answer.delete("1.0", "end")
            self.render_step()
            self.feedback.configure(text="Đúng rồi. ✓\n\nCách trình bày đi thi:\n" + official, fg=self.SUCCESS)
        else:
            self.store.set(problem["id"], len(problem["steps"]))
            self.progress["value"] = len(problem["steps"])
            self.progress_label.configure(text=f"{len(problem['steps'])}/{len(problem['steps'])} bước đã hoàn thành")
            self.feedback.configure(text="Hoàn thành bài! ✓ Bạn đã đi hết đường giải, không chỉ tìm được đáp số.", fg=self.SUCCESS)
            messagebox.showinfo("Hoàn thành", "Bạn đã hoàn thành bài demo này!")


if __name__ == "__main__":
    MathTrainer().mainloop()
