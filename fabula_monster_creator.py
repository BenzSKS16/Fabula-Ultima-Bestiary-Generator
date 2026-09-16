import streamlit as st
import json

# ==========================================
# FABULA ULTIMA - BESTIARY VOL. I DATA
# ==========================================

LEVELS = [5, 10, 20, 30, 40, 50, 60]

ROLES_DATA = {
    "Brute": {
        "attributes": {"DEX": "d8", "INS": "d6", "MIG": "d10", "WLP": "d8"},
        "hp_table": {5: 70, 10: 80, 20: 100, 30: 120, 40: 150, 50: 180, 60: 200},
        "mp_table": {5: 45, 10: 50, 20: 60, 30: 70, 40: 80, 50: 90, 60: 110},
        "init": 7, "def": 0, "mdef": 0,
        "description": "Abundant Hit Points, low defenses, and strong basic attacks. Simple but dangerous numbers.",
        "skills": {
            "Status Immunity": "Add immunity to two status effects from: poisoned, shaken, slow.",
            "Magic Defense Attack": "Normal attack targets Magic Defense instead of Defense.",
            "Ranged Strong Attack": "Strong attack becomes ranged [DEX+MIG] and inflicts chosen status effect (dazed, shaken, slow, or weak).",
            "Collapse Clock": "When strong attack misses, fill 1 section of a 6-section Clock named 'Collapse'. When full, deals minor damage to everyone. (Elite/Champion only)",
            "Brute Spells": "Learns 2 spells from: Area Status, Curse XL, Cursed Breath, Enrage, Lick Wounds, Life Theft, Poison, Reinforce. (Elite/Champion only)",
            "Crush (Unique Action)": "Use an action so enveloped enemies lose 20 HP (30 if level 30+). Strong attack gains envelop property.",
            "Enhancing Guard": "After Guarding, next action attack deals +5 extra damage and ignores Resistances.",
            "Sore Loser": "After failing an Opposed Check on enemy turn where enemy filled/erased 2+ sections of a Clock, enemy suffers dazed/shaken/slow/weak.",
            "Steady Recovery": "At end of turn, if suffering from 3 or more status effects, heal from all status effects."
        }
    },
    "Hunter": {
        "attributes": {"DEX": "d10", "INS": "d8", "MIG": "d8", "WLP": "d6"},
        "hp_table": {5: 50, 10: 60, 20: 80, 30: 100, 40: 120, 50: 140, 60: 160},
        "mp_table": {5: 35, 10: 40, 20: 60, 30: 70, 40: 80, 50: 90, 60: 100},
        "init": 9, "def": 0, "mdef": 0,
        "description": "High accuracy, high Defense, and accurate single-target damage.",
        "skills": {
            "Magic Defense Attack": "Normal attack targets Magic Defense instead of Defense.",
            "Strong Attack (Multi 2)": "Add strong attack [DEX+INS] or [DEX+MIG] dealing +15 damage with Multi (2), but cannot act on next turn.",
            "Hunter Spells": "Learns 2 spells from: Breath, Cursed Breath, Lick Wounds, Life Theft, Mirror.",
            "Ambush": "During round 1, treat Dexterity, Insight, or Willpower as 1 die size higher (max d12).",
            "Elusive": "As long as suffering from no status effects, all sources of damage deal 0 damage instead.",
            "Hunter's Bait": "When an enemy hits/misses with attack/spell and Check result is even, perform a free normal attack against them.",
            "Opportunist": "Opposed Check against dazed/slow target triggers critical success if dice match.",
            "Target Lock": "Guarding locks onto a target; next normal attack deals +10 damage to them."
        }
    },
    "Mage": {
        "attributes": {"DEX": "d8", "INS": "d8", "MIG": "d6", "WLP": "d10"},
        "hp_table": {5: 40, 10: 50, 20: 70, 30: 90, 40: 110, 50: 130, 60: 160},
        "mp_table": {5: 55, 10: 60, 20: 70, 30: 80, 40: 100, 50: 110, 60: 120},
        "init": 8, "def": 1, "mdef": 2,
        "description": "High Magic Defense, multi-target elemental spells, low HP.",
        "skills": {
            "Status Immunities": "Add immunity to two: dazed, enraged, poisoned, shaken.",
            "Elemental Resistances": "Add Resistance to two damage types other than physical.",
            "MP Drain Strike": "When normal attack hits, recover 10 MP (20 if level 30+).",
            "Volatile Touch": "Normal attack makes targets volatile; damage to volatile targets ignores Resistances.",
            "Advanced Spells": "Learns 2 spells from: Devastation, Drain Spirit, Flare, Iceberg, Life Theft, Mind Theft, Omega, Thunderbolt.",
            "Element Drain": "When taking elemental damage (not physical/poison), recover MP equal to half damage taken.",
            "Element Shift": "Casting elemental spell changes Absorption to that element and Vulnerability to counter element.",
            "Magical Mastery": "Succeeding on magic Opposed Check to fill/erase Clocks alters +1 extra section."
        }
    },
    "Saboteur": {
        "attributes": {"DEX": "d8", "INS": "d8", "MIG": "d8", "WLP": "d8"},
        "hp_table": {5: 50, 10: 60, 20: 80, 30: 100, 40: 120, 50: 140, 60: 160},
        "mp_table": {5: 45, 10: 50, 20: 70, 30: 80, 40: 90, 50: 100, 60: 110},
        "init": 8, "def": 2, "mdef": 1,
        "description": "Adept at inflicting status effects, draining MP, and imposing action denial.",
        "skills": {
            "Multi Normal Attack": "Normal attack gains multi (2).",
            "Magic Defense Strike": "Normal attack targets Magic Defense instead of Defense.",
            "Strong Debuff Attack": "Add strong attack that prevents HP/MP recovery, action types, or status gains.",
            "Saboteur Spells": "Learns 1 spell from: Area Status, Curse XL, Dispel, Drain Spirit, Poison, Rage, Stop, Weaken (+10 MP).",
            "Cruel Hypnosis": "Action (20 MP): Force an enemy with dazed/enraged/shaken to make a free attack against an ally. (Elite/Champion)",
            "Secret Technique": "Choose attack/spell; perform it without anyone realizing what it was.",
            "Parting Gift": "Upon defeat, enemies under Weaken spell lose minor HP. (Soldier/Elite)",
            "Shadow of Doubt": "Players with 2+ status effects cannot invoke Traits and Bonds."
        }
    },
    "Sentinel": {
        "attributes": {"DEX": "d8", "INS": "d8", "MIG": "d8", "WLP": "d8"},
        "hp_table": {5: 50, 10: 60, 20: 90, 30: 110, 40: 130, 50: 150, 60: 170},
        "mp_table": {5: 45, 10: 50, 20: 60, 30: 70, 40: 90, 50: 100, 60: 110},
        "init": 8, "def": 2, "mdef": 1,
        "description": "High Defense and Magic Defense, protects allies and counters aggressors.",
        "skills": {
            "Defensive Resistances": "Add Resistance to two damage types.",
            "Multi Normal Attack": "Normal attack gains multi (2). (Elite/Champion)",
            "Bypass Resistances": "Damage dealt by normal attack ignores Resistances.",
            "Dispel Strike": "Hitting enemy suffering status effect with strong attack ends 'Scene' duration spells.",
            "Sentinel Spells": "Learns 1 spell from: Breath, Lick Wounds, Shell, War Cry (+10 MP).",
            "Barricade": "Action (10 MP): Self and allies gain Resistance to chosen damage types.",
            "Avenge": "Free attack with strong attack after enemy hits self or ally with attack/spell. (Elite/Champion)",
            "Reassuring Aura": "Allies able to see/hear sentinel are immune to dazed/shaken/slow/weak.",
            "Reduce Progress": "Enemies fill/erase 1 fewer section of Clocks."
        }
    },
    "Support": {
        "attributes": {"DEX": "d8", "INS": "d8", "MIG": "d6", "WLP": "d10"},
        "hp_table": {5: 50, 10: 60, 20: 80, 30: 100, 40: 130, 50: 150, 60: 170},
        "mp_table": {5: 55, 10: 60, 20: 70, 30: 80, 40: 90, 50: 100, 60: 110},
        "init": 8, "def": 0, "mdef": 0,
        "description": "Bolsters allies with buffs, healing, attribute boosts, and clean status management.",
        "skills": {
            "Multi Normal Attack": "Normal attack gains multi (2).",
            "Magic Defense Attack": "Normal attack targets Magic Defense instead of Defense.",
            "Status Inflicting Strike": "Creatures hit by normal attack suffer dazed, shaken, slow, or weak.",
            "MP Recovery Strike": "Normal attack recovers 10 MP (20 if level 30+).",
            "Advise & Inspire": "Gain both Advise and Inspire unique actions, but gain 1 extra Vulnerability. (Champion only)",
            "Enhanced Advise": "Advise Skill allows chosen ally to recover from ALL status effects.",
            "Healing Aura": "At end of turn, every ally present recovers minor HP.",
            "MP Battery": "When ally spends MP, support NPC can pay the cost instead.",
            "One Last Command": "Upon defeat, perform Advise, Inspire, or Strategic Command for free."
        }
    }
}

