# Rubric — lovable-prompt

Domain: Code authoring / scaffolding (custom criteria)

## Criterion 1: Routing Quality (0–20)
Does the skill fire on relevant inputs and decline on out-of-scope ones?

| Score | Anchor |
|-------|--------|
| 18–20 | Description 250+ chars, 5+ user-typed trigger phrases (incl. Portuguese), WHAT+WHEN in first 250, "Do NOT use for" boundary with /pointers, third person |
| 12–17 | Description present but missing triggers or boundary pointer |
| 0–11  | No frontmatter, first person, or under 100 chars |

## Criterion 2: Output Specificity (0–20)
Does the output use real context from the user's discovery answers — not generic filler?

| Score | Anchor |
|-------|--------|
| 18–20 | Every section references specific discovery answers (named stack, named features, specific DO NOT rules from context) |
| 14–17 | Most sections specific; 1–2 generic placeholders remain (principled-decline path with correct gate) |
| 0–13  | Generic output — could apply to any app; training-data defaults presented as user-confirmed facts |

## Criterion 3: Output Format Consistency (0–20)
Would three different runs with the same input produce the same 7-section structure?

| Score | Anchor |
|-------|--------|
| 18–20 | All 7 sections present in the correct order every time; prompt in a code block; usage note in user's language |
| 12–17 | Sections present but order varies or one section missing |
| 0–11  | No consistent structure; free-form output |

## Criterion 4: Prompt Completeness (0–20) [Domain primary]
Are all required sections present with specific, actionable content?

| Score | Anchor |
|-------|--------|
| 18–20 | All 7 sections filled; Scope items are specific (not "user settings" — specifies which); Out of v1 has ≥1 exclusion; no [CONFIRM] markers unresolved |
| 14–17 | Correct decline path: asks all 6 discovery questions in one message, names exactly what's missing |
| 0–13  | Sections missing, scope items vague, or Out of v1 absent |

## Criterion 5: Scope Containment (0–20) [Domain secondary]
Do the DO NOT rules and Out of v1 section prevent Lovable from over-helping?

| Score | Anchor |
|-------|--------|
| 18–20 | ≥5 DO NOT rules present (5 universal + context-specific); Out of v1 lists explicit exclusions; design system written out even when "default" |
| 14–17 | Correct discovery gate: asks about exclusions and constraints before producing prompt |
| 0–13  | Fewer than 5 DO NOT rules; missing Out of v1; design system omitted |
