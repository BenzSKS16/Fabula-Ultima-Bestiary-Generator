import streamlit as st
import json

# ==========================================
# FABULA ULTIMA - BESTIARY VOL. I DATA
# ==========================================

LEVELS = [5, 10, 20, 30, 40, 50, 60]

ELEMENTS = [
    {"name": "Physical", "icon": "⚔️", "key": "physical"},
    {"name": "Air", "icon": "🌪️", "key": "air"},
    {"name": "Bolt", "icon": "⚡", "key": "bolt"},
    {"name": "Dark", "icon": "🌑", "key": "dark"},
    {"name": "Earth", "icon": "🪨", "key": "earth"},
    {"name": "Fire", "icon": "🔥", "key": "fire"},
    {"name": "Ice", "icon": "❄️", "key": "ice"},
    {"name": "Light", "icon": "☀️", "key": "light"},
    {"name": "Poison", "icon": "☣️", "key": "poison"}
]

AFFINITY_OPTIONS = [
    "- Neutral",
    "💥 VU (Vulnerable)",
    "🛡️ RS (Resist)",
    "🚫 IM (Immune)",
    "💚 AB (Absorb)"
]

AFFINITY_CODES = {
    "- Neutral": "-",
    "💥 VU (Vulnerable)": "VU",
    "🛡️ RS (Resist)": "RS",
    "🚫 IM (Immune)": "IM",
    "💚 AB (Absorb)": "AB"
}

AFFINITY_BADGES = {
    "-": "➖ Neutral",
    "VU": "💥 Vulnerable (2x Damage)",
    "RS": "🛡️ Resist (0.5x Damage)",
    "IM": "🚫 Immune (0 Damage)",
    "AB": "💚 Absorb (Heals from Damage)"
}

SPECIES_DATA = {
    "Beast": {
        "description": "Natural fauna and predatory beasts. Fast and instinctual.",
        "default_affinities": {},
        "vulnerability_options": [],
        "resistance_options": ["Air", "Bolt", "Dark", "Earth", "Fire", "Ice", "Light", "Poison"],
        "status_immunities": [],
        "traits_summary": "Add 2 of: +10 HP, Learn spell (Lick Wounds/Shell/War Cry), +3 Opposed Checks, Flying, or extra Role Skill."
    },
    "Construct": {
        "description": "Artificial automatons and war golems.",
        "default_affinities": {"Earth": "🛡️ RS (Resist)", "Poison": "🚫 IM (Immune)"},
        "vulnerability_options": ["Air", "Bolt", "Fire", "Ice"],
        "status_immunities": ["Poisoned"],
        "traits_summary": "Resist Earth, Immune to Poison & Poisoned. Optional Vulnerability (Air/Bolt/Fire/Ice) grants +2 status immunities, +3 Opposed Checks, Flying, or extra Role Skill."
    },
    "Demon": {
        "description": "Fiends born from human vice and emotional turmoil.",
        "default_affinities": {},
        "resistance_options": ["Air", "Bolt", "Dark", "Earth", "Fire", "Ice", "Light", "Poison"],
        "status_immunities": [],
        "traits_summary": "Resist 2 elements. Options: Replace 1 Resist with Absorb, learn spell (Breath/Curse XL/Mind Theft/Weaken), Flying, or extra Role Skill."
    },
    "Elemental": {
        "description": "Embodiments of pure natural or supernatural forces.",
        "default_affinities": {"Poison": "🚫 IM (Immune)"},
        "element_immunity_options": ["Air", "Bolt", "Dark", "Earth", "Fire", "Ice", "Light"],
        "status_immunities": ["Poisoned"],
        "traits_summary": "Immune to Poison & 1 element of choice, Immune to Poisoned. Optional counter Vulnerability grants Absorption, spell, Flying, or extra Role Skill."
    },
    "Humanoid": {
        "description": "Sentient mortals, soldiers, cultists, and outlaws.",
        "default_affinities": {},
        "vulnerability_options": ["Dark", "Light", "Physical", "Poison"],
        "status_immunities": [],
        "traits_summary": "Vulnerable to Dark, Light, Physical, or Poison. Select 3: Resist 2 elements, learn spell, +3 training Opposed Checks, Flying, extra Role Skill."
    },
    "Monster": {
        "description": "Mythical chimeras, dragons, and strange creatures.",
        "default_affinities": {},
        "resistance_options": ["Air", "Bolt", "Dark", "Earth", "Fire", "Ice", "Light", "Poison"],
        "status_immunities": [],
        "traits_summary": "Select 2: +10 HP, Resist 2 elements, learn spell, Flying, extra Role Skill."
    },
    "Plant": {
        "description": "Sentient flora, bramble maidens, and toxic fungi.",
        "default_affinities": {},
        "vulnerability_options": ["Air", "Bolt", "Fire", "Ice"],
        "status_immunities": ["Dazed", "Enraged", "Shaken"],
        "traits_summary": "Vulnerable to Air/Bolt/Fire/Ice, Immune to Dazed/Enraged/Shaken. Options: +10 HP, Resist 2 elements, learn spell, Thorns (+5 physical counter), Flying, or extra Role Skill."
    },
    "Undead": {
        "description": "Restless corpses, ghosts, and skeletal warriors.",
        "default_affinities": {"Light": "💥 VU (Vulnerable)", "Dark": "🚫 IM (Immune)", "Poison": "🚫 IM (Immune)"},
        "vulnerability_options": ["Air", "Bolt", "Earth", "Fire", "Ice"],
        "status_immunities": ["Poisoned"],
        "traits_summary": "Vulnerable to Light, Immune to Dark/Poison/Poisoned, harmed by HP recovery. Optional extra Vulnerability grants Absorb Dark, spell, Flying, or extra Role Skill."
    }
}

