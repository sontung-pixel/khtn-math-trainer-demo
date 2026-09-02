import json
import re
import tkinter as tk
import ctypes
from pathlib import Path
from tkinter import messagebox

import customtkinter as ctk


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


class MathTrainer(ctk.CTk):
    BG = "#0B1020"
    SIDEBAR = "#10172A"
    PANEL = "#141D33"
    PANEL_2 = "#1B2742"
    INPUT = "#0E1629"
    BORDER = "#2A3859"
    TEXT = "#F3F6FF"
    MUTED = "#9BA9C7"
    ACCENT = "#756AF8"
    ACCENT_HOVER = "#887FFF"
    SUCCESS = "#45D69A"
    WARNING = "#F5C451"
    DANGER = "#FF7186"

    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1240x790")
        self.minsize(1060, 680)
        self.configure(fg_color=self.BG)
        self.store = ProgressStore()
        self.problem_index = 0
        self.step_index = 0
        self.mode = tk.StringVar(value="informal")
        self._build()
        self.load_problem(0)

    def _label(self, parent, text="", size=14, color=None, weight="normal", **kwargs):
        kwargs.pop("bg", None)
        anchor = kwargs.pop("anchor", None)
        label = ctk.CTkLabel(parent, text=text, text_color=color or self.TEXT,
                             font=ctk.CTkFont("Segoe UI", size, weight=weight), **kwargs)
        if anchor:
            label.configure(anchor=anchor)
        return label

    def _button(self, parent, text, command, primary=False, width=0):
        return ctk.CTkButton(parent, text=text, command=command, width=width, height=40,
                             corner_radius=10, border_width=0 if primary else 1,
                             border_color=self.BORDER,
                             fg_color=self.ACCENT if primary else self.PANEL_2,
                             hover_color=self.ACCENT_HOVER if primary else "#263554",
                             text_color="white", font=ctk.CTkFont("Segoe UI", 13, weight="bold"))

    def _build(self):
        root = ctk.CTkFrame(self, fg_color=self.BG, corner_radius=0)
        root.pack(fill="both", expand=True)

        sidebar = ctk.CTkFrame(root, fg_color=self.SIDEBAR, width=292, corner_radius=0)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        brand = ctk.CTkFrame(sidebar, fg_color="transparent")
        brand.pack(fill="x", padx=24, pady=(25, 20))
        ctk.CTkLabel(brand, text="K", width=42, height=42, corner_radius=12,
                     fg_color=self.ACCENT, text_color="white",
                     font=ctk.CTkFont("Segoe UI", 22, weight="bold")).pack(side="left")
        brand_text = ctk.CTkFrame(brand, fg_color="transparent")
        brand_text.pack(side="left", padx=12)
        self._label(brand_text, "KHTN Math", 19, weight="bold").pack(anchor="w")
        self._label(brand_text, "TRAINER  •  DEMO V0.2", 10, self.MUTED, "bold").pack(anchor="w")

        self._label(sidebar, "LỘ TRÌNH CỦA BẠN", 10, self.MUTED, "bold").pack(anchor="w", padx=25, pady=(5, 9))
        self.lesson_buttons = []
        for i, problem in enumerate(PROBLEMS):
            btn = ctk.CTkButton(sidebar, text=f"  {i+1:02d}   {problem['title']}", anchor="w",
                                command=lambda idx=i: self.load_problem(idx), height=52,
                                corner_radius=10, fg_color="transparent", hover_color=self.PANEL_2,
                                text_color=self.TEXT, font=ctk.CTkFont("Segoe UI", 13),
                                wraplength=220)
            btn.pack(fill="x", padx=14, pady=3)
            self.lesson_buttons.append(btn)

        footer = ctk.CTkFrame(sidebar, fg_color=self.PANEL, corner_radius=12)
        footer.pack(side="bottom", fill="x", padx=16, pady=18)
        self._label(footer, "●  HỌC OFFLINE", 10, self.SUCCESS, "bold").pack(anchor="w", padx=15, pady=(12, 3))
        self._label(footer, "Tiến độ được lưu tự động\ntrên máy của bạn.", 11, self.MUTED,
                    justify="left").pack(anchor="w", padx=15, pady=(0, 12))

        main = ctk.CTkFrame(root, fg_color=self.BG, corner_radius=0)
        main.pack(side="left", fill="both", expand=True, padx=38, pady=27)

        header = ctk.CTkFrame(main, fg_color="transparent")
        header.pack(fill="x")
        self.source_label = self._label(header, "", 11, self.ACCENT, "bold")
        self.source_label.pack(anchor="w")
        self.title_label = self._label(header, "", 28, weight="bold")
        self.title_label.pack(anchor="w", pady=(2, 13))
        progress_row = ctk.CTkFrame(header, fg_color="transparent")
        progress_row.pack(fill="x", pady=(0, 16))
        self.progress = ctk.CTkProgressBar(progress_row, height=8, corner_radius=4,
                                           progress_color=self.ACCENT, fg_color=self.PANEL_2)
        self.progress.pack(side="left", fill="x", expand=True, pady=5)
        self.progress_label = self._label(progress_row, "", 11, self.MUTED, "bold")
        self.progress_label.pack(side="right", padx=(16, 0))

        card = ctk.CTkFrame(main, fg_color=self.PANEL, corner_radius=18,
                            border_width=1, border_color=self.BORDER)
        card.pack(fill="both", expand=True)
        problem_box = ctk.CTkFrame(card, fg_color="#19243D", corner_radius=13)
        problem_box.pack(fill="x", padx=22, pady=(22, 12))
        self._label(problem_box, "ĐỀ BÀI", 10, self.ACCENT, "bold").pack(anchor="w", padx=18, pady=(14, 4))
        self.problem_label = self._label(problem_box, "", 17, weight="bold",
                                         justify="left", anchor="w", wraplength=800)
        self.problem_label.pack(fill="x", padx=18, pady=(0, 8))
        self.goal_label = self._label(problem_box, "", 12, self.MUTED,
                                      justify="left", anchor="w", wraplength=800)
        self.goal_label.pack(fill="x", padx=18, pady=(0, 15))

        mode_row = ctk.CTkFrame(card, fg_color="transparent")
        mode_row.pack(fill="x", padx=24, pady=(5, 8))
        self.segmented = ctk.CTkSegmentedButton(mode_row, values=["Nháp nhanh", "Trình bày đi thi"],
                                                command=self.change_mode, height=36, corner_radius=9,
                                                selected_color=self.ACCENT, selected_hover_color=self.ACCENT_HOVER,
                                                unselected_color=self.PANEL_2, unselected_hover_color="#263554")
        self.segmented.set("Nháp nhanh")
        self.segmented.pack(side="left")
        self.mode_note = self._label(mode_row, "", 11, self.MUTED)
        self.mode_note.pack(side="right")

        self.prompt_label = self._label(card, "", 14, weight="bold",
                                        justify="left", anchor="w", wraplength=800)
        self.prompt_label.pack(fill="x", padx=24, pady=(8, 9))
        self.answer = ctk.CTkTextbox(card, height=104, fg_color=self.INPUT, border_width=1,
                                     border_color=self.BORDER, corner_radius=12, text_color=self.TEXT,
                                     font=ctk.CTkFont("Segoe UI", 15), wrap="word", undo=True)
        self.answer.pack(fill="x", padx=24)
        self.answer.bind("<Control-Return>", lambda _: self.check_answer())

        actions = ctk.CTkFrame(card, fg_color="transparent")
        actions.pack(fill="x", padx=24, pady=12)
        self._button(actions, "Kiểm tra bước  →", self.check_answer, True).pack(side="left")
        self._button(actions, "Gợi ý", self.show_hint).pack(side="left", padx=8)
        self._button(actions, "App hiểu gì?", self.show_interpretation).pack(side="left")
        self._button(actions, "Câu chuẩn", self.show_official).pack(side="right")

        self.feedback_box = ctk.CTkFrame(card, fg_color=self.PANEL_2, corner_radius=12)
        self.feedback_box.pack(fill="x", padx=24, pady=(0, 22))
        self.feedback_icon = self._label(self.feedback_box, "●", 14, self.ACCENT, "bold")
        self.feedback_icon.pack(side="left", padx=(15, 9), pady=13, anchor="n")
        self.feedback = self._label(self.feedback_box, "", 12, self.MUTED,
                                    justify="left", anchor="w", wraplength=750)
        self.feedback.pack(side="left", fill="x", expand=True, padx=(0, 14), pady=12)

    def change_mode(self, value):
        self.mode.set("informal" if value == "Nháp nhanh" else "official")
        self.update_mode_note()

    def load_problem(self, index):
        self.problem_index = index
        problem = PROBLEMS[index]
        saved = self.store.get(problem["id"])
        self.step_index = min(saved, len(problem["steps"]) - 1)
        for i, btn in enumerate(self.lesson_buttons):
            btn.configure(fg_color=self.PANEL_2 if i == index else "transparent",
                          text_color="white" if i == index else self.TEXT)
        self.source_label.configure(text=problem["source"].upper())
        self.title_label.configure(text=problem["title"])
        self.problem_label.configure(text=problem["problem"])
        self.goal_label.configure(text="Mục tiêu: " + problem["goal"])
        self.answer.delete("1.0", "end")
        self.set_feedback("Cứ viết theo cách bạn đang nghĩ. App sẽ kiểm tra từng bước.", self.MUTED)
        self.render_step()
        self.update_mode_note()

    def render_step(self):
        problem = PROBLEMS[self.problem_index]
        step = problem["steps"][self.step_index]
        total = len(problem["steps"])
        self.prompt_label.configure(text=f"Bước {self.step_index + 1}: {step['prompt']}")
        self.progress.set(self.step_index / total)
        self.progress_label.configure(text=f"{self.step_index}/{total} bước đã hoàn thành")

    def update_mode_note(self):
        if self.mode.get() == "informal":
            self.mode_note.configure(text="Viết tắt cũng được: chc, ntc, scp…")
        else:
            self.mode_note.configure(text="Viết đầy đủ như trong bài kiểm tra")

    def current_step(self):
        return PROBLEMS[self.problem_index]["steps"][self.step_index]

    def set_feedback(self, text, color):
        self.feedback.configure(text=text, text_color=color)
        self.feedback_icon.configure(text_color=color)

    def show_interpretation(self):
        text = self.answer.get("1.0", "end").strip()
        self.set_feedback("App hiểu: " + interpret(text), self.WARNING)

    def show_hint(self):
        self.set_feedback("Gợi ý nhẹ: " + self.current_step()["hint"], self.WARNING)

    def show_official(self):
        self.set_feedback("Cách trình bày đi thi:\n" + self.current_step()["official"], self.ACCENT)

    def check_answer(self):
        text = self.answer.get("1.0", "end").strip()
        if not text:
            self.set_feedback("Bạn chưa nhập bước giải. Nếu đang kẹt, hãy bấm “Gợi ý” nhé.", self.WARNING)
            return
        ok, reason = is_correct(self.current_step()["kind"], text)
        if not ok:
            self.set_feedback(f"App hiểu: {interpret(text)}\n\n{reason}", self.DANGER)
            return
        problem = PROBLEMS[self.problem_index]
        if self.step_index + 1 < len(problem["steps"]):
            official = self.current_step()["official"]
            self.step_index += 1
            self.store.set(problem["id"], self.step_index)
            self.answer.delete("1.0", "end")
            self.render_step()
            self.set_feedback("Đúng rồi. ✓\n\nCách trình bày đi thi:\n" + official, self.SUCCESS)
        else:
            self.store.set(problem["id"], len(problem["steps"]))
            self.progress.set(1)
            self.progress_label.configure(text=f"{len(problem['steps'])}/{len(problem['steps'])} bước đã hoàn thành")
            self.set_feedback("Hoàn thành bài! ✓ Bạn đã đi hết đường giải, không chỉ tìm được đáp số.", self.SUCCESS)
            messagebox.showinfo("Hoàn thành", "Bạn đã hoàn thành bài demo này!")


if __name__ == "__main__":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except (AttributeError, OSError):
        pass
    MathTrainer().mainloop()
