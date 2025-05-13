from cairosvg import svg2png

with open("BuWiFi-white-logo.svg", "r", encoding="utf-8") as f:
    svg_string = f.read()

svg2png(bytestring=svg_string.encode("utf-8"), write_to="output.png")