ROLES_DATA = {
    "Brute": {
        "attributes": {"DEX": "d8", "INS": "d6", "MIG": "d10", "WLP": "d8"},
        "hp_table": {5: 70, 10: 80, 20: 100, 30: 120, 40: 150, 50: 180, 60: 200},
        "mp_table": {5: 45, 10: 50, 20: 60, 30: 70, 40: 80, 50: 90, 60: 110},
        "init": 7, "def": 0, "mdef": 0,
        "description": "Abundant HP, low defenses, heavy physical attacks. Threat based on raw numbers.",
        "skills": [
            {
                "id": "brute_status_immunity",
                "name": "Status Resilience",
                "tag": "Passive Rule",
                "detail": "Gain permanent immunity to two status effects chosen from: poisoned, shaken, slow."
            },
            {
                "id": "brute_mdef_attack",
                "name": "Mind-Piercing Blow",
                "tag": "Basic Attack Modifier",
                "detail": "Normal attack targets Magic Defense instead of Defense."
            },
            {
                "id": "brute_ranged_strong",
                "name": "Heavy Throw / Ranged Strike",
                "tag": "Strong Attack Modifier",
                "detail": "Strong attack becomes Ranged [DEX + MIG] and targets hit suffer dazed, shaken, slow, or weak."
            },
            {
                "id": "brute_collapse_clock",
                "name": "Collapse Clock",
                "tag": "Special Rule (Elite/Champion)",
                "detail": "When strong attack misses all targets, fill 1 section of a 6-section 'Collapse' Clock. When full, lose this skill and deal minor damage to ALL creatures on the scene."
            },
            {
                "id": "brute_spells",
                "name": "Brute Spells",
                "tag": "Spell Access (Elite/Champion)",
                "detail": "Learns 2 spells from: Area Status, Curse XL, Cursed Breath, Enrage, Lick Wounds, Life Theft, Poison, Reinforce."
            },
            {
                "id": "brute_crush",
                "name": "Crush",
                "tag": "Unique Action",
                "detail": "Action: All enveloped enemies lose 20 HP (30 HP if Lv 30+). Strong attack gains property: 'Creatures hit are enveloped until this NPC uses strong attack again or takes Vulnerable damage.'"
            },
            {
                "id": "brute_enhancing_guard",
                "name": "Enhancing Guard",
                "tag": "Special Rule",
                "detail": "After Guarding, the next turn's attack deals +5 extra damage and ignores Resistances."
            },
            {
                "id": "brute_sore_loser",
                "name": "Sore Loser",
                "tag": "Reaction Rule",
                "detail": "After failing an Opposed Check on an enemy's turn where the enemy filled/erased 2+ Clock sections, that enemy suffers dazed, shaken, slow, or weak."
            },
            {
                "id": "brute_steady_recovery",
                "name": "Steady Recovery",
                "tag": "Special Rule",
                "detail": "At the end of each turn, if afflicted by 3 or more status effects, heal from ALL status effects automatically."
            }
        ]
    },
    "Hunter": {
        "attributes": {"DEX": "d10", "INS": "d8", "MIG": "d8", "WLP": "d6"},
        "hp_table": {5: 50, 10: 60, 20: 80, 30: 100, 40: 120, 50: 140, 60: 160},
        "mp_table": {5: 35, 10: 40, 20: 60, 30: 70, 40: 80, 50: 90, 60: 100},
        "init": 9, "def": 0, "mdef": 0,
        "description": "Exceptional accuracy, high Defense, and lethal single-target strikes.",
        "skills": [
            {
                "id": "hunter_mdef_attack",
                "name": "Precision Piercing",
                "tag": "Basic Attack Modifier",
                "detail": "Normal attack targets Magic Defense instead of Defense."
            },
            {
                "id": "hunter_strong_multi",
                "name": "Overwhelming Multi-Strike",
                "tag": "Strong Attack Modifier",
                "detail": "Add a strong attack [DEX + INS] or [DEX + MIG] + 15 damage with Multi (2). After resolving, this NPC cannot perform actions or free attacks until the end of its next turn."
            },
            {
                "id": "hunter_spells",
                "name": "Hunter Spells",
                "tag": "Spell Access",
                "detail": "Learns 2 spells from: Breath, Cursed Breath, Lick Wounds, Life Theft, Mirror."
            },
            {
                "id": "hunter_ambush",
                "name": "Ambush",
                "tag": "Special Rule",
                "detail": "During Round 1 of conflict, treat DEX, INS, or WLP as 1 die size higher (up to d12)."
            },
            {
                "id": "hunter_elusive",
                "name": "Elusive",
                "tag": "Special Rule",
                "detail": "As long as suffering from NO status effects, all sources of damage deal 0 damage to this NPC."
            },
            {
                "id": "hunter_bait",
                "name": "Hunter's Bait",
                "tag": "Reaction Rule",
                "detail": "When an enemy hits/misses with an attack/spell and the Check result is an even number, perform a free normal attack against them (High Roll = 0 for damage)."
            },
            {
                "id": "hunter_opportunist",
                "name": "Opportunist",
                "tag": "Special Rule",
                "detail": "When performing an Opposed Check against a creature suffering from dazed and/or slow, matching dice trigger a Critical Success."
            },
            {
                "id": "hunter_target_lock",
                "name": "Target Lock",
                "tag": "Special Rule",
                "detail": "Guarding locks onto a random enemy. Next normal attack against locked target deals +10 extra damage and removes the lock."
            }
        ]
    },
    "Mage": {
        "attributes": {"DEX": "d8", "INS": "d8", "MIG": "d6", "WLP": "d10"},
        "hp_table": {5: 40, 10: 50, 20: 70, 30: 90, 40: 110, 50: 130, 60: 160},
        "mp_table": {5: 55, 10: 60, 20: 70, 30: 80, 40: 100, 50: 110, 60: 120},
        "init": 8, "def": 1, "mdef": 2,
        "description": "High Magic Defense and multi-target elemental magic. High devastation potential.",
        "skills": [
            {
                "id": "mage_status_immunities",
                "name": "Arcane Immunity",
                "tag": "Passive Rule",
                "detail": "Gain permanent immunity to two status effects from: dazed, enraged, poisoned, shaken."
            },
            {
                "id": "mage_elemental_resists",
                "name": "Elemental Shroud",
                "tag": "Passive Rule",
                "detail": "Add Resistance to two damage types other than physical."
            },
            {
                "id": "mage_mp_drain",
                "name": "Siphon Strike",
                "tag": "Basic Attack Modifier",
                "detail": "When normal attack hits 1+ targets, recover 10 MP (20 MP if level 30+)."
            },
            {
                "id": "mage_volatile",
                "name": "Volatile Touch",
                "tag": "Basic Attack Modifier",
                "detail": "When normal attack deals HP loss, targets become volatile. All damage to volatile creatures ignores Resistances until healed or end of scene."
            },
            {
                "id": "mage_advanced_spells",
                "name": "Advanced Sorcery",
                "tag": "Spell Access",
                "detail": "Learns 2 spells from: Devastation, Drain Spirit, Flare, Iceberg, Life Theft, Mind Theft, Omega, Thunderbolt (+10 MP if choosing 1 spell)."
            },
            {
                "id": "mage_element_drain",
                "name": "Element Drain",
                "tag": "Reaction Rule",
                "detail": "When suffering non-physical, non-poison elemental damage, recover MP equal to half damage suffered."
            },
            {
                "id": "mage_element_shift",
                "name": "Element Shift",
                "tag": "Special Rule",
                "detail": "Casting an elemental spell changes Absorption to that element and Vulnerability to counter element (Air<->Bolt, Fire<->Ice, Earth<->Air, Light<->Dark)."
            },
            {
                "id": "mage_magical_mastery",
                "name": "Magical Mastery",
                "tag": "Special Rule",
                "detail": "Succeeding on a magic-related Opposed Check to fill or erase Clocks fills/erases +1 additional section."
            }
        ]
    },
    "Saboteur": {
        "attributes": {"DEX": "d8", "INS": "d8", "MIG": "d8", "WLP": "d8"},
        "hp_table": {5: 50, 10: 60, 20: 80, 30: 100, 40: 120, 50: 140, 60: 160},
        "mp_table": {5: 45, 10: 50, 20: 70, 30: 80, 40: 90, 50: 100, 60: 110},
        "init": 8, "def": 2, "mdef": 1,
        "description": "Specializes in status ailments, MP drain, and locking down enemy strategies.",
        "skills": [
            {
                "id": "sab_multi_attack",
                "name": "Sweeping Debuff",
                "tag": "Basic Attack Modifier",
                "detail": "Normal attack gains Multi (2)."
            },
            {
                "id": "sab_mdef_attack",
                "name": "Mind Sabotage",
                "tag": "Basic Attack Modifier",
                "detail": "Normal attack targets Magic Defense instead of Defense."
            },
            {
                "id": "sab_strong_debuff",
                "name": "Lockdown Strike",
                "tag": "Strong Attack Modifier",
                "detail": "Add a strong attack [DEX + INS] that prevents target from recovering HP/MP, acting, seeing, or gaining Resistances/Immunities until end of next turn."
            },
            {
                "id": "sab_spells",
                "name": "Saboteur Magic",
                "tag": "Spell Access",
                "detail": "Learns 1 spell from: Area Status, Curse XL, Dispel, Drain Spirit, Poison, Rage, Stop, Weaken (+10 MP)."
            },
            {
                "id": "sab_cruel_hypnosis",
                "name": "Cruel Hypnosis",
                "tag": "Unique Action (Elite/Champion)",
                "detail": "Action (20 MP): Target an enemy suffering dazed, enraged, or shaken. They must immediately perform a free attack against a target of your choice."
            },
            {
                "id": "sab_secret_technique",
                "name": "Secret Technique",
                "tag": "Special Rule",
                "detail": "Perform a chosen basic attack or spell without anyone other than the target realizing what it was."
            },
            {
                "id": "sab_parting_gift",
                "name": "Parting Gift",
                "tag": "Reaction Rule (Soldier/Elite)",
                "detail": "Upon defeat or leaving scene, every enemy affected by a Weaken spell cast by this NPC loses minor HP."
            },
            {
                "id": "sab_shadow_of_doubt",
                "name": "Shadow of Doubt",
                "tag": "Special Rule",
                "detail": "Any Player Character suffering from 2 or more status effects cannot invoke Traits or Bonds."
            }
        ]
    },
    "Sentinel": {
        "attributes": {"DEX": "d8", "INS": "d8", "MIG": "d8", "WLP": "d8"},
        "hp_table": {5: 50, 10: 60, 20: 90, 30: 110, 40: 130, 50: 150, 60: 170},
        "mp_table": {5: 45, 10: 50, 20: 60, 30: 70, 40: 90, 50: 100, 60: 110},
        "init": 8, "def": 2, "mdef": 1,
        "description": "High Defense and Magic Defense, intercepts attacks, counters aggressors.",
        "skills": [
            {
                "id": "sent_resistances",
                "name": "Iron Wall",
                "tag": "Passive Rule",
                "detail": "Add Resistance to two damage types."
            },
            {
                "id": "sent_multi_attack",
                "name": "Guard Sweep",
                "tag": "Basic Attack Modifier (Elite/Champion)",
                "detail": "Normal attack gains Multi (2)."
            },
            {
                "id": "sent_bypass_resist",
                "name": "Shield-Breaker",
                "tag": "Basic Attack Modifier",
                "detail": "Damage dealt by normal attack ignores Resistances."
            },
            {
                "id": "sent_dispel_strike",
                "name": "Nullifying Counter",
                "tag": "Strong Attack Modifier",
                "detail": "Hitting an enemy suffering a status effect with strong attack ends all 'Scene' duration spells affecting them."
            },
            {
                "id": "sent_spells",
                "name": "Sentinel Spells",
                "tag": "Spell Access",
                "detail": "Learns 1 spell from: Breath, Lick Wounds, Shell, War Cry (+10 MP)."
            },
            {
                "id": "sent_barricade",
                "name": "Barricade",
                "tag": "Unique Action",
                "detail": "Action (10 MP): Self and all allies gain Resistance to 1-2 chosen damage types until end of scene or taking Vulnerable damage."
            },
            {
                "id": "sent_avenge",
                "name": "Avenge",
                "tag": "Reaction Rule (Elite/Champion)",
                "detail": "After an enemy hits self/ally with melee/ranged attack or offensive spell, perform a free strong attack against that enemy."
            },
            {
                "id": "sent_reassuring_aura",
                "name": "Reassuring Aura",
                "tag": "Special Rule",
                "detail": "Allies able to see/hear this NPC are immune to dazed, shaken, slow, and weak."
            },
            {
                "id": "sent_reduce_progress",
                "name": "Reduce Progress",
                "tag": "Special Rule",
                "detail": "When an enemy fills/erases 2+ sections of a Clock, if this NPC is not afflicted by status, they fill/erase 1 fewer section."
            }
        ]
    },
    "Support": {
        "attributes": {"DEX": "d8", "INS": "d8", "MIG": "d6", "WLP": "d10"},
        "hp_table": {5: 50, 10: 60, 20: 80, 30: 100, 40: 130, 50: 150, 60: 170},
        "mp_table": {5: 55, 10: 60, 20: 70, 30: 80, 40: 90, 50: 100, 60: 110},
        "init": 8, "def": 0, "mdef": 0,
        "description": "Amplifies ally threat, heals, buffs attributes, and manages tactical flow.",
        "skills": [
            {
                "id": "supp_multi_attack",
                "name": "Tactical Multi-Hit",
                "tag": "Basic Attack Modifier",
                "detail": "Normal attack gains Multi (2)."
            },
            {
                "id": "supp_mdef_attack",
                "name": "Mind Pulse",
                "tag": "Basic Attack Modifier",
                "detail": "Normal attack targets Magic Defense instead of Defense."
            },
            {
                "id": "supp_status_attack",
                "name": "Disruptive Strike",
                "tag": "Basic Attack Modifier",
                "detail": "Creatures hit by normal attack suffer dazed, shaken, slow, or weak."
            },
            {
                "id": "supp_mp_recovery",
                "name": "Energizing Attack",
                "tag": "Basic Attack Modifier",
                "detail": "When normal attack hits 1+ targets, recover 10 MP (20 MP if Lv 30+)."
            },
            {
                "id": "supp_advise_inspire",
                "name": "Advise & Inspire Dual Package",
                "tag": "Unique Actions (Champion Only)",
                "detail": "Gain both Advise (+3 check bonus, removes dazed/shaken) and Inspire (minor HP/MP heal, +1 attribute die size) actions, but gain 1 extra Vulnerability."
            },
            {
                "id": "supp_enhanced_advise",
                "name": "Master Advise",
                "tag": "Special Rule",
                "detail": "Advise Skill allows the chosen ally to recover from ALL status effects instead of just dazed/shaken."
            },
            {
                "id": "supp_strategic_command",
                "name": "Strategic Command",
                "tag": "Unique Action",
                "detail": "Action (10 MP): Chosen ally acts immediately after this turn and deals +10 extra damage on their first hit."
            },
            {
                "id": "supp_healing_aura",
                "name": "Healing Aura",
                "tag": "Special Rule",
                "detail": "At the end of each turn, every ally present on the scene recovers minor HP."
            },
            {
                "id": "supp_mp_battery",
                "name": "MP Battery",
                "tag": "Special Rule",
                "detail": "When an ally spends Mind Points, this support NPC can pay the MP cost in their place."
            },
            {
                "id": "supp_one_last_command",
                "name": "One Last Command",
                "tag": "Reaction Rule",
                "detail": "Upon defeat or leaving scene, immediately perform Advise, Inspire, or Strategic Command for free."
            }
        ]
    }
}

