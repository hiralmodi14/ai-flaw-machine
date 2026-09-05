# 🛡️ OWASP AI Flaw Machine

An interactive, educational security lab and CTF playground designed to demonstrate and practice attacking/defending modern **Agentic AI** and **Large Language Model (LLM)** vulnerabilities, aligned with the **OWASP Top 10 for LLMs**.

---

## 🎯 Features

- **OWASP LLM01 - Prompt Injection**: Direct & Indirect Prompt Injections, System Prompt Extraction.
- **OWASP LLM08 - Excessive Agency**: Insecure Tool & Function Calling, File Traversal.
- **OWASP LLM02 - Insecure Output Handling**: Agentic SQL Injection.
- **OWASP LLM06 - Sensitive Information Disclosure**: Indirect Data Exfiltration via Agent Email Tools.
- **OWASP LLM07 - System / MCP Flaws**: Model Context Protocol (MCP) Description Poisoning.
- **Universal Game Engine**: Modular REPL console and extensible architecture.
- **Red Team vs. Blue Team Modes**: Practice both exploiting flaws and writing defensive guardrails.

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/hiralmodi14/ai-flaw-machine.git
cd ai-flaw-machine
```

### 2. Run the Universal Console Engine
```bash
python engine.py
```

### 3. Console Commands
- `menu` : View available challenges and your score.
- `load <level_id>` : Load a specific challenge.
- `flag <captured_flag>` : Submit your flag for points.
- `hint` : Reveal tactical clues.
- `exit` : Quit the session.

---

## 📜 License
MIT License
