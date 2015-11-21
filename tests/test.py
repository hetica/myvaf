#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

import cairosvg

svg_code1 = """<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="5cm" height="4cm" version="1.1"
     xmlns="http://www.w3.org/2000/svg">
  <desc>Four separate rectangles
  </desc>
    <rect x="0.5cm" y="0.5cm" width="2cm" height="1cm"/>
    <rect x="0.5cm" y="2cm" width="1cm" height="1.5cm"/>
    <rect x="3cm" y="0.5cm" width="1.5cm" height="2cm"/>
    <rect x="3.5cm" y="3cm" width="1cm" height="0.5cm"/>

  <!-- Show outline of canvas using 'rect' element -->
  <rect x=".01cm" y=".01cm" width="4.98cm" height="3.98cm"
        fill="none" stroke="blue" stroke-width=".02cm" />

</svg>
"""

svg_code2 = """<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"
	"http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
	<svg width="620px" height="420px" xml:lang="fr"
	xmlns="http://www.w3.org/2000/svg"
	xmlns:xlink="http://www.w3.org/1999/xlink">

		<title>My VAF</title>
	<rect x="0" y="0" width="620" height="420" fill="white" opacity="0.7"/>
	<path d="M 150,10 L 10,10 L 10,410 L 610,410 L 610,10 L 250,10" style="fill:none; stroke:grey;"/>
	<text id="lisere1" x="160" y="15">sample3</text>
	<line x1="95" y1="330" x2="565" y2="330" stroke="grey"/>
	<line x1="100" y1="335" x2="100" y2="55" stroke="grey"/>
	<text x="90" y="335" style="text-anchor:end;">0 %</text>
	<line x1="95" y1="240.0" x2="565" y2="240.0" stroke="#B3B3B3"/>
	<text x="90" y="245.0" style="text-anchor:end; baseline-shift:5;">10 %</text>
	<line x1="95" y1="150.0" x2="565" y2="150.0" stroke="#B3B3B3"/>
	<text x="90" y="155.0" style="text-anchor:end; baseline-shift:5;">20 %</text>
	<line x1="95" y1="60.0" x2="565" y2="60.0" stroke="#B3B3B3"/>
	<text x="90" y="65.0" style="text-anchor:end; baseline-shift:5;">30 %</text>
	<line x1="157.5" y1="330" x2="157.5" y2="123.0" style=" stroke:grey; stroke-width:15 "/>
	<text x="157.5" y="350" style="text-anchor:middle">ATM</text>
	<g fill="grey"><text x="192.5" y="119.0" style="text-anchor:middle" >H111P</text></g>
	<line x1="272.5" y1="330" x2="272.5" y2="276.0" style=" stroke:grey; stroke-width:15 "/>
	<text x="272.5" y="350" style="text-anchor:middle">BIRC3</text>
	<g fill="grey"><text x="307.5" y="272.0" style="text-anchor:middle" >R22P</text></g>
	<line x1="387.5" y1="330" x2="387.5" y2="195.0" style=" stroke:grey; stroke-width:15 "/>
	<text x="387.5" y="350" style="text-anchor:middle">TP53</text>
	<g fill="grey"><text x="422.5" y="191.0" style="text-anchor:middle" >W40S</text></g>
	<line x1="502.5" y1="330" x2="502.5" y2="60.0" style=" stroke:grey; stroke-width:15 "/>
	<text x="502.5" y="350" style="text-anchor:middle">BRAF</text>
	<g fill="grey"><text x="537.5" y="56.0" style="text-anchor:middle" >Y999Z</text></g>
	</svg>
"""