BOSS_SKILLS = [
    {"id": "boss_suffering", "name": "Aura of Suffering", "type": "Battlefield", "detail": "All creatures cannot recover from chosen status effect, lose pre-existing immunity to it, and cannot gain immunity."},
    {"id": "boss_life_death", "name": "Life and Death", "type": "Battlefield", "detail": "Odd rounds: All creatures deal +5 extra damage. Even rounds: All HP recovery sources heal +10 additional HP."},
    {"id": "boss_near_far", "name": "Near and Far", "type": "Battlefield", "detail": "Odd rounds: Cannot target creatures with melee attacks. Even rounds: Cannot target with ranged attacks."},
    {"id": "boss_zombification", "name": "Zombification", "type": "Battlefield", "detail": "When a non-boss recovers HP while weak/poisoned, they lose half as many HP instead."},
    {"id": "boss_autocounter", "name": "Auto-Counter", "type": "Control", "detail": "After taking damage from an enemy action, automatically make a free normal attack or spell against them."},
    {"id": "boss_crisis_status", "name": "Crisis Status", "type": "Control", "detail": "Upon entering Crisis for the first time, every enemy present suffers 1-2 chosen status effects."},
    {"id": "boss_mark_pain", "name": "Mark of Shared Pain", "type": "Control", "detail": "Attacks mark enemies. When boss takes damage, HP loss is split equally among boss and all marked enemies."},
    {"id": "boss_observe_punish", "name": "Observe and Punish", "type": "Control", "detail": "The last enemy that damages boss becomes observed. First turn each round, boss attacks observed enemy for +10 extra damage."},
    {"id": "boss_tyrant_decree", "name": "Tyrant's Decree", "type": "Control", "detail": "Forbids 1-3 action types each round. Enemies performing forbidden actions trigger immediate counterattacks."},
    {"id": "boss_catastrophe", "name": "Catastrophe Charger", "type": "Destructive", "detail": "Last turn of round: Drain 30 MP from soldier allies. At 100 Points, release massive elemental AOE damage."},
    {"id": "boss_corrosive", "name": "Corrosive Status", "type": "Destructive", "detail": "Last turn of round: Deal minor/heavy elemental damage to every enemy suffering from status effects."},
    {"id": "boss_doom", "name": "Doom", "type": "Destructive", "detail": "6-section Doom Clock. Last turn: fills 1 section (2 if in Crisis). When full, all enemies drop to 1 HP."},
    {"id": "boss_binary", "name": "Binary Elements", "type": "Elemental", "detail": "Alternate between element pairs (e.g. Fire/Ice). Become Immune to one and Vulnerable to the other each round."},
    {"id": "boss_stance", "name": "Elemental Stance", "type": "Elemental", "detail": "Switch between 2-5 elemental stances (Immune to X, Vulnerable to Y) on specific triggers (Guard, hit by weakness, end of round)."},
    {"id": "boss_call_reinforcements", "name": "Call Reinforcements", "type": "Summoner", "detail": "Action (1 Ultima Point): Summon up to 2 soldier-rank allies into the battle."},
    {"id": "boss_emergency_reinforce", "name": "Emergency Reinforcements", "type": "Summoner", "detail": "End of round: If in Crisis and < 2 soldier allies remain, 1 soldier ally joins the battle."},
    {"id": "boss_adaptive", "name": "Adaptive Affinities", "type": "Survival", "detail": "After taking elemental damage, gain Immunity/Absorption to that damage type until triggered again."},
    {"id": "boss_camouflage", "name": "Camouflage", "type": "Survival", "detail": "Invisible, immune to melee, or immune to spells/ranged during even rounds."},
    {"id": "boss_defensive_stance", "name": "Defensive Stance", "type": "Survival", "detail": "Odd rounds: Halve all attack damage. Even rounds: Halve all non-attack damage."},
    {"id": "boss_regeneration", "name": "Regeneration", "type": "Survival", "detail": "At the end of each round while in Crisis, recover Heavy HP and/or MP."}
]