BOSS_SKILLS_DATA = {
    "Aura of Suffering (Battlefield)": "All creatures cannot recover from chosen status effect and lose immunity to it.",
    "Life and Death (Battlefield)": "Odd rounds: +5 extra damage for all. Even rounds: HP recovery sources heal +10 extra HP.",
    "Near and Far (Battlefield)": "Odd rounds: cannot target with melee. Even rounds: cannot target with ranged.",
    "Zombification (Battlefield)": "When a non-boss recovers HP while suffering weak/poisoned, they lose half as many HP instead.",
    "Auto-Counter (Control)": "After taking damage from an enemy action, automatically make a free normal attack/spell against them.",
    "Crisis Status (Control)": "Upon entering Crisis for the first time, all enemies suffer 1-2 chosen status effects.",
    "Mark of Shared Pain (Control)": "Attacks mark enemies. When boss takes damage, HP loss is split equally among boss and marked enemies.",
    "Observe and Punish (Control)": "The last enemy that damages boss becomes observed. First turn each round, boss attacks observed enemy for +10 damage.",
    "Tyrant's Decree (Control)": "Forbids 1-3 action types each round. Enemies performing forbidden actions trigger counterattacks.",
    "Catastrophe Charger (Destructive)": "Last turn of round: drain 30 MP from soldier allies. At 100 Points, release massive AOE damage.",
    "Corrosive Status (Destructive)": "Last turn of round: deal minor/heavy elemental damage to all enemies suffering status effects.",
    "Doom (Destructive)": "6-section Doom Clock. Last turn: fills 1 section (2 if in Crisis). When full, all enemies drop to 1 HP.",
    "Elemental Stance (Elemental)": "Switch between 2-5 elemental stances (Immune to X, Vulnerable to Y) on specific triggers.",
    "Binary Elements (Elemental)": "Alternate between element pairs (e.g., Fire/Ice) becoming Immune to one and Vulnerable to other each round.",
    "Call Reinforcements (Summoner)": "Action (1 Ultima Point): Summon up to 2 soldier-rank allies.",
    "Emergency Reinforcements (Summoner)": "End of round: if in Crisis and <2 soldiers remain, 1 soldier joins.",
    "Adaptive Affinities (Survival)": "After taking elemental damage, gain Immunity/Absorption to that damage type.",
    "Camouflage (Survival)": "Invisible, immune to melee, or immune to spells/ranged during even rounds.",
    "Defensive Stance (Survival)": "Odd rounds: halve attack damage. Even rounds: halve non-attack damage.",
    "Regeneration (Survival)": "End of round while in Crisis: recover Heavy HP/MP."
}

