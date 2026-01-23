# Template assets for Hexcells parsing

Place PNG templates in this folder so the parser can classify cells and read clue digits.
Template images are intentionally not checked into git; drop your captures into the folders below.

## Required templates

### Cell states (`assets/templates/cells/`)
- `hidden.png`
- `revealed.png`
- `flagged.png`

### Digits (`assets/templates/digits/`)
- `0.png`
- `1.png`
- `2.png`
- `3.png`
- `4.png`
- `5.png`
- `6.png`

## How to capture templates
1. Capture a screenshot of the Hexcells board at the same resolution you will parse.
2. Crop a single hex cell for each state (hidden, revealed, flagged).
3. Crop each clue digit from a revealed cell (0-6) with minimal padding.
4. Save each crop as a grayscale PNG using the filenames listed above.
5. If you change resolution or UI scale, recapture templates and update `TemplateMatchingConfig.scale`.