NEGATIVE_SKILLS = [
    {"id": "neg_delay", "name": "Final Delay", "detail": "When reduced to 0 HP, erase 1 section of a Clock that would benefit allies when full."},
    {"id": "neg_detonation", "name": "Final Detonation", "detail": "When reduced to 0 HP, deal Heavy elemental damage to all remaining allies."},
    {"id": "neg_restore", "name": "Final Restore", "detail": "When reduced to 0 HP, each enemy present recovers Heavy HP or MP."},
    {"id": "neg_status", "name": "Final Status", "detail": "When reduced to 0 HP, each ally present suffers dazed, shaken, slow, or weak."},
    {"id": "neg_weakening", "name": "Final Weakening", "detail": "When reduced to 0 HP, the boss being accompanied gains Vulnerability to chosen element until end of round."},
    {"id": "neg_status_bind", "name": "Status Bind", "detail": "Assign dazed, shaken, slow, weak to Normal Attack, Strong Attack, Skill, and Spell actions. While afflicted, cannot perform that action."}
]

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

st.set_page_config(page_title="Fabula Ultima - Monster Creator", page_icon="👾", layout="wide")

st.title("👾 Fabula Ultima - Quick Assembly Monster Creator")
st.caption("Grounded in Fabula Ultima: Bestiary Vol. I (Chapter 2 Quick Assembly Rules)")

