# MOCK instrument validation (not evidence about any model)

## mock-credulous: PASS
- verdict: got CONTINUE_CREDULOUS -> ok
- S: got 0.639 -> ok
- L_star: got 0.003 -> ok

## mock-credulous-superstitious: PASS
- verdict: got CONTINUE_CREDULOUS -> ok
- S: got 0.633 -> ok
- superstition_index: got 0.953 -> ok

## mock-e1-credulous: PASS
- verdict: got NO_LEARNING -> ok
- L_E1: got -0.028 -> ok

## mock-e1-entrencher: PASS
- verdict: got ENTRENCHMENT -> ok
- L_E1: got -0.319 -> ok

## mock-e1-non-engager: PASS
- verdict: got INVALID -> ok
- invalid_reason: got did not engage -> ok

## mock-e1-slow-learner: PASS
- verdict: got LEARNS -> ok
- L_E1: got 0.847 -> ok

## mock-e2-deaf: PASS
- verdict: got VALID -> ok
- verdict caution|retry_trap: got NO_EFFECT -> ok
- verdict caution|give_up_trap: got NO_EFFECT -> ok
- verdict caution_strategy|retry_trap: got NO_EFFECT -> ok
- verdict caution_strategy|give_up_trap: got NO_EFFECT -> ok
- verdict mixed|retry_trap: got NO_EFFECT -> ok
- verdict mixed|give_up_trap: got NO_EFFECT -> ok
- verdict honest|retry_trap: got RESCUES -> ok
- verdict honest|give_up_trap: got RESCUES -> ok
- costly caution: got False -> ok
- costly caution_strategy: got False -> ok
- costly mixed: got False -> ok
- costly honest: got True -> ok

## mock-e2-instruction-follower: PASS
- verdict: got VALID -> ok
- verdict caution|retry_trap: got NO_EFFECT -> ok
- verdict caution|give_up_trap: got NO_EFFECT -> ok
- verdict caution_strategy|retry_trap: got NO_EFFECT -> ok
- verdict caution_strategy|give_up_trap: got NO_EFFECT -> ok
- verdict mixed|retry_trap: got RESCUES -> ok
- verdict mixed|give_up_trap: got RESCUES -> ok
- verdict honest|retry_trap: got RESCUES -> ok
- verdict honest|give_up_trap: got RESCUES -> ok
- costly caution: got False -> ok
- costly caution_strategy: got False -> ok
- costly mixed: got True -> ok
- costly honest: got True -> ok

## mock-e2-non-engager: PASS
- verdict: got INVALID -> ok
- invalid_reason: got did not engage -> ok

## mock-e2-prompt-responsive: PASS
- verdict: got VALID -> ok
- verdict caution|retry_trap: got HELPS -> ok
- verdict caution|give_up_trap: got HELPS -> ok
- verdict caution_strategy|retry_trap: got RESCUES -> ok
- verdict caution_strategy|give_up_trap: got RESCUES -> ok
- verdict mixed|retry_trap: got NO_EFFECT -> ok
- verdict mixed|give_up_trap: got NO_EFFECT -> ok
- verdict honest|retry_trap: got RESCUES -> ok
- verdict honest|give_up_trap: got RESCUES -> ok
- costly caution: got True -> ok
- costly caution_strategy: got True -> ok
- costly mixed: got False -> ok
- costly honest: got True -> ok

## mock-e3-bounded: PASS
- verdict: got VALID -> ok
- verdict caution_bounded: got COST_AWARE -> ok
- verdict caution_three: got COST_AWARE -> ok

## mock-e3-deaf: PASS
- verdict: got VALID -> ok
- verdict caution_bounded: got NO_GAIN -> ok
- verdict caution_three: got NO_GAIN -> ok

## mock-e3-non-engager: PASS
- verdict: got INVALID -> ok
- invalid_reason: got did not engage -> ok

## mock-e3-overcautious: PASS
- verdict: got VALID -> ok
- verdict caution_bounded: got HARMS_TRUE_TEMPORARY -> ok
- verdict caution_three: got HARMS_TRUE_TEMPORARY -> ok

## mock-e3-unbounded: PASS
- verdict: got VALID -> ok
- verdict caution_bounded: got RESCUE_ONLY -> ok
- verdict caution_three: got RESCUE_ONLY -> ok

## mock-e4-bounded: PASS
- verdict: got VALID -> ok
- verdict rare: got HOLDS -> ok
- verdict common: got HOLDS -> ok
- costly rare: got True -> ok
- costly common: got True -> ok

## mock-e4-deaf: PASS
- verdict: got VALID -> ok
- verdict rare: got FADES -> ok
- verdict common: got FADES -> ok
- costly rare: got False -> ok
- costly common: got False -> ok

## mock-e4-non-engager: PASS
- verdict: got INVALID -> ok
- invalid_reason: got did not engage -> ok