NEGATIVE_SKILLS_DATA = {
    "Final Delay": "When reduced to 0 HP, erase 1 section of an ally-beneficial Clock.",
    "Final Detonation": "When reduced to 0 HP, deal Heavy damage to all remaining allies.",
    "Final Restore": "When reduced to 0 HP, all enemies recover Heavy HP/MP.",
    "Final Status": "When reduced to 0 HP, all allies suffer dazed/shaken/slow/weak.",
    "Final Weakening": "When reduced to 0 HP, boss gains Vulnerability to chosen element until end of round.",
    "Status Bind": "Assign status effects to Normal/Strong attacks and Skill/Spell actions. While afflicted, cannot perform that action."
}

SPECIES_DATA = {
    "Beast": "Options: +10 HP, learn spell (Lick Wounds/Shell/War Cry), +3 to physical/instinct Opposed Checks, Flying, or extra Role Skill.",
    "Construct": "Resist earth, Immune to poison/poisoned. Optional: add extra Vulnerability (Air/Bolt/Fire/Ice) for 2 status immunities, +3 Opposed Checks, Flying, or extra Role Skill.",
    "Demon": "Resist two damage types. Options: Replace 1 Resist with Absorb, learn spell (Breath/Curse XL/Mind Theft/Weaken), Flying, or extra Role Skill.",
    "Elemental": "Immune to poison/poisoned + 1 element. Optional: add counter Vulnerability for Absorption, spell, Flying, or extra Role Skill.",
    "Humanoid": "Vulnerable to Dark/Light/Physical/Poison. Select 3: Resist 2 elements, learn spell, +3 training Opposed Checks, Flying, extra Role Skill.",
    "Monster": "Select 2: +10 HP, Resist 2 elements, learn spell, Flying, extra Role Skill.",
    "Plant": "Vulnerable to Air/Bolt/Fire/Ice, Immune to dazed/enraged/shaken. Option: +10 HP, Resist 2 elements, learn spell, Thorns rule, Flying, or extra Role Skill.",
    "Undead": "Vulnerable to Light, Immune to Dark/Poison/poisoned, harmed by HP recovery. Optional Vulnerability grants Absorb Dark, spell, Flying, or extra Role Skill."
}