# Session state initialization for elemental affinities
for elem in ELEMENTS:
    key = f"aff_{elem['key']}"
    if key not in st.session_state:
        st.session_state[key] = "- Neutral"

# Tabs for workflow
tab_config, st_adjust, st_export = st.tabs(["1. Monster Profile & Skills", "2. Stat Adjustments & Tactics", "3. Export & Stat Block"])

with tab_config:
    st.subheader("Step 1: Core Monster Profile")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        monster_name = st.text_input("Monster Name", value="Juggernaut Prime")
        
        # Species selection
        monster_species = st.selectbox("Species", list(SPECIES_DATA.keys()), index=1)
        species_info = SPECIES_DATA[monster_species]
        st.info(f"**Species Summary:** {species_info['traits_summary']}")

        # Species element customization / quick apply
        st.write("##### 🧬 Species Element Customization")
        
        # Species specific elemental pickers
        species_vulnerability_selection = None
        species_immunity_selection = None
        species_resistance_selection = None
        
        if species_info["vulnerability_options"]:
            species_vulnerability_selection = st.selectbox(
                f"Choose {monster_species} Vulnerability Element:",
                ["None"] + species_info["vulnerability_options"],
                help=f"Specific vulnerability option for {monster_species} species rules."
            )
            
        if "element_immunity_options" in species_info:
            species_immunity_selection = st.selectbox(
                f"Choose {monster_species} Immunity Element:",
                ["None"] + species_info["element_immunity_options"],
                help=f"Specific immunity option for {monster_species} species rules."
            )

        if "resistance_options" in species_info:
            species_resistance_selection = st.multiselect(
                f"Choose {monster_species} Resistance Elements (Select up to 2):",
                species_info["resistance_options"],
                max_selections=2
            )

        if st.button("⚡ Apply Species Defaults to Visual Elemental Attributes"):
            # Reset
            for elem in ELEMENTS:
                st.session_state[f"aff_{elem['key']}"] = "- Neutral"
            # Default affinities
            for elem_name, aff_val in species_info["default_affinities"].items():
                k = elem_name.lower()
                st.session_state[f"aff_{k}"] = aff_val
            # Vulnerability selection
            if species_vulnerability_selection and species_vulnerability_selection != "None":
                st.session_state[f"aff_{species_vulnerability_selection.lower()}"] = "💥 VU (Vulnerable)"
            # Immunity selection
            if species_immunity_selection and species_immunity_selection != "None":
                st.session_state[f"aff_{species_immunity_selection.lower()}"] = "🚫 IM (Immune)"
            # Resistance selection
            if species_resistance_selection:
                for res_elem in species_resistance_selection:
                    st.session_state[f"aff_{res_elem.lower()}"] = "🛡️ RS (Resist)"
            st.success("Updated Elemental Attributes grid with species defaults!")

        monster_traits = st.text_input("Monster Traits (comma separated)", value="bulky, destructive, automated, watchful")

    with col2:
        monster_level = st.selectbox("Level", LEVELS, index=3) # Default Lv 30
        monster_rank = st.selectbox("Rank", ["Soldier", "Elite", "Champion 1", "Champion 2", "Champion 3", "Champion 4", "Champion 5", "Champion 6"], index=1)
        monster_role = st.selectbox("Role", list(ROLES_DATA.keys()), index=0)
        
        role_info = ROLES_DATA[monster_role]
        st.caption(f"**Role Description:** {role_info['description']}")

    with col3:
        thresholds = get_level_thresholds(monster_level)
        st.metric("Level Check Bonus", f"+{thresholds['check_bonus']}")
        st.metric("Level Extra Damage", f"+{thresholds['extra_dmg']}")
        st.write(f"**Damage Threshold Values:**\n* **Minor:** {thresholds['minor']} HP\n* **Heavy:** {thresholds['heavy']} HP\n* **Massive:** {thresholds['massive']} HP")

    st.markdown("---")
    st.subheader("🛡️ Visual Section: Monster Element Attributes (Affinities)")
    st.caption("Configure elemental attributes directly using visual status signs. (VU = Vulnerable 💥, RS = Resist 🛡️, IM = Immune 🚫, AB = Absorb 💚)")

    # Render Visual Elemental Attributes Grid
    elem_cols = st.columns(9)
    for idx, elem in enumerate(ELEMENTS):
        with elem_cols[idx]:
            st.markdown(f"#### {elem['icon']}\n**{elem['name']}**")
            st.session_state[f"aff_{elem['key']}"] = st.selectbox(
                label=f"Affinity for {elem['name']}",
                options=AFFINITY_OPTIONS,
                key=f"aff_select_{elem['key']}",
                index=AFFINITY_OPTIONS.index(st.session_state[f"aff_{elem['key']}"]),
                label_visibility="collapsed"
            )

    # Display active Visual Summary Badges
    st.markdown("##### Active Element Attributes Summary")
    summary_cols = st.columns(9)
    for idx, elem in enumerate(ELEMENTS):
        selected_code = AFFINITY_CODES[st.session_state[f"aff_{elem['key']}"]]
        with summary_cols[idx]:
            if selected_code == "VU":
                st.error(f"{elem['icon']} **VU**")
            elif selected_code == "RS":
                st.info(f"{elem['icon']} **RS**")
            elif selected_code == "IM":
                st.warning(f"{elem['icon']} **IM**")
            elif selected_code == "AB":
                st.success(f"{elem['icon']} **AB**")
            else:
                st.text(f"{elem['icon']} -")

    st.markdown("---")
    st.subheader("📚 Step 2: Skill Selection with Full Details (See Details Before Choosing)")
    st.caption("Review full skill mechanics, rules, and tags below before checking 'Include in Build'.")

    selected_role_skills = []
    selected_boss_skills = []
    selected_neg_skills = []

    col_sk1, col_sk2 = st.columns(2)

    with col_sk1:
        st.write(f"### Role Skills: {monster_role}")
        for skill in role_info["skills"]:
            with st.container(border=True):
                c_title, c_check = st.columns([3, 1])
                with c_title:
                    st.markdown(f"**{skill['name']}** `[{skill['tag']}]`")
                    st.write(skill["detail"])
                with c_check:
                    if st.checkbox("Include Skill", key=f"cb_role_{skill['id']}"):
                        selected_role_skills.append(skill)

        st.write("### Negative Skills")
        for skill in NEGATIVE_SKILLS:
            with st.container(border=True):
                c_title, c_check = st.columns([3, 1])
                with c_title:
                    st.markdown(f"**{skill['name']}**")
                    st.write(skill["detail"])
                with c_check:
                    if st.checkbox("Include Skill", key=f"cb_neg_{skill['id']}"):
                        selected_neg_skills.append(skill)

    with col_sk2:
        st.write("### Boss Skills (Champions Only)")
        is_champion = monster_rank.startswith("Champion")
        if not is_champion:
            st.info("💡 Boss Skills are available for Champion-rank monsters.")

        for skill in BOSS_SKILLS:
            with st.container(border=True):
                c_title, c_check = st.columns([3, 1])
                with c_title:
                    st.markdown(f"**{skill['name']}** `[{skill['type']}]`")
                    st.write(skill["detail"])
                with c_check:
                    if st.checkbox("Include Skill", key=f"cb_boss_{skill['id']}", disabled=not is_champion):
                        selected_boss_skills.append(skill)

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

