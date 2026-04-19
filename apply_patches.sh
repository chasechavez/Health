#!/bin/bash
# Chase 2026 Training App - Goal & Sprint Update Patch
# Usage: bash apply_patches.sh index.html
# Creates patched copy at index_patched.html

FILE="$1"
if [ -z "$FILE" ]; then echo "Usage: bash apply_patches.sh index.html"; exit 1; fi
if [ ! -f "$FILE" ]; then echo "File not found: $FILE"; exit 1; fi

OUT="${FILE%.html}_patched.html"
cp "$FILE" "$OUT"

echo "Patching $FILE → $OUT"

# 1. Remove Mile Time goal
sed -i '/"Mile Time", target: 315/d' "$OUT"

# 2. Trap Bar DL target 405→450
sed -i 's/target: 405, current: 405/target: 450, current: 405/g' "$OUT"

# 3. Bench Press target 255→275
sed -i 's/target: 255, current: 213/target: 275, current: 213/g' "$OUT"

# 4. 30yd Dash → 40yd Dash
sed -i 's/"30yd Dash", target: 4.0, current: 4.5/"40yd Dash", target: 5.0, current: 5.3/g' "$OUT"

# 5. 1RM Calculator goals
sed -i "s/'Bench Press':255,'Trap Bar Deadlift':405/'Bench Press':275,'Trap Bar Deadlift':450/g" "$OUT"

# 6. Max Out section
sed -i 's/Trap Bar DL:<\/span> <span className="text-gray-700">405 lbs/Trap Bar DL:<\/span> <span className="text-gray-700">450 lbs/g' "$OUT"
sed -i 's/Bench Press:<\/span> <span className="text-gray-700">255 lbs/Bench Press:<\/span> <span className="text-gray-700">275 lbs/g' "$OUT"
sed -i 's/30yd Dash:<\/span> <span className="text-gray-700">Sub-4.0 sec/40yd Dash:<\/span> <span className="text-gray-700">Sub-5.0 sec/g' "$OUT"
sed -i 's/Mile:<\/span> <span className="text-gray-700">Sub-5:15/Power Clean:<\/span> <span className="text-gray-700">225 lbs/g' "$OUT"

# 7. Mesocycle label  
sed -i 's/Peak VJ and 30yd dash/Peak VJ and 40yd dash/g' "$OUT"

# 8. Saturday session name + notes
sed -i 's/"Plyos + 30yd Training"/"Plyos + 40yd Training"/g' "$OUT"
sed -i 's/Sub-4.0 30yd Dash/Sub-5.0 40yd Dash/g' "$OUT"

# 9. Sprint exercise names (all 30yd → 40yd)
sed -i 's/30yd Sprint (standing start)/40yd Sprint (standing start)/g' "$OUT"
sed -i 's/30yd Sprint (3-point)/40yd Sprint (3-point)/g' "$OUT"
sed -i 's/30yd Sprint — MAX EFFORT/40yd Sprint — MAX EFFORT/g' "$OUT"
sed -i 's/30yd Sprint — PEAK EFFORT/40yd Sprint — PEAK EFFORT/g' "$OUT"
sed -i 's/30yd Sprint — COMPETITION PREP/40yd Sprint — COMPETITION PREP/g' "$OUT"
sed -i 's/30yd Sprint (standing)/40yd Sprint (standing)/g' "$OUT"
sed -i "s/Jump → 30yd Sprint/Jump → 40yd Sprint/g" "$OUT"
sed -i "s/Complex: Heavy Trap Bar → 30yd Sprint/Complex: Heavy Trap Bar → 40yd Sprint/g" "$OUT"
sed -i "s/Complex: Power Clean → 30yd Sprint/Complex: Power Clean → 40yd Sprint/g" "$OUT"
sed -i 's/Resisted 30yd + Free 30yd/Resisted 40yd + Free 40yd/g' "$OUT"
sed -i 's/🏆 30-YARD DASH TEST/🏆 40-YARD DASH TEST/g' "$OUT"
sed -i 's/"30yd Sprint"/"40yd Sprint"/g' "$OUT"

# 10. Sprint reps
sed -i 's/reps: "30yd"/reps: "40yd"/g' "$OUT"
sed -i 's/reps: "2+30yd"/reps: "2+40yd"/g' "$OUT"
sed -i 's/reps: "30yd x2"/reps: "40yd x2"/g' "$OUT"

# 11. Sprint notes
sed -i 's/goal sub-4.0/goal sub-5.0/g' "$OUT"
sed -i 's/target sub-4.0/target sub-5.0/g' "$OUT"
sed -i 's/Goal: Sub-4.0/Goal: Sub-5.0/g' "$OUT"
sed -i 's/sub-4.2 this week/sub-5.2 this week/g' "$OUT"
sed -i 's/30yd dash position/40yd dash position/g' "$OUT"
sed -i 's/CMJ then immediate 30yd/CMJ then immediate 40yd/g' "$OUT"
sed -i 's/sprint mechanics for 30yd dash goal/sprint mechanics for 40yd dash goal/g' "$OUT"

# 12. migrateGoals - add Mile Time filter
sed -i 's/filter(g => g.name !== "Half Marathon")/filter(g => g.name !== "Half Marathon" \&\& g.name !== "Mile Time")/g' "$OUT"

# 13. migrateGoals - add goal target updates after 5K check
# Insert new code after the closing brace of the has5K block
sed -i '/savedData.goals.unshift.*5K Race.*Sub-21:00.*Apr 30/,/return savedData;/{
  /return savedData;/i\
                    // Update goal targets and convert 30yd→40yd\
                    savedData.goals.forEach(g => {\
                        if (g.name === "Trap Bar DL") g.target = 450;\
                        if (g.name === "Bench Press") g.target = 275;\
                        if (g.name === "30yd Dash") { g.name = "40yd Dash"; g.target = 5.0; g.current = 5.3; }\
                    });\
                    const has40 = savedData.goals.some(g => g.name === "40yd Dash");\
                    if (!has40) { savedData.goals.push({name: "40yd Dash", target: 5.0, current: 5.3, unit: "sec", icon: "SP", higherIsBetter: false}); }
}' "$OUT"

echo ""
echo "✅ All patches applied!"
echo "📁 Output: $OUT ($(wc -c < "$OUT") bytes)"
echo ""

# Verify
echo "── Verification ──"
grep -c "40yd" "$OUT" | xargs -I{} echo "  ✓ '40yd' references: {}"
grep -c "30yd" "$OUT" | xargs -I{} echo "  ⚠ '30yd' references remaining: {} (check these)"
grep -c "Mile Time" "$OUT" | xargs -I{} echo "  Mile Time references: {} (1 in filter is OK)"
grep -c "target: 450" "$OUT" | xargs -I{} echo "  ✓ Trap Bar 450 target found"
grep -c "target: 275" "$OUT" | xargs -I{} echo "  ✓ Bench 275 target found"
echo ""
echo "🚀 Rename $OUT to index.html and upload to GitHub!"