# Helper for Level Threshold Values
def get_level_thresholds(level):
    if level < 20:
        return {"minor": 10, "heavy": 30, "massive": 40, "check_bonus": 0 if level == 5 else 1, "extra_dmg": 0}
    elif level < 40:
        return {"minor": 20, "heavy": 40, "massive": 60, "check_bonus": 2 if level == 20 else 3, "extra_dmg": 5}
    else:
        cb = 4 if level == 40 else (5 if level == 50 else 6)
        ed = 10 if level in [40, 50] else 15
        return {"minor": 30, "heavy": 50, "massive": 80, "check_bonus": cb, "extra_dmg": ed}

# ==========================================
# STREAMLIT UI APP
# ==========================================

st.set_page_config(page_title="Fabula Ultima Monster Creator", layout="wide")

st.title("👾 Fabula Ultima - Quick Assembly Monster Creator")
st.caption("Based on Fabula Ultima: Bestiary Vol. I (Chapter 2 Quick Assembly Rules)")

# Top Navigation Tabs
tab_config, st_adjust, st_export = st.tabs(["1. Monster Configuration", "2. Final Adjustments & Preview", "3. Export & Output"])

with tab_config:
    st.subheader("Step 1: Core Profile & Stats Selection")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        monster_name = st.text_input("Monster Name", value="Juggernaut Prime")
        monster_species = st.selectbox("Species", list(SPECIES_DATA.keys()), index=1)
        st.info(f"**Species Traits & Rules:**\n{SPECIES_DATA[monster_species]}")
        monster_traits = st.text_input("Traits (comma separated)", value="bulky, destructive, automated, watchful")

    with col2:
        monster_level = st.selectbox("Level", LEVELS, index=3) # Default Lv 30
        monster_rank = st.selectbox("Rank", ["Soldier", "Elite", "Champion 1", "Champion 2", "Champion 3", "Champion 4", "Champion 5", "Champion 6"], index=1)
        monster_role = st.selectbox("Role", list(ROLES_DATA.keys()), index=0)
        
        role_info = ROLES_DATA[monster_role]
        st.caption(f"**Role Focus:** {role_info['description']}")

    with col3:
        thresholds = get_level_thresholds(monster_level)
        st.metric("Level Check Bonus", f"+{thresholds['check_bonus']}")
        st.metric("Level Extra Damage", f"+{thresholds['extra_dmg']}")
        st.write(f"**Damage Scaling Values:** Minor: {thresholds['minor']} | Heavy: {thresholds['heavy']} | Massive: {thresholds['massive']}")

    st.markdown("---")
    st.subheader("Step 2: Skills & Abilities Selection")

    col_s1, col_s2 = st.columns(2)

    with col_s1:
        st.write("### Role Skills")
        selected_role_skills = st.multiselect(
            "Select Role Skills:", 
            list(role_info["skills"].keys()),
            help="Select role skills granted by Level & Rank."
        )
        for r_skill in selected_role_skills:
            st.success(f"**{r_skill}:** {role_info['skills'][r_skill]}")

        st.write("### Negative Skills (Optional)")
        selected_neg_skills = st.multiselect(
            "Select Negative Skills:",
            list(NEGATIVE_SKILLS_DATA.keys())
        )
        for n_skill in selected_neg_skills:
            st.warning(f"**{n_skill}:** {NEGATIVE_SKILLS_DATA[n_skill]}")

    with col_s2:
        st.write("### Boss Skills (Champions Only)")
        selected_boss_skills = st.multiselect(
            "Select Boss Skills:",
            list(BOSS_SKILLS_DATA.keys()),
            disabled=not monster_rank.startswith("Champion")
        )
        for b_skill in selected_boss_skills:
            st.error(f"**{b_skill}:** {BOSS_SKILLS_DATA[b_skill]}")