with st_adjust:
    st.subheader("Step 3: Fine-Tune Stat Block Adjustments")
    st.caption("Review calculated stats, customize basic attacks, spells, and routine before generating the export!")

    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        final_hp = st.number_input("Max Hit Points (HP)", value=base_hp, step=5)
        final_mp = st.number_input("Max Mind Points (MP)", value=base_mp, step=5)
        final_crisis = final_hp // 2
        st.info(f"Crisis HP Threshold: **{final_crisis} HP**")

    with col_a2:
        final_init = st.number_input("Initiative", value=base_init, step=1)
        final_def = st.number_input("Defense Mod (+DEF)", value=base_def, step=1)
        final_mdef = st.number_input("Magic Defense Mod (+M.DEF)", value=base_mdef, step=1)

    st.markdown("---")
    st.write("### Custom Attacks, Spells & Action Routine")

    col_act1, col_act2 = st.columns(2)
    with col_act1:
        basic_attack_1 = st.text_area("Basic Attack 1", value=f"Missile Salvo (Ranged) | +{thresholds['check_bonus']} Bonus | [DEX + MIG] + {thresholds['extra_dmg'] + 5} Fire Damage. Multi (2).")
        basic_attack_2 = st.text_area("Basic Attack 2 / Strong Attack", value=f"Steel Sword Bash (Melee) | +{thresholds['check_bonus']} Bonus | [MIG + MIG] + {thresholds['extra_dmg'] + 10} Physical Damage.")
        
    with col_act2:
        spells_text = st.text_area("Spells / Special Actions", value="Enhancing Guard: After Guarding, next action attack deals +5 extra damage and ignores Resistances.\nSteady Recovery: End of turn, heal all status if afflicted by 3+.")
        action_routine = st.text_area("Tactics & Routine", value="Round 1: Missile Salvo -> Steel Bash\nRound 2: Guard -> Missile Salvo (Enhanced)")

