#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

import markdown

f = open('../TODO.md', encoding='utf-8')
md = f.read()
html = markdown.markdown(md)

print("""content-type: text/html\n
<!--#include virtual="/head.html" -->
<!--#include virtual="/header.html" -->
""")

print("""
<section>
<article>
<h1>À faire</h1>
""")

print(html)

print("""
</article>
</section>
<!--#include virtual="/footer.html" -->
""")
