from glob import glob
import re
import pysrt

files = sorted(glob("subs/*.srt"))

offsets = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
]

width = 1920
height = 1080
rows = 3
cols = 3
gheight = height / 3
gwidth = width / 3
fontsize = 20
font = "Arial"
color = "4BE4E6"
outlinecolor = "000000"
outlinewidth = 1

coords = []
padding = 30

for y in range(rows):
    for x in range(cols):
        coords.append((int(x * gwidth), int(y * gheight + gheight - padding)))

styles = []
for i, c in enumerate(coords):
    margin_left = c[0]
    margin_right = width - c[0] - gwidth
    margin_bottom = height - c[1]
    style = f"Style: S{i}, {font}, {fontsize}, &H{color}, &H{outlinecolor}, &H555555, 1, {outlinewidth}, 0, 100,  100,  0.00,  0.00, 2, 0, {margin_left}, {margin_right}, {margin_bottom}"
    styles.append(style)

dialog = []
for i, f in enumerate(files):
    try:
        subs = pysrt.open(f)
    except Exception as e:
        subs = pysrt.open(f, encoding="iso-8859-1")

    subs.shift(seconds=offsets[i])

    for s in subs:
        text = s.text.replace("\n", " ")
        text = re.sub(r"<.*?>", "", text)

        start = str(s.start).replace(",", ".")[0:-1]
        end = str(s.end).replace(",", ".")[0:-1]
        line = f"Dialogue: {start},{end},S{i},{text}"
        dialog.append(line)

dialog = "\n".join(dialog)
styles = "\n".join(styles)

out = f"""
[Script Info]
PlayResX: {width}
PlayResY: {height}
WrapStyle: 1

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, BorderStyle, Outline, Shadow, ScaleX, ScaleY, Spacing, Angle, Alignment, Encoding, MarginL, MarginR, MarginV
{styles}

[Events]
Format: Start, End, Style, Text
{dialog}
"""

with open("F1F2F3F4F5F6F7F8F9.1080.x264.ass", "w") as outfile:
    outfile.write(out)
