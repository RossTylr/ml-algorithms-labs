"""shared.explanation — markdown blocks the gates look for. Thin on purpose: the words are the notebook's job."""
from __future__ import annotations

from IPython.display import Markdown, display


def three_registers(plain: str, developer: str, technical: str):
    display(Markdown(f"🗣️ **Plain**\n\n{plain}\n\n💻 **Developer**\n\n{developer}\n\n🔬 **Technical**\n\n{technical}"))


def rfi(results: str, findings: str, implications: str, considerations: str = ""):
    md = f"### 📊 Results\n\n{results}\n\n### 🔍 Findings\n\n{findings}\n\n### 💡 Implications\n\n{implications}"
    if considerations:
        md += f"\n\n### ⚠️ Considerations\n\n{considerations}"
    display(Markdown(md))


def clinical_reading(text: str):
    display(Markdown(f"### 🩺 Clinical Reading\n\n{text}"))


def complexity(algorithm: str, train: str, predict: str, space: str, note: str = ""):
    md = f"| | |\n|---|---|\n| **Algorithm** | {algorithm} |\n| **Train** | {train} |\n| **Predict** | {predict} |\n| **Space** | {space} |"
    if note:
        md += f"\n\n*{note}*"
    display(Markdown(md))