svg_code3 = '<?xml version="1.0" encoding="utf-8"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd"><svg width="620px" height="420px" xml:lang="fr" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><title>My VAF</title><rect x="0" y="0" width="620" height="420" fill="white" opacity="0.7"/><path d="M 150,10 L 10,10 L 10,410 L 610,410 L 610,10 L 250,10" style="fill:none; stroke:grey;"/><text id="lisere1" x="160" y="15">sample3</text><line x1="95" y1="330" x2="565" y2="330" stroke="grey"/><line x1="100" y1="335" x2="100" y2="55" stroke="grey"/><text x="90" y="335" style="text-anchor:end;">0 %</text><line x1="95" y1="240.0" x2="565" y2="240.0" stroke="#B3B3B3"/><text x="90" y="245.0" style="text-anchor:end; baseline-shift:5;">10 %</text><line x1="95" y1="150.0" x2="565" y2="150.0" stroke="#B3B3B3"/><text x="90" y="155.0" style="text-anchor:end; baseline-shift:5;">20 %</text><line x1="95" y1="60.0" x2="565" y2="60.0" stroke="#B3B3B3"/><text x="90" y="65.0" style="text-anchor:end; baseline-shift:5;">30 %</text><line x1="157.5" y1="330" x2="157.5" y2="123.0" style=" stroke:grey; stroke-width:15 "/><text x="157.5" y="350" style="text-anchor:middle">ATM</text><g fill="grey"><text x="192.5" y="119.0" style="text-anchor:middle" >H111P</text></g><line x1="272.5" y1="330" x2="272.5" y2="276.0" style=" stroke:grey; stroke-width:15 "/><text x="272.5" y="350" style="text-anchor:middle">BIRC3</text><g fill="grey"><text x="307.5" y="272.0" style="text-anchor:middle" >R22P</text></g><line x1="387.5" y1="330" x2="387.5" y2="195.0" style=" stroke:grey; stroke-width:15 "/><text x="387.5" y="350" style="text-anchor:middle">TP53</text><g fill="grey"><text x="422.5" y="191.0" style="text-anchor:middle" >W40S</text></g><line x1="502.5" y1="330" x2="502.5" y2="60.0" style=" stroke:grey; stroke-width:15 "/><text x="502.5" y="350" style="text-anchor:middle">BRAF</text><g fill="grey"><text x="537.5" y="56.0" style="text-anchor:middle" >Y999Z</text></g></svg>'
svg_code4 = '<?xml version="1.0" encoding="utf-8"?> <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd"> <svg width="620px" height="420px" xml:lang="fr" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><title>My VAF</title><rect x="0" y="0" width="620" height="420" fill="white" opacity="0.7"/><path d="M 150,10 L 10,10 L 10,410 L 610,410 L 610,10 L 250,10" style="fill:none; stroke:grey;"/><text id="lisere1" x="160" y="15">sample3</text><line x1="95" y1="330" x2="565" y2="330" stroke="grey"/><line x1="100" y1="335" x2="100" y2="55" stroke="grey"/><text x="90" y="335" style="text-anchor:end;">0 %</text><line x1="95" y1="240.0" x2="565" y2="240.0" stroke="#B3B3B3"/><text x="90" y="245.0" style="text-anchor:end; baseline-shift:5;">10 %</text><line x1="95" y1="150.0" x2="565" y2="150.0" stroke="#B3B3B3"/><text x="90" y="155.0" style="text-anchor:end; baseline-shift:5;">20 %</text><line x1="95" y1="60.0" x2="565" y2="60.0" stroke="#B3B3B3"/><text x="90" y="65.0" style="text-anchor:end; baseline-shift:5;">30 %</text><line x1="157.5" y1="330" x2="157.5" y2="123.0" style=" stroke:grey; stroke-width:15 "/><text x="157.5" y="350" style="text-anchor:middle">ATM</text><g fill="grey"><text x="192.5" y="119.0" style="text-anchor:middle" >H111P</text></g><line x1="272.5" y1="330" x2="272.5" y2="276.0" style=" stroke:grey; stroke-width:15 "/><text x="272.5" y="350" style="text-anchor:middle">BIRC3</text><g fill="grey"><text x="307.5" y="272.0" style="text-anchor:middle" >R22P</text></g><line x1="387.5" y1="330" x2="387.5" y2="195.0" style=" stroke:grey; stroke-width:15 "/><text x="387.5" y="350" style="text-anchor:middle">TP53</text><g fill="grey"><text x="422.5" y="191.0" style="text-anchor:middle" >W40S</text></g><line x1="502.5" y1="330" x2="502.5" y2="60.0" style=" stroke:grey; stroke-width:15 "/><text x="502.5" y="350" style="text-anchor:middle">BRAF</text><g fill="grey"><text x="537.5" y="56.0" style="text-anchor:middle" >Y999Z</text></g></svg>'


def build_png(svg, png):
	fic = open(png,'wb')
	cairosvg.svg2png(bytestring=svg,write_to=fic)
	fic.close()

build_png(svg_code4, "glop.png")

# CAF 02 72 64 46 33
