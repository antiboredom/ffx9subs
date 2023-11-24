from glob import glob
import re
import pysrt

files = sorted(glob("subs/*.srt"))

width = 1920
height = 1080
rows = 3
cols = 3
gheight = height / 3
gwidth = width / 3

coords = []
padding = 30

for y in range(rows):
    for x in range(cols):
        coords.append((int(x * gwidth), int(y * gheight + gheight - padding)))

dialog = []
for i, f in enumerate(files):
    try:
        subs = pysrt.open(f)
    except Exception as e:
        subs = pysrt.open(f, encoding="iso-8859-1")

    x = coords[i][0]
    y = coords[i][1]
    for s in subs:
        text = s.text.replace("\n", " ")
        text = re.sub(r"<.*?>", "", text)

        start = str(s.start).replace(",", ".")[0:-1]
        end = str(s.end).replace(",", ".")[0:-1]
        line = f"Dialogue: {start},{end},S1,{{\pos({x},{y})}}{text}"
        dialog.append(line)

dialog = "\n".join(dialog)

out = f"""
[Script Info]
PlayResX: {width}
PlayResY: {height}
WrapStyle: 1

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, BorderStyle, Outline, Shadow, ScaleX, ScaleY, Spacing, Angle, Alignment, Encoding
Style: S1, Arial,10,&H4BE4E6, &H000000, &H555555, 1, 1, 0, 100,  100,  0.00,  0.00, 7, 0

[Events]
Format: Start, End, Style, Text
{dialog}
"""

with open("ff9.ass", "w") as outfile:
    outfile.write(out)
