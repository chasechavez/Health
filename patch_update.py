#!/usr/bin/env python3
"""
Chase 2026 Training App — Goal & Sprint Update Patch
=====================================================
Run:    python3 patch_update.py index.html
Output: Overwrites index.html with all changes applied

CHANGES:
  - Remove Mile Time goal
  - Trap Bar DL target: 405 → 450
  - Bench Press target: 255 → 275
  - 30yd Dash → 40yd Dash (target 4.0 → 5.0, current 4.5 → 5.3)
  - All sprint exercises: 30yd → 40yd
  - Sprint target times: sub-4.0 → sub-5.0
  - 1RM calculator goals updated
  - Max Out section updated
  - migrateGoals updated to handle all new changes
  - Speed/Power Peaking mesocycle label updated
"""

import sys, os, re

def patch(c):
    changes = 0

    def r(old, new, desc, count=0):
        nonlocal c, changes
        if old in c:
            if count:
                c = c.replace(old, new, count)
            else:
                c = c.replace(old, new)
            changes += 1
            print(f"  ✓ {desc}")
        else:
            if new in c:
                print(f"  ⊘ Already applied: {desc}")
            else:
                print(f"  ✗ NOT FOUND: {desc}")

    print("═══ GOALS ═══")

    # Remove Mile Time goal line
    for variant in [
        '                        {name: "Mile Time", target: 315, current: 360, unit: "sec", icon: "M", higherIsBetter: false, targetText: "5:15"},\n',
        '{name: "Mile Time", target: 315, current: 360, unit: "sec", icon: "M", higherIsBetter: false, targetText: "5:15"},',
    ]:
        if variant in c:
            c = c.replace(variant, '')
            changes += 1
            print("  ✓ Removed Mile Time goal")
            break
    else:
        if '"Mile Time"' not in c or 'target: 315' not in c:
            print("  ⊘ Mile Time goal already removed or not present")
        else:
            # Regex fallback
            c = re.sub(r'\s*\{name:\s*"Mile Time"[^}]+\},?\n?', '\n', c)
            changes += 1
            print("  ✓ Removed Mile Time goal (regex)")

    r('{name: "Trap Bar DL", target: 405, current: 405,',
      '{name: "Trap Bar DL", target: 450, current: 405,',
      "Trap Bar DL target → 450")

    r('{name: "Bench Press", target: 255, current: 213,',
      '{name: "Bench Press", target: 275, current: 213,',
      "Bench Press target → 275")

    r('{name: "30yd Dash", target: 4.0, current: 4.5, unit: "sec", icon: "SP", higherIsBetter: false}',
      '{name: "40yd Dash", target: 5.0, current: 5.3, unit: "sec", icon: "SP", higherIsBetter: false}',
      "30yd Dash → 40yd Dash goal")

    print("\n═══ 1RM CALCULATOR ═══")
    r("'Bench Press':255,'Trap Bar Deadlift':405,",
      "'Bench Press':275,'Trap Bar Deadlift':450,",
      "1RM calc goal targets updated")

    print("\n═══ MAX OUT SECTION ═══")
    r('Trap Bar DL:</span> <span className="text-gray-700">405 lbs',
      'Trap Bar DL:</span> <span className="text-gray-700">450 lbs',
      "Max Out: Trap Bar 450")
    r('Bench Press:</span> <span className="text-gray-700">255 lbs',
      'Bench Press:</span> <span className="text-gray-700">275 lbs',
      "Max Out: Bench 275")
    r('30yd Dash:</span> <span className="text-gray-700">Sub-4.0 sec',
      '40yd Dash:</span> <span className="text-gray-700">Sub-5.0 sec',
      "Max Out: 40yd Dash Sub-5.0")

    print("\n═══ MESOCYCLE & SESSION LABELS ═══")
    r('focus: "Peak VJ and 30yd dash"',
      'focus: "Peak VJ and 40yd dash"',
      "Mesocycle label")
    r('"Plyos + 30yd Training"',
      '"Plyos + 40yd Training"',
      "Saturday session name")
    r('Sub-4.0 30yd Dash',
      'Sub-5.0 40yd Dash',
      "Saturday notes")

    print("\n═══ SPRINT EXERCISE NAMES ═══")
    sprint_names = [
        ('30yd Sprint (standing start)', '40yd Sprint (standing start)'),
        ('30yd Sprint (3-point)', '40yd Sprint (3-point)'),
        ('30yd Sprint — MAX EFFORT', '40yd Sprint — MAX EFFORT'),
        ('30yd Sprint — PEAK EFFORT', '40yd Sprint — PEAK EFFORT'),
        ('30yd Sprint — COMPETITION PREP', '40yd Sprint — COMPETITION PREP'),
        ('30yd Sprint (standing)', '40yd Sprint (standing)'),
        ('Jump → 30yd Sprint', 'Jump → 40yd Sprint'),
        ('Complex: Heavy Trap Bar → 30yd Sprint', 'Complex: Heavy Trap Bar → 40yd Sprint'),
        ('Complex: Power Clean → 30yd Sprint', 'Complex: Power Clean → 40yd Sprint'),
        ('Resisted 30yd + Free 30yd', 'Resisted 40yd + Free 40yd'),
        ('🏆 30-YARD DASH TEST', '🏆 40-YARD DASH TEST'),
    ]
    for old, new in sprint_names:
        r(old, new, f"{old[:35]}...")

    print("\n═══ SPRINT REPS & NOTES ═══")
    # Reps fields
    r('reps: "30yd"', 'reps: "40yd"', "Sprint reps 30yd → 40yd (all)")
    r('reps: "2+30yd"', 'reps: "2+40yd"', "Complex reps 2+30yd → 2+40yd")
    r('reps: "30yd x2"', 'reps: "40yd x2"', "Contrast reps 30yd x2 → 40yd x2")
    
    # Notes
    r('goal sub-4.0', 'goal sub-5.0', "Sprint notes: goal sub-4.0 → sub-5.0")
    r('target sub-4.0', 'target sub-5.0', "Sprint notes: target sub-4.0 → sub-5.0")
    r('Goal: Sub-4.0', 'Goal: Sub-5.0', "Sprint test: Goal Sub-4.0 → Sub-5.0")
    r('sub-4.2 this week', 'sub-5.2 this week', "Peaking note: sub-4.2 → sub-5.2")
    r('30yd dash position', '40yd dash position', "Sprint position note")
    r('CMJ then immediate 30yd', 'CMJ then immediate 40yd', "CMJ sprint transition note")

    # Catch any remaining generic "30yd Sprint" exercise names
    remaining = c.count('"30yd Sprint"')
    if remaining > 0:
        c = c.replace('"30yd Sprint"', '"40yd Sprint"')
        changes += 1
        print(f"  ✓ Fixed {remaining} remaining generic '30yd Sprint' references")

    print("\n═══ MIGRATE GOALS FUNCTION ═══")
    r('savedData.goals = savedData.goals.filter(g => g.name !== "Half Marathon");',
      'savedData.goals = savedData.goals.filter(g => g.name !== "Half Marathon" && g.name !== "Mile Time");',
      "migrateGoals: added Mile Time filter")

    # Add goal target updates after the 5K check
    old_block = '''if (!has5K) {
                        savedData.goals.unshift({name: "5K Race", target: 21, current: 23, unit: "min", icon: "5K", higherIsBetter: false, targetText: "Sub-21:00 (Apr 30)"});
                    }
                    return savedData;'''
    new_block = '''if (!has5K) {
                        savedData.goals.unshift({name: "5K Race", target: 21, current: 23, unit: "min", icon: "5K", higherIsBetter: false, targetText: "Sub-21:00 (Apr 30)"});
                    }
                    // Update goal targets and convert 30yd→40yd
                    savedData.goals.forEach(g => {
                        if (g.name === "Trap Bar DL") g.target = 450;
                        if (g.name === "Bench Press") g.target = 275;
                        if (g.name === "30yd Dash") { g.name = "40yd Dash"; g.target = 5.0; g.current = 5.3; }
                    });
                    const has40 = savedData.goals.some(g => g.name === "40yd Dash");
                    if (!has40) { savedData.goals.push({name: "40yd Dash", target: 5.0, current: 5.3, unit: "sec", icon: "SP", higherIsBetter: false}); }
                    return savedData;'''
    r(old_block, new_block, "migrateGoals: added goal target updates + 40yd conversion")

    return c, changes


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 patch_update.py <path-to-index.html>")
        print("  Applies all goal and sprint updates in-place.")
        sys.exit(1)

    path = sys.argv[1]
    if not os.path.exists(path):
        print(f"Error: {path} not found")
        sys.exit(1)

    with open(path, 'r', encoding='utf-8') as f:
        original = f.read()

    print(f"Read {len(original):,} bytes from {path}\n")

    patched, count = patch(original)

    # Write patched version
    with open(path, 'w', encoding='utf-8') as f:
        f.write(patched)

    print(f"\n{'='*50}")
    print(f"✅ Applied {count} patches to {path}")
    print(f"   File size: {len(patched):,} bytes")

    # Verification
    print(f"\n── Quick Verification ──")
    checks = {
        '"40yd Dash"': "40yd Dash goal present",
        'target: 450': "Trap Bar 450 target",
        'target: 275': "Bench 275 target",
        '40-YARD DASH TEST': "40yd test day",
        '40yd Sprint': "40yd sprint exercises",
        'sub-5.0': "Sub-5.0 target time",
    }
    all_good = True
    for text, desc in checks.items():
        found = text in patched
        print(f"  {'✓' if found else '✗'} {desc}")
        if not found: all_good = False

    # Check Mile Time is only in filter
    mt_count = patched.count('"Mile Time"')
    print(f"  {'✓' if mt_count <= 1 else '✗'} Mile Time references: {mt_count} (1 in filter is OK)")

    if all_good:
        print(f"\n🚀 Ready to deploy! Upload {path} to GitHub Pages.")
    else:
        print(f"\n⚠️  Some checks failed — review the output above.")
