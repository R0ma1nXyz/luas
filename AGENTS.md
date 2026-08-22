# Antigravity Context: FFXI GearSwap Optimization

This rule file provides essential context for any AI agents interacting with the GearSwap Lua files in this workspace (`/home/romain/luas`). 

## 1. Modern FFXI BiS Standards
- **Ignore Ancient BiS:** The original Lua files may contain comments for outdated "Best-in-Slot" (BiS) items from the 2016-2018 era (e.g., `Abnoba Kaftan`, `Nibiru Cudgel`, `Vampirism`, `Sayadio's Kaftan`). Do not take these for granted.
- **Modern Gear Priority:** Always optimize for the modern 2024-2026 meta. The user already owns extremely powerful endgame gear, including **full Nyame (Path B)**, **full Malignance**, and **full Empyrean +3 sets** (e.g., `Hashishin +3`). Leverage these sets heavily when optimizing.

## 2. Set Context and Nuance
- **Job Abilities (JA) & Skill Sets:** **NEVER** blindly upgrade AF (Artifact) or Relic pieces to Empyrean pieces if they are inside a `sets.buff` or `sets.midcast` set dedicated to a specific JA or skill. 
    - *Example:* Do not replace `Assim. Shalwar +1` (Enhances Burst Affinity) with `Hashishin Tayt +3` in the Burst Affinity set.
    - If the user is missing the +3 version of an AF/Relic piece required for a JA, check if they own the +1 or +2 version and use that instead to preserve the specific enhancement modifier.
- **Weaponskills:** Pay attention to modifiers. Physical WSD scales massively with **Nyame (Path B)**. Crit WS (like Chant du Cygne) scales with **Gleti's** or **Adhemar +1**.
- **Magical Blue Magic:** Prioritize Blue Magic Skill, MACC, and MATK (e.g., **Hashishin +3**, **Amalric +1**).

## 3. Recording Missing BiS Gear
When the user is missing a modern BiS item, follow these steps exactly:
1. **Fallback:** Replace the missing item in the Lua table with the best contextually appropriate item the user *actually owns* (e.g., use the +1 version if they don't have +3, or use `Nyame` as a strong generic fallback).
2. **Inline Comments:** Append an inline comment to the end of the line recording the missing BiS item. 
    - *Format:* `-- BiS: <Original Item>`
    - *Example:* `body="Nyame Mail", -- BiS: Ashera Harness`
3. **TODO Lists:** Extract the missing BiS item and add it to the corresponding standalone checklist file in `GearSwap/data/Tenroh/TODO_BiS_<Job>.md`.

## 4. Upgrading Empyrean / AF / Relic
- If a Lua set calls for a +1 or +2 piece, always dynamically check the user's export file to see if they own the **+3 version**. If they do, upgrade it immediately.
