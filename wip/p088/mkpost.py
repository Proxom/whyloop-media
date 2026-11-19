import json
caption = "What Holds Your Trunk Open? 🚗\nGuess: what's inside that little strut? 👇\nFollow @whyloop.hq for a new machine every day\n#cars #howitworks #mechanism #engineering #carparts"
first = """Answer: squeezed nitrogen gas 🚗

The struts that hold up a hatchback or trunk lid are gas springs. Each one is a sealed tube filled with nitrogen at high pressure, plus a little oil.

Inside, a piston sits on the end of the rod. A small hole in the piston lets the gas reach both sides, so the pressure is the same everywhere.

But on the rod side, the rod takes up part of the piston's area. So the gas has more area to push on from the other side, and the extra push equals the pressure times the rod's cross-section. That's why the rod always wants to slide out, and why it holds the lid up.

The oil helps slow the rod down near the end of its stroke, so the lid doesn't bang open.

(Simplified 3D model; the tube is drawn much wider than real so you can see inside.)

Sources:
SUSPA, Gas springs FAQ (filled with nitrogen plus oil; the filling pressure acts on both piston surfaces, the rod side is reduced by the rod cross-section, so the force F = p x A acts in the extension direction): https://www.suspa.com/global/products/gas-struts/faq
Stabilus, Gas Springs Technical Information (a nozzle in the piston keeps the pressure the same on both sides; spring force = inside pressure x piston rod cross-section): https://www.betz.cz/stabilus/ke-stazeni/08_Technical_Information_EN.pdf
ACE Controls, Industrial Gas Springs (when opening a car tailgate, gas flows through the orifice in the piston and the oil zone damps the end of the stroke): https://www.acecontrols.com/media/acedownloads/ACE_Catalog_GasSprings_US_2012.pdf"""
alt = ("3D animation of a car's rear hatch and its gas strut, with a voiceover. Under the question What holds the trunk open? the hatch lid floats up and stays open on a thin black strut with a chrome rod. "
       "The strut is then shown cut open, standing up with the rod pointing down; the tube is drawn wider than real. "
       "1, nitrogen, squeezed hard: blue dots of gas fill the tube, labeled high pressure. "
       "2, a hole: gas on both sides: a small hole in the piston lets dots flow through, so gas fills the space above and below the piston. "
       "3, the rod takes up room: five arrows push down on the full top of the piston, but underneath only a ring beside the rod gets pushed, by four shorter arrows. "
       "4, the push out wins: a big arrow beside the rod points out of the tube. "
       "Back outside, the payoff reads Squeezed gas pushes the rod out, a hand pushes the lid shut, a follow line appears and the video loops.")
on = ['INSIDE IT', 'WHAT HOLDS', 'THE TRUNK OPEN?', 'GAS STRUT', 'NITROGEN, SQUEEZED HARD', 'NITROGEN GAS', 'HIGH PRESSURE', 'A HOLE: GAS ON BOTH SIDES', 'PISTON', 'TINY HOLE',
      'THE ROD TAKES UP ROOM', 'ROD', 'THE PUSH OUT WINS', 'PUSH OUT', 'SQUEEZED GAS', 'PUSHES THE ROD OUT', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p088', track='A', group='V', slot='', topicKey='gas strut',
  outlier='scorecard rule: everyday object you touch + one "what holds it" question; our own model, script, words and sound',
  topic="Trunk/hatch gas strut (gas spring): a sealed tube of high-pressure nitrogen; a hole in the piston equalizes the pressure on both sides; the rod covers part of one side, so the net force p x A(rod) always pushes the rod out and holds the lid up; oil damps the end of the stroke.",
  hook="WHAT HOLDS / THE TRUNK OPEN?", title="What Holds Your Trunk Open? 🚗",
  principle="In a gas spring the nitrogen filling pressure p acts on both faces of the piston (equalized by the piston orifice); the rod-side face is smaller by the rod cross-section A, so the net force F = p x A acts in the extension direction. Oil lubricates the seal and damps the end of the extension stroke.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://www.suspa.com/global/products/gas-struts/faq', 'https://www.betz.cz/stabilus/ke-stazeni/08_Technical_Information_EN.pdf', 'https://www.acecontrols.com/media/acedownloads/ACE_Catalog_GasSprings_US_2012.pdf'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
import re
from spellchecker import SpellChecker
sp = SpellChecker(); txt = ' '.join([caption, first, alt] + on + vo)
words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z']+", re.sub(r'https?://\S+', ' ', txt)))
words = {w.strip("'") for w in words}; words = {w[:-2] if w.endswith("'s") else w for w in words}
print('spell flags:', sorted(sp.unknown(words)))
