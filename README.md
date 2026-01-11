# Gemini Skills 

## Credits & Acknowledgements

This project is based on and inspired by the work of **[`rez0`](https://x.com/rez0__)**

- Original FFUF skill & helper logic  
 https://github.com/jthack/ffuf_claude_skill/tree/main/ffuf-skill

  - GitHub : https://github.com/jthack  
  - X (Twitter) : https://x.com/rez0__


### Follow for instructions to use `Gemini Agent Skill` https://github.com/ikajakam/Gemini_Skills/blob/main/FFUF/README.md

## This repository contains a multi-agent skill workflow built for Gemini CLI, designed to behave like an experienced bug bounty hunter, not a blind scanner.

It combines:
- JavaScript attack-surface discovery
- Endpoint enumeration
- Vulnerability verification

All agent skills share intelligence through a **per-target output memory file (`analysis.txt`)**.
Each target has its own isolated output directory and all agents operating on that target
read from and write to / append the same `analysis.txt`.


| Component      | Role                                                    |
| -------------- | ------------------------------------------------------- |
| `*_helper.py`  | Execute tools and collect raw data                      |
| `SKILL.md`     | Define agent behavior, constraints, and decision-making |
| `analysis.txt` | Shared intelligence between agents                      |

No agent “talks” directly to another.
Agents coordinate through shared artifacts.

#### Each agent:

- Reads `analysis.txt`
- Extracts context
- Decides how to act
- Updates / append `analysis.txt`

Python executes.
Gemini reasons.
Files are memory.

### Agent Chain
```shell
JSH → FFUF → NUCLEI
```

### Understanding Skills

### Read `SKILL.md` to understand how agent skill works and how instructions are interpreted.

This will help you:

- Understand how the agent selects and executes commands
- Craft more precise prompts for your own use cases
- Customise or extend behavior by updating `SKILL.md` to match your workflow
- Modifying `SKILL.md` allows you to tailor skill to your recon style and testing needs
