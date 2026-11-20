import json
caption = "Why Is There a Hole in the Plane Window? ✈️\nGuess: which pane takes the push, inner, middle or outer? 👇\nFollow @whyloop.hq for a new machine every day\n#howitworks #aviation #airplane #engineering #planes"
first = """Answer: the outer pane ✈️

A cabin window is usually three acrylic panes with small air gaps between them: the inner "scratch" pane you can touch, a middle pane, and an outer pane.

At cruising altitude the cabin is pressurized, so the air inside pushes outward on the window. The tiny "breather" (or "bleed") hole in the middle pane lets cabin air into the gap between the middle and outer panes. That makes the pressure the same on both sides of the middle pane, so the cabin pressure acts only on the outer pane.

The middle pane is strong enough to hold the cabin pressure too, so it is the backup if the outer pane ever fails.

The hole also lets moisture out of the gap, which helps keep the window from fogging or frosting up between the panes.

(Simplified 3D model: the gaps and the hole are drawn much bigger than in a real window.)

Sources:
Slate, What's That Thing: Why are there holes in airplane windows? (GKN Aerospace: the bleed hole in the middle pane lets pressure equalize between the cabin and the air gap, so cabin pressure in flight is applied only to the outer pane): https://slate.com/human-interest/2015/05/whats-that-thing-why-are-there-holes-in-airplane-windows.html
ScienceAlert, Here's Why There's a Tiny Hole in Airplane Windows (three panes; the outer pane takes the cabin pressure, the middle pane is the backup; the hole also helps keep the panes from fogging up): https://www.sciencealert.com/here-s-why-there-s-a-tiny-hole-in-airplane-windows
AFAR, Why Is There a Tiny Hole in the Airplane Window? (three layers of stretched acrylic; the bleed hole equalizes pressure and helps prevent condensation or fog between the panes): https://www.afar.com/magazine/why-airplane-windows-have-tiny-holes"""
alt = ("3D animation of an airplane cabin window, with a voiceover. Under the question Why is there a hole in the window? a rounded cabin window in a beige wall panel shows a tiny dark hole near the bottom, circled in red, with soft rings pulsing around it. "
       "The camera turns to the side and the window is cut in half, showing three acrylic panes with gaps between them, the cabin on the left and the outside on the right; the panes are labeled inner, middle and outer one at a time. "
       "2, up high, cabin air pushes out: yellow arrows push from the cabin toward the window, and white air dots fill the cabin side. "
       "3, the hole lets cabin air in: close up, air dots stream through the tiny hole in the middle pane and fill the gap in front of the outer pane, tagged cabin air in the gap. "
       "4, same push on both sides: equal white arrows push on both faces of the middle pane; then only the outer pane takes it: big yellow arrows push only on the outer pane, tagged outer pane full load, and the middle pane is tagged backup. "
       "5, it also lets moisture out: blue droplets from the outer pane drift down and out through the hole. "
       "The camera turns back to the window, the payoff reads One tiny hole: outer pane does the work, a follow line appears and the video loops.")
on = ['INSIDE IT', 'WHY IS THERE A', 'HOLE IN THE WINDOW?', 'THREE PANES', 'CABIN', 'OUTSIDE', 'INNER', 'MIDDLE', 'OUTER', 'UP HIGH: CABIN AIR PUSHES OUT', 'THE HOLE LETS CABIN AIR IN', 'TINY HOLE',
      'CABIN AIR IN THE GAP', 'SAME PUSH ON BOTH SIDES', 'ONLY THE OUTER PANE TAKES IT', 'OUTER PANE: FULL LOAD', 'MIDDLE PANE: BACKUP', 'IT ALSO LETS MOISTURE OUT', 'MOISTURE OUT',
      'ONE TINY HOLE:', 'OUTER PANE DOES THE WORK', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p096', track='A', group='V', slot='2026-11-25T01:00 Europe/London', topicKey='plane window hole',
  outlier='scorecard rule: everyday thing people see + one "why is it there"; our own model, script, words and sound',
  topic="Airplane cabin window breather hole: the hole in the middle pane lets cabin air into the gap, so only the outer pane carries the cabin pressure and the middle pane is the backup; it also vents moisture so the window does not fog.",
  hook="WHY IS THERE A / HOLE IN THE WINDOW?", title="Why Is There a Hole in the Plane Window? ✈️",
  principle="The breather (bleed) hole in the middle pane equalizes the pressure between the cabin and the gap between the middle and outer panes, so the cabin pressure differential is applied only to the outer pane; the middle pane is a fail-safe, and the hole vents moisture to prevent fogging between the panes.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://slate.com/human-interest/2015/05/whats-that-thing-why-are-there-holes-in-airplane-windows.html', 'https://www.sciencealert.com/here-s-why-there-s-a-tiny-hole-in-airplane-windows', 'https://www.afar.com/magazine/why-airplane-windows-have-tiny-holes'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
import re
from spellchecker import SpellChecker
sp = SpellChecker(); txt = ' '.join([caption, first, alt] + on + vo)
words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z']+", re.sub(r'https?://\S+', ' ', txt)))
words = {w.strip("'") for w in words}; words = {w[:-2] if w.endswith("'s") else w for w in words}
print('spell flags:', sorted(sp.unknown(words)))
