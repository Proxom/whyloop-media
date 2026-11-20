import json
caption = "How Does It Pull the Soap Up? 🧴\nGuess: how many tiny balls are inside? 👇\nFollow @whyloop.hq for a new machine every day\n#howitworks #engineering #mechanism #satisfying #everydayscience"
first = """Answer: two balls, and each one is a one-way door 🧴

Under the head there is a small chamber full of soap, a piston, and a spring. A tube runs from the chamber to the bottom of the bottle.

Press down: the piston squeezes the soap in the chamber. That pressure pushes the bottom ball onto its seat (shut) and lifts the top ball (open), so the soap can only go up through the stem and out of the nozzle.

Let go: the spring pushes the piston back up. That sucks on the chamber, so the top ball drops shut and the bottom ball lifts off its seat. Because the top is shut, new soap can only come up the tube from the bottle, and the chamber is full again for the next press.

(Simplified 3D model, not to exact scale. Some pumps use the piston itself as the top valve instead of a second ball; the idea is the same: two one-way valves and a spring.)

Sources:
US Patent 11,267,009 B1, Manually operated dispensing pump (an inlet one-way valve, a pump chamber, a piston, a compression spring and an outlet one-way valve; both valves can be free-floating ball check valves; liquid is drawn from the container via a dip tube): https://patents.google.com/patent/US11267009B1
US Patent 8,863,989 B2, Soap dispenser including actuator with spring arm (when the head is released, the spring moves the piston back, creating a vacuum that lifts the ball check valve off its seat and draws soap from the container): https://patents.google.com/patent/US8863989B2
US Patent 10,875,043 B1, Lotion pump (a conventional lotion pump has a dip tube, a chamber with a spring, and a check valve between the chamber and the dip tube that lets liquid into the chamber but prevents reverse flow): https://patents.google.com/patent/US10875043B1"""
alt = ("3D animation of a soap pump bottle, with a voiceover. Under the question How does it pull the soap up? a finger presses the white pump head of a clear bottle of green soap on a wooden counter and soap streams out of the nozzle. "
       "Then the pump is shown cut in half: the fixed parts have red cut faces and the moving piston, stem and head have blue ones. 1, a piston, a spring and two little balls, each ball a one-way door. "
       "2, press: soap goes up and out. In slow motion the finger pushes the head down, the soap in the chamber is squeezed, the bottom ball is shut (red ring), the top ball lifts open (green ring), and dots of soap flow up the stem and out of the nozzle. "
       "3, let go: the finger lifts off and the spring pushes the piston and head back up. 4, top ball shuts, bottom lifts: the chamber gets bigger, suction arrows, the top ball drops shut and the bottom ball lifts open. "
       "5, new soap comes up the tube: dots of soap rise up the long tube from the bottom of the bottle into the chamber, the only way in. "
       "The payoff reads Two one-way balls, soap only goes up, a follow line appears and the video loops.")
on = ['INSIDE IT', 'HOW DOES IT PULL', 'THE SOAP UP?', 'A PISTON, A SPRING, 2 BALLS', 'PISTON', 'SPRING', 'TOP BALL', 'BOTTOM BALL', 'EACH BALL = A ONE-WAY DOOR',
      'PRESS: SOAP GOES UP AND OUT', 'SLOW MOTION', 'SHUT', 'OPEN', 'SQUEEZED', 'LET GO: THE SPRING PUSHES UP', 'FINGER OFF', 'TOP BALL SHUTS, BOTTOM LIFTS', 
      'NEW SOAP COMES UP THE TUBE', 'ONLY WAY IN', 'BIGGER CHAMBER = SUCTION', 'TWO ONE-WAY BALLS', 'SOAP ONLY GOES UP', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p100', track='A', group='E', slot='2026-11-26T21:00 Europe/London (planned, coordinator schedules)', topicKey='lotion pump',
  outlier='scorecard rule: everyday object you hold + one "why does it only go one way"; our own model, script, words and sound',
  topic="Lotion / soap dispenser pump: a piston, a return spring and two one-way ball valves. Pressing squeezes the chamber (bottom ball shut, top ball open) so soap goes out; releasing, the spring lifts the piston and the suction shuts the top ball and lifts the bottom ball, so soap is drawn up the dip tube.",
  hook="HOW DOES IT PULL / THE SOAP UP?", title="How Does It Pull the Soap Up? 🧴",
  principle="A manually operated dispensing pump has an inlet one-way valve between the dip tube and the pump chamber, a piston in the chamber, a compression spring and an outlet one-way valve; pressing raises the chamber pressure (inlet shut, outlet open, product dispensed), and the spring's return stroke creates a vacuum (outlet shut, inlet ball lifted) that draws product up the dip tube to refill the chamber.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://patents.google.com/patent/US11267009B1', 'https://patents.google.com/patent/US8863989B2', 'https://patents.google.com/patent/US10875043B1'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
import re
from spellchecker import SpellChecker
sp = SpellChecker(); txt = ' '.join([caption, first, alt] + on + vo)
words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z']+", re.sub(r'https?://\S+', ' ', txt)))
words = {w.strip("'") for w in words}; words = {w[:-2] if w.endswith("'s") else w for w in words}
print('spell flags:', sorted(sp.unknown(words)))