# Calculate Auto Base Stats
rank_hp_mult = 1
rank_mp_mult = 1
init_rank_bonus = 0

if monster_rank == "Elite":
    rank_hp_mult = 2
    init_rank_bonus = 2
elif monster_rank.startswith("Champion"):
    champ_num = int(monster_rank.split()[-1])
    rank_hp_mult = champ_num
    rank_mp_mult = 2
    init_rank_bonus = champ_num

base_hp = role_info["hp_table"][monster_level] * rank_hp_mult
base_mp = role_info["mp_table"][monster_level] * rank_mp_mult
base_init = role_info["init"] + init_rank_bonus
base_def = role_info["def"]
base_mdef = role_info["mdef"]

# Store state in session_state if not present
if "adj_hp" not in st.session_state:
    st.session_state.adj_hp = base_hp
    st.session_state.adj_mp = base_mp
    st.session_state.adj_init = base_init
    st.session_state.adj_def = base_def
    st.session_state.adj_mdef = base_mdef

with st_adjust:
    st.subheader("Step 3: Fine-Tune Stat Block Adjustments")
    st.caption("You can freely modify any calculated stats, add custom attacks, spells, or tactics before generating the final export!")

    col_a1, col_a2, col_a3 = st.columns(3)
    
    with col_a1:
        final_hp = st.number_input("Max Hit Points (HP)", value=base_hp, step=5)
        final_mp = st.number_input("Max Mind Points (MP)", value=base_mp, step=5)
        final_crisis = final_hp // 2
        st.info(f"Crisis HP Threshold: **{final_crisis} HP**")

    with col_a2:
        final_init = st.number_input("Initiative", value=base_init, step=1)
        final_def = st.number_input("Defense Mod (+DEF)", value=base_def, step=1)
        final_mdef = st.number_input("Magic Defense Mod (+M.DEF)", value=base_mdef, step=1)

    with col_a3:
        aff_vuln = st.text_input("Vulnerabilities (VU)", value="Bolt, Ice")
        aff_res = st.text_input("Resistances (RS)", value="Dark, Physical, Earth")
        aff_imm = st.text_input("Immunities (IM)", value="Poison, Air")
        aff_abs = st.text_input("Absorptions (AB)", value="None")

    st.markdown("---")
    st.write("### Custom Attacks, Spells & Action Routine")

    col_act1, col_a2 = st.columns(2)
    with col_act1:
        basic_attack_1 = st.text_area("Basic Attack 1", value=f"Missile Salvo (Ranged) | +{thresholds['check_bonus']} Bonus | [DEX + MIG] + {thresholds['extra_dmg'] + 5} Fire Damage. Multi (2).")
        basic_attack_2 = st.text_area("Basic Attack 2 / Strong Attack", value=f"Steel Sword Bash (Melee) | +{thresholds['check_bonus']} Bonus | [MIG + MIG] + {thresholds['extra_dmg'] + 10} Physical Damage.")
        
    with col_a2:
        spells_text = st.text_area("Spells / Special Actions", value="Enhancing Guard: After Guarding, next action attack deals +5 extra damage and ignores Resistances.\nSteady Recovery: End of turn, heal all status if afflicted by 3+.")
        action_routine = st.text_area("Tactics & Routine", value="Round 1: Missile Salvo -> Steel Bash\nRound 2: Guard -> Missile Salvo (Enhanced)")

