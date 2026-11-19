import json
caption = "One Lever: Hot or Cold? 🚰\nGuess: how many holes are in the bottom disc? 👇\nFollow @whyloop.hq for a new machine every day\n#howitworks #engineering #plumbing #mechanism #satisfying"
first = """Answer: three. A hot inlet, a cold inlet, and a way out 🚰

Inside a single-lever mixer tap sits a cartridge with two flat ceramic discs. The bottom disc is fixed. It has an inlet for hot water, an inlet for cold water, and an outlet. The top disc is moved by the lever, and its underside has a pocket.

Water can only get in where the pocket sits over part of an inlet. Under solid ceramic, the inlets are shut.

Lift the lever and the top disc slides, so the pocket opens more of the inlets: more water. Swing the lever and the disc turns, so the pocket sits over more of the hot inlet or more of the cold one (on this tap: left for hot, right for cold). The hot and cold water mix inside the pocket and leave through the outlet.

The two discs are polished so flat that they seal against each other without a rubber washer.

(Simplified 3D model; real cartridges differ in hole shapes and travel.)

Sources:
US Patent 8,109,292 B2 (fixed inlet disc with warm inlet, cold inlet and outlet; moving control disc above it; tilting the arm sets the amount, rotating it sets the temperature): https://patents.google.com/patent/US8109292B2
US Patent 9,115,819 B2 (control disc indentation: no inlet covered = closed; both inlets and the outlet covered = mixing inside the indentation): https://patents.google.com/patent/US9115819B2
Builders Squad, Ceramic disc technology in bathroom taps (fixed lower disc, moving upper disc, seal by flatness, no rubber washer): https://builderssquad.co.uk/blog/ceramic-disc-technology-in-bathrooms"""
alt = ("3D animation of a chrome single-lever mixer tap over a white basin on a stone counter, with a voiceover. Under the question One lever: hot or cold? the lever swings left and the water turns from blue to red. "
       "Then the view goes inside the tap to a cartridge with two flat white ceramic discs. 1, two flat ceramic discs: the top disc lifts off the bottom disc. "
       "2, the bottom disc never moves: it has a red hot slot, a blue cold slot and a curved way-out slot. "
       "3, water only under the pocket: the outlined top disc has a pocket underneath; it sits over no hole, the holes are shut by ceramic and the spout is off. "
       "4, lift: a small lever drawing tilts up while the top disc slides, the pocket reaches both holes and arrows show water going up into the pocket, across it and down the way out. "
       "5, swing: the lever goes left and the pocket turns onto the hot hole, the water turns red; then right onto the cold hole, the water turns blue. "
       "The payoff reads One moving pocket, two fixed holes, a follow line appears and the video loops.")
on = ['INSIDE IT', 'ONE LEVER:', 'HOT OR COLD?', 'HOT', 'COLD', 'TWO FLAT CERAMIC DISCS', 'TOP DISC', 'BOTTOM DISC', 'THE BOTTOM DISC NEVER MOVES', 'WAY OUT',
      'WATER ONLY UNDER THE POCKET', 'POCKET', 'HOLE SHUT BY CERAMIC', 'OFF', 'WATER', 'LIFT: MORE OVERLAP, MORE WATER', 'LIFT', 'DISC', 'SWING', 'LEFT = HOT', 'RIGHT = COLD', 'MIDDLE', 'SWING: MORE HOT OR MORE COLD',
      'MORE HOT', 'MORE COLD', 'ONE MOVING POCKET', 'TWO FIXED HOLES', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p084', track='A', group='E', slot='', topicKey='mixer tap cartridge',
  outlier='scorecard rule: everyday object you touch + one "why" question; our own model, script, words and sound',
  topic="Single-lever mixer tap ceramic disc cartridge: a fixed inlet disc (hot inlet, cold inlet, outlet) and a control disc with a pocket moved by the lever; lift slides it (flow), swing turns it (hot/cold share).",
  hook="ONE LEVER: / HOT OR COLD?", title="One Lever: Hot or Cold? 🚰",
  principle="Two flat ceramic discs seal against each other; the lever slides and turns the upper control disc over the fixed inlet disc, so the overlap of its pocket with the hot and cold inlets sets the flow (slide) and the hot/cold share (turn); the streams mix in the pocket and leave through the outlet.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://patents.google.com/patent/US8109292B2', 'https://patents.google.com/patent/US9115819B2', 'https://builderssquad.co.uk/blog/ceramic-disc-technology-in-bathrooms'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
import re
from spellchecker import SpellChecker
sp = SpellChecker(); txt = ' '.join([caption, first, alt] + on + vo)
words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z']+", re.sub(r'https?://\S+', ' ', txt)))
words = {w.strip("'") for w in words}; words = {w[:-2] if w.endswith("'s") else w for w in words}
print('spell flags:', sorted(sp.unknown(words)))