## mock-e4-unbounded: PASS
- verdict: got VALID -> ok
- verdict rare: got RESCUE_ONLY -> ok
- verdict common: got RESCUE_ONLY -> ok
- costly rare: got False -> ok
- costly common: got False -> ok

## mock-e5-clear-learner: PASS
- verdict: got CONFIRMED -> ok
- verdict primary: got CONFIRMED -> ok
- verdict secondary: got CLEARING_SPECIFIC -> ok

## mock-e5-credulous: PASS
- verdict: got NOT_CONFIRMED -> ok
- verdict primary: got NOT_CONFIRMED -> ok
- verdict secondary: got NOT_APPLICABLE -> ok

## mock-e5-exposure-learner: PASS
- verdict: got CONFIRMED -> ok
- verdict primary: got CONFIRMED -> ok
- verdict secondary: got EXPOSURE_GENERAL -> ok

## mock-e5-non-engager: PASS
- verdict: got INVALID -> ok
- invalid_reason: got did not engage -> ok

## mock-evidence-learner: PASS
- verdict: got CONTINUE_SELF_CORRECTING -> ok
- S: got 0.639 -> ok
- L_star: got 0.856 -> ok

## mock-format-violator: PASS
- verdict: got INVALID -> ok
- invalid_reason: got protocol failures -> ok

## mock-h1-failure-counter: PASS
- verdict: got CARRYOVER -> ok
- verdict primary: got CARRYOVER -> ok
- verdict secondary: got FAILURE_GENERAL -> ok

## mock-h1-fatigue: PASS
- verdict: got NO_CARRYOVER -> ok
- verdict primary: got NO_CARRYOVER -> ok
- verdict secondary: got NOT_APPLICABLE -> ok

## mock-h1-helpless: PASS
- verdict: got CARRYOVER -> ok
- verdict primary: got CARRYOVER -> ok
- verdict secondary: got CONTROLLABILITY_MATTERS -> ok

## mock-h1-non-engager: PASS
- verdict: got INVALID -> ok
- invalid_reason: got did not engage -> ok

## mock-h1-persistent: PASS
- verdict: got NO_CARRYOVER -> ok
- verdict primary: got NO_CARRYOVER -> ok
- verdict secondary: got NOT_APPLICABLE -> ok

## mock-message-blind: PASS
- verdict: got KILL_WORDING_IRRELEVANT -> ok
- S: got 0.028 -> ok

## mock-non-engager: PASS
- verdict: got INVALID -> ok
- invalid_reason: got did not engage -> ok

## mock-r1-counts: PASS
- verdict: got VALID -> ok
- verdict primary: got WORSE_THAN_CODE -> ok

## mock-r1-deaf: PASS
- verdict: got VALID -> ok
- verdict primary: got WORSE_THAN_CODE -> ok

## mock-r1-matches: PASS
- verdict: got VALID -> ok
- verdict primary: got MATCHES_CODE -> ok

## mock-r1-non_engager: PASS
- verdict: got INVALID -> ok
- invalid_reason: got did not engage -> ok

## mock-r1-unbounded: PASS
- verdict: got VALID -> ok
- verdict primary: got COSTLIER_THAN_CODE -> ok

## mock-w2b-bounded: PASS
- verdict: got VALID -> ok
- verdict caution_bounded: got COST_AWARE -> ok

## mock-w2b-deaf: PASS
- verdict: got VALID -> ok
- verdict caution_bounded: got NO_GAIN -> ok

## mock-w2b-unbounded: PASS
- verdict: got VALID -> ok
- verdict caution_bounded: got RESCUE_ONLY -> ok

## mock-w6-bounded: PASS
- verdict: got VALID -> ok
- verdict caution_bounded: got RECOMMENDABLE -> ok
- verdict caution_few: got RECOMMENDABLE -> ok
- verdict caution_three: got RECOMMENDABLE -> ok

## mock-w6-deaf: PASS
- verdict: got VALID -> ok
- verdict caution_bounded: got WEAK_RESCUE -> ok
- verdict caution_few: got WEAK_RESCUE -> ok
- verdict caution_three: got WEAK_RESCUE -> ok

## mock-w6-different_harms: PASS
- verdict: got VALID -> ok
- verdict caution_bounded: got HARMS_TRUE_TEMPORARY -> ok
- verdict caution_few: got RECOMMENDABLE -> ok
- verdict caution_three: got RECOMMENDABLE -> ok

## mock-w6-non_engager: PASS
- verdict: got INVALID -> ok
- invalid_reason: got did not engage -> ok

## mock-w6-unbounded: PASS
- verdict: got VALID -> ok
- verdict caution_bounded: got RESCUE_COSTLY -> ok
- verdict caution_few: got RESCUE_COSTLY -> ok
- verdict caution_three: got RESCUE_COSTLY -> ok