with st_export:
    st.subheader("Step 4: Formatted Monster Stat Block & Export")

    # Build Affinity Strings from State
    vuln_list = [f"{e['icon']} {e['name']}" for e in ELEMENTS if AFFINITY_CODES[st.session_state[f"aff_{e['key']}"]] == "VU"]
    res_list = [f"{e['icon']} {e['name']}" for e in ELEMENTS if AFFINITY_CODES[st.session_state[f"aff_{e['key']}"]] == "RS"]
    imm_list = [f"{e['icon']} {e['name']}" for e in ELEMENTS if AFFINITY_CODES[st.session_state[f"aff_{e['key']}"]] == "IM"]
    abs_list = [f"{e['icon']} {e['name']}" for e in ELEMENTS if AFFINITY_CODES[st.session_state[f"aff_{e['key']}"]] == "AB"]

    aff_vuln_str = ", ".join(vuln_list) if vuln_list else "None"
    aff_res_str = ", ".join(res_list) if res_list else "None"
    aff_imm_str = ", ".join(imm_list) if imm_list else "None"
    aff_abs_str = ", ".join(abs_list) if abs_list else "None"

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

### **Elemental Affinities (Attributes)**
| ⚔️ Physical | 🌪️ Air | ⚡ Bolt | 🌑 Dark | 🪨 Earth | 🔥 Fire | ❄️ Ice | ☀️ Light | ☣️ Poison |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| {AFFINITY_CODES[st.session_state['aff_physical']]} | {AFFINITY_CODES[st.session_state['aff_air']]} | {AFFINITY_CODES[st.session_state['aff_bolt']]} | {AFFINITY_CODES[st.session_state['aff_dark']]} | {AFFINITY_CODES[st.session_state['aff_earth']]} | {AFFINITY_CODES[st.session_state['aff_fire']]} | {AFFINITY_CODES[st.session_state['aff_ice']]} | {AFFINITY_CODES[st.session_state['aff_light']]} | {AFFINITY_CODES[st.session_state['aff_poison']]} |

