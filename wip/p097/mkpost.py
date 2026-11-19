import json
caption = "How Does a Pepper Grinder Crush Pepper? 🧂\nGuess: what sets coarse or fine? 👇\nFollow @whyloop.hq for a new machine every day\n#howitworks #engineering #mechanism #kitchen #satisfying"
first = """Answer: the size of one tiny gap 🧂

At the bottom of a pepper mill there are two grinding parts: a grooved cone that turns with the shaft when you twist the top, and a grooved ring around it that stays still.

The gap between them is wide at the top and narrow at the bottom. A whole peppercorn drops into the wide part, and as the cone turns, the grooves crack it into smaller and smaller pieces on the way down. Only pieces smaller than the gap at the very bottom can fall out.

On mills with a top knob, the knob sits on the end of the shaft. Tighten it, and the cone is pulled further into the ring, so the burrs move closer together and the bottom gap gets smaller: finer pepper. Loosen it for a coarser, cracked grind. (Some mills use a dial at the bottom instead.)

(Simplified 3D model: the gap, the cone's movement and the pieces are enlarged so you can see them.)

Sources:
Wikipedia, Burr mill (food is ground between two revolving abrasive surfaces separated by a distance set by the user; closer = finer, farther = coarser): https://en.wikipedia.org/wiki/Burr_mill
US Patent 6,929,201, Adjustable spice grinder (an inner serrated cone inside an outer grinding member forms a tapered annular gap; turning the knob moves the shaft axially to adjust the gap and the coarseness): https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6929201
Peppermate, Adjusting your pepper mill grind (turning the top knob changes the space between the burrs; tighter = less space = finer grind, looser = coarser): https://www.peppermate.com/blogs/recipes/dialing-in-deliciousness-adjusting-your-pepper-mill-grind"""
alt = ("3D animation of a wooden pepper mill, with a voiceover. Under the question How does it crush pepper? a red circle marks the bottom of the mill while fine black pepper falls out of it. "
       "The top of the mill twists, then the mill is cut in half: inside, peppercorns sit in the chamber above a bright grooved steel cone that turns inside a dark grooved steel ring. "
       "1, a grooved cone turns in a ring: tags mark the cone (turns) and the ring (fixed). "
       "2, wide at the top, narrow at the bottom: yellow arrows measure a wide gap at the top and a narrow gap at the bottom. "
       "3, peppercorns crack smaller and smaller: dark pieces split apart as they move down the narrowing gap, tagged cracked. "
       "4, only tiny bits fit out: a gap arrow at the bottom, and tiny bits fall out. "
       "5, tighten the knob, smaller gap: the knob on top turns, the cone moves up into the ring, the bottom gap gets smaller, and two cards compare before, coarse pieces, with after, fine pepper. "
       "The payoff reads A narrowing gap crushes the pepper, a follow line appears and the video loops.")
on = ['INSIDE IT', 'HOW DOES IT', 'CRUSH PEPPER?', 'TWIST THE TOP', 'A GROOVED CONE TURNS IN A RING', 'CONE (TURNS)', 'RING (FIXED)', 'WIDE AT THE TOP, NARROW AT THE BOTTOM', 'WIDE GAP', 'NARROW GAP',
      'PEPPERCORNS CRACK SMALLER AND SMALLER', 'CRACKED', 'ONLY TINY BITS FIT OUT', 'GAP', 'TINY BITS FALL OUT', 'TIGHTEN THE KNOB: SMALLER GAP', 'TIGHTEN THE KNOB', 'CONE MOVES UP', 'SMALLER GAP',
      'BEFORE: COARSE', 'AFTER: FINE', 'A NARROWING GAP', 'CRUSHES THE PEPPER', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p097', track='A', group='E', slot='2026-11-25T01:00 Europe/London (planned, coordinator schedules)', topicKey='pepper grinder',
  outlier='scorecard rule: everyday object you touch + one "how does it" question; our own model, script, words and sound',
  topic="Pepper grinder: a grooved cone turns inside a grooved ring; the gap narrows downward, so peppercorns are cracked smaller and smaller until they fit through the bottom gap; tightening the top knob pulls the cone further in -> smaller gap -> finer.",
  hook="HOW DOES IT / CRUSH PEPPER?", title="How Does a Pepper Grinder Crush Pepper? 🧂",
  principle="A conical burr mill grinds between a rotating serrated inner cone and a fixed serrated outer ring separated by a tapered annular gap; particles are reduced until they pass the smallest gap at the outlet, and moving the cone axially (top knob on the shaft) sets that gap and so the grind size.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://en.wikipedia.org/wiki/Burr_mill', 'https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6929201', 'https://www.peppermate.com/blogs/recipes/dialing-in-deliciousness-adjusting-your-pepper-mill-grind'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
import re
from spellchecker import SpellChecker
sp = SpellChecker(); txt = ' '.join([caption, first, alt] + on + vo)
words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z']+", re.sub(r'https?://\S+', ' ', txt)))
words = {w.strip("'") for w in words}; words = {w[:-2] if w.endswith("'s") else w for w in words}
print('spell flags:', sorted(sp.unknown(words)))