with st_export:
    st.subheader("Step 4: Final Stat Block & Export Options")

    # Generate Markdown Stat Block
    md_stat_block = f"""# {monster_name}
**Level {monster_level} {monster_rank} {monster_role}**  
*Species:* {monster_species} | *Traits:* {monster_traits}

---
### **Attributes & Vital Stats**
* **DEX:** {role_info['attributes']['DEX']} | **INS:** {role_info['attributes']['INS']} | **MIG:** {role_info['attributes']['MIG']} | **WLP:** {role_info['attributes']['WLP']}
* **HP:** {final_hp} (Crisis: {final_crisis}) | **MP:** {final_mp}
* **Initiative:** {final_init} | **DEF:** +{final_def} | **M.DEF:** +{final_mdef}
* **Accuracy Check Bonus:** +{thresholds['check_bonus']} | **Extra Damage:** +{thresholds['extra_dmg']}

### **Affinities**
* **Vulnerabilities (VU):** {aff_vuln}
* **Resistances (RS):** {aff_res}
* **Immunities (IM):** {aff_imm}
* **Absorptions (AB):** {aff_abs}

---
### **Basic Attacks & Spells**
* **Attack 1:** {basic_attack_1}
* **Attack 2:** {basic_attack_2}
* **Spells & Special Rules:**
{spells_text}

---
### **Selected Skills & Effects**
"""
    for r_skill in selected_role_skills:
        md_stat_block += f"* **Role Skill [{r_skill}]:** {role_info['skills'][r_skill]}\n"
    for b_skill in selected_boss_skills:
        md_stat_block += f"* **Boss Skill [{b_skill}]:** {BOSS_SKILLS_DATA[b_skill]}\n"
    for n_skill in selected_neg_skills:
        md_stat_block += f"* **Negative Skill [{n_skill}]:** {NEGATIVE_SKILLS_DATA[n_skill]}\n"

    md_stat_block += f"""
---
### **Tactics & Routine**
{action_routine}
"""

    st.markdown("### 📄 Formatted Stat Block Preview")
    st.markdown(md_stat_block)

    st.markdown("---")
    st.subheader("💾 Export Options")

    col_exp1, col_exp2 = st.columns(2)

    with col_exp1:
        st.download_button(
            label="📥 Download Stat Block as Markdown (.md)",
            data=md_stat_block,
            file_name=f"{monster_name.lower().replace(' ', '_')}_statblock.md",
            mime="text/markdown"
        )

    with col_exp2:
        export_json = {
            "name": monster_name,
            "level": monster_level,
            "rank": monster_rank,
            "role": monster_role,
            "species": monster_species,
            "traits": monster_traits,
            "attributes": role_info['attributes'],
            "hp": final_hp,
            "crisis": final_crisis,
            "mp": final_mp,
            "initiative": final_init,
            "def_mod": final_def,
            "mdef_mod": final_mdef,
            "affinities": {
                "vulnerable": aff_vuln,
                "resistant": aff_res,
                "immune": aff_imm,
                "absorbed": aff_abs
            },
            "attacks": [basic_attack_1, basic_attack_2],
            "spells_special": spells_text,
            "routine": action_routine
        }
        st.download_button(
            label="📥 Download Configuration as JSON (.json)",
            data=json.dumps(export_json, indent=2),
            file_name=f"{monster_name.lower().replace(' ', '_')}_config.json",
            mime="application/json"
        )
