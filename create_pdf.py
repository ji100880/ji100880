from __future__ import annotations

from pathlib import Path
from textwrap import wrap

OUTPUT_FILE = Path("CHATGPT_PRO_Guide_Blue_Edition.pdf")
PAGE_WIDTH = 595
PAGE_HEIGHT = 842


class PdfBuilder:
    def __init__(self) -> None:
        self.objects: list[str] = []
        self.font_regular = self.add_object("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
        self.font_bold = self.add_object("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")

    def add_object(self, obj: str) -> int:
        self.objects.append(obj)
        return len(self.objects)

    @staticmethod
    def esc(text: str) -> str:
        return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

    def add_stream(self, commands: list[str]) -> int:
        payload = "\n".join(commands)
        length = len(payload.encode("latin-1", errors="replace"))
        return self.add_object(f"<< /Length {length} >>\nstream\n{payload}\nendstream")

    def draw_wrapped_text(
        self,
        commands: list[str],
        text: str,
        x: int,
        y: int,
        size: int = 12,
        bold: bool = False,
        max_chars: int = 80,
        line_gap: int = 16,
    ) -> int:
        font = "F2" if bold else "F1"
        for line in wrap(text, width=max_chars):
            commands.append(f"BT /{font} {size} Tf {x} {y} Td ({self.esc(line)}) Tj ET")
            y -= line_gap
        return y

    def build(self, content_ids: list[int], output: Path = OUTPUT_FILE) -> None:
        pages_id = self.add_object("")
        page_ids: list[int] = []

        for cid in content_ids:
            page_ids.append(
                self.add_object(
                    "<< /Type /Page "
                    f"/Parent {pages_id} 0 R "
                    f"/MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
                    f"/Resources << /Font << /F1 {self.font_regular} 0 R /F2 {self.font_bold} 0 R >> >> "
                    f"/Contents {cid} 0 R >>"
                )
            )

        kids = " ".join(f"{pid} 0 R" for pid in page_ids)
        self.objects[pages_id - 1] = f"<< /Type /Pages /Count {len(page_ids)} /Kids [{kids}] >>"

        info_id = self.add_object(
            "<< /Title (ChatGPT PRO Guide Blue Edition) "
            "/Author (Codex Assistant) "
            "/Subject (Practical usage guide for ChatGPT PRO subscribers) >>"
        )
        catalog_id = self.add_object(f"<< /Type /Catalog /Pages {pages_id} 0 R >>")

        chunks: list[str] = ["%PDF-1.4\n"]
        offsets = [0]
        for i, obj in enumerate(self.objects, start=1):
            offsets.append(sum(len(c.encode("latin-1")) for c in chunks))
            chunks.append(f"{i} 0 obj\n{obj}\nendobj\n")

        xref_pos = sum(len(c.encode("latin-1")) for c in chunks)
        chunks.append(f"xref\n0 {len(self.objects) + 1}\n")
        chunks.append("0000000000 65535 f \n")
        chunks.extend(f"{offset:010d} 00000 n \n" for offset in offsets[1:])
        chunks.append(
            "trailer\n"
            f"<< /Size {len(self.objects) + 1} /Root {catalog_id} 0 R /Info {info_id} 0 R >>\n"
            f"startxref\n{xref_pos}\n%%EOF\n"
        )
        output.write_bytes("".join(chunks).encode("latin-1"))


def cover_page(pdf: PdfBuilder) -> list[str]:
    cmds: list[str] = [
        "0.05 0.23 0.64 rg 0 0 595 842 re f",
        "0.12 0.37 0.85 rg 0 500 595 342 re f",
        "1 1 1 rg",
        "BT /F2 40 Tf 60 708 Td (ChatGPT PRO) Tj ET",
        "BT /F2 20 Tf 60 672 Td (Practical Subscriber Handbook) Tj ET",
        "0.86 0.93 1 rg 60 192 470 132 re f",
    ]
    y = 632
    y = pdf.draw_wrapped_text(
        cmds,
        "A blue-themed starter guide for beginners: mode differences, PRO advantages,"
        " and detailed usage tactics for daily work.",
        x=60,
        y=y,
        size=13,
        max_chars=72,
        line_gap=18,
    )
    pdf.draw_wrapped_text(
        cmds,
        "Blue Edition eBook Style",
        x=80,
        y=272,
        size=16,
        bold=True,
        max_chars=40,
    )
    pdf.draw_wrapped_text(
        cmds,
        "Tip: Use role + context + output format constraints in one prompt for best results.",
        x=80,
        y=240,
        size=11,
        max_chars=64,
        line_gap=14,
    )
    return cmds


def comparison_page(pdf: PdfBuilder) -> list[str]:
    cmds = [
        "1 1 1 rg 0 0 595 842 re f",
        "0.12 0.25 0.7 rg 0 790 595 52 re f",
        "1 1 1 rg BT /F2 18 Tf 40 808 Td (1. Standard Mode vs PRO Mode) Tj ET",
    ]

    y = 758
    bullets = [
        "Standard mode is sufficient for short Q&A, quick checks, and simple rewrites.",
        "PRO mode is stronger with long context, multi-step constraints, and final-form outputs.",
        "Beginner takeaway: PRO generally reduces the number of prompt-revision loops.",
    ]
    for bullet in bullets:
        y = pdf.draw_wrapped_text(cmds, f"- {bullet}", 40, y, size=12, max_chars=82, line_gap=16)
        y -= 6

    cmds.extend(
        [
            "0.12 0.25 0.7 rg 40 628 515 24 re f",
            "1 1 1 rg BT /F2 11 Tf 48 636 Td (Category) Tj ET",
            "1 1 1 rg BT /F2 11 Tf 220 636 Td (Standard) Tj ET",
            "1 1 1 rg BT /F2 11 Tf 390 636 Td (PRO) Tj ET",
        ]
    )

    rows = [
        ("Complex Prompt Reliability", "Moderate", "Higher under multi-constraint requests"),
        ("Long Task Handling", "Basic continuity", "Strong continuity and structure"),
        ("Draft Quality", "Rough to intermediate", "Near-final professional drafts"),
        ("Revision Count", "Often multiple rounds", "Usually fewer correction rounds"),
    ]
    row_y = 602
    for i, row in enumerate(rows):
        shade = "0.93 0.96 1" if i % 2 == 0 else "0.88 0.93 1"
        cmds.append(f"{shade} rg 40 {row_y} 515 22 re f")
        cmds.append(f"0 0 0 rg BT /F1 10 Tf 48 {row_y + 7} Td ({pdf.esc(row[0])}) Tj ET")
        cmds.append(f"BT /F1 10 Tf 220 {row_y + 7} Td ({pdf.esc(row[1])}) Tj ET")
        cmds.append(f"BT /F1 10 Tf 390 {row_y + 7} Td ({pdf.esc(row[2])}) Tj ET")
        row_y -= 26
    return cmds


def benefit_page(pdf: PdfBuilder) -> list[str]:
    cmds = [
        "1 1 1 rg 0 0 595 842 re f",
        "0.12 0.25 0.7 rg 0 790 595 52 re f",
        "1 1 1 rg BT /F2 18 Tf 40 808 Td (2. Why PRO mode improves workflow) Tj ET",
    ]

    y = 760
    items = [
        "Faster turnaround by combining planning, drafting, and editing in one prompt flow.",
        "Higher practical quality for proposals, reports, scripts, and learning materials.",
        "More dependable handling of tone, length, audience, and formatting constraints.",
        "Better scalability from personal study tasks to professional deliverables.",
    ]
    for item in items:
        cmds.append(f"0.93 0.96 1 rg 38 {y - 12} 520 30 re f")
        y = pdf.draw_wrapped_text(cmds, f"- {item}", 46, y, size=12, max_chars=78, line_gap=16)
        y -= 10

    flow_labels = ["1. Define Goal", "2. Add Context", "3. Generate", "4. Review"]
    x = 40
    for label in flow_labels:
        cmds.append(f"0.15 0.39 0.92 rg {x} 486 120 56 re f")
        cmds.append(f"1 1 1 rg BT /F2 11 Tf {x + 10} 516 Td ({pdf.esc(label)}) Tj ET")
        x += 135

    return cmds


def features_page(pdf: PdfBuilder) -> list[str]:
    cmds = [
        "1 1 1 rg 0 0 595 842 re f",
        "0.12 0.25 0.7 rg 0 790 595 52 re f",
        "1 1 1 rg BT /F2 18 Tf 40 808 Td (3. Other must-know functions) Tj ET",
    ]

    y = 752
    features = [
        "Custom Instructions: persist your role, tone, and output style defaults.",
        "File analysis workflow: extract actions from PDFs/docs and convert to plans.",
        "Iterative prompting: preserve content while improving structure and clarity.",
        "Quality-check pass: request typo fixes, logic checks, and repetition removal.",
        "Constraint-first prompts: set length, forbid fluff, and enforce output format.",
    ]
    for feature in features:
        y = pdf.draw_wrapped_text(cmds, f"* {feature}", 40, y, size=12, max_chars=82, line_gap=16)
        y -= 8

    cmds.extend(
        [
            "0.86 0.93 1 rg 36 112 525 88 re f",
            "0.12 0.23 0.64 rg BT /F2 14 Tf 48 172 Td (Conclusion) Tj ET",
        ]
    )
    pdf.draw_wrapped_text(
        cmds,
        "PRO is not only about better answers. It is a practical output-production system"
        " that helps beginners reach reliable results more quickly.",
        x=48,
        y=150,
        size=12,
        max_chars=80,
        line_gap=16,
    )
    return cmds


def main() -> None:
    pdf = PdfBuilder()
    pages = [
        cover_page(pdf),
        comparison_page(pdf),
        benefit_page(pdf),
        features_page(pdf),
    ]
    content_ids = [pdf.add_stream(commands) for commands in pages]
    pdf.build(content_ids)
    print(f"generated {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