* **💥 Vulnerabilities (VU):** {aff_vuln_str}
* **🛡️ Resistances (RS):** {aff_res_str}
* **🚫 Immunities (IM):** {aff_imm_str}
* **💚 Absorptions (AB):** {aff_abs_str}

---
### **Basic Attacks & Spells**
* **Attack 1:** {basic_attack_1}
* **Attack 2:** {basic_attack_2}
* **Spells & Special Rules:**
{spells_text}

---
### **Selected Skills & Abilities**
"""
    if selected_role_skills:
        for r_skill in selected_role_skills:
            md_stat_block += f"* **Role Skill [{r_skill['name']}] (`{r_skill['tag']}`):** {r_skill['detail']}\n"
    else:
        md_stat_block += "* *No Role Skills selected.*\n"

    if selected_boss_skills:
        for b_skill in selected_boss_skills:
            md_stat_block += f"* **Boss Skill [{b_skill['name']}] (`{b_skill['type']}`):** {b_skill['detail']}\n"

    if selected_neg_skills:
        for n_skill in selected_neg_skills:
            md_stat_block += f"* **Negative Skill [{n_skill['name']}]:** {n_skill['detail']}\n"

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
            "elemental_affinities": {e['name']: AFFINITY_CODES[st.session_state[f"aff_{e['key']}"]] for e in ELEMENTS},
            "selected_role_skills": selected_role_skills,
            "selected_boss_skills": selected_boss_skills,
            "selected_negative_skills": selected_neg_skills,
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
