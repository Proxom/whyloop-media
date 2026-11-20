import json
caption = "How Does a Spinning Wheel Light the Lamp? 🚲\nGuess: is there a battery inside? 👇\nFollow @whyloop.hq for a new machine every day\n#bike #howitworks #cycling #engineering #physics"
first = """Answer: no battery, a spinning magnet 🧲

This is a bottle dynamo (also called a sidewall dynamo). Its small ribbed roller presses on the side of the tire, so when the wheel turns, the tire spins the roller. The roller is much smaller than the wheel, so it spins many times faster.

Inside, the roller turns a permanent magnet that sits in the middle of a fixed coil of copper wire. A moving magnet changes the magnetic field inside the coil, and that makes electricity flow in the wire (electromagnetic induction, found by Michael Faraday). The wire carries it to the lamp.

The faster the magnet spins, the more electricity it makes, so the light gets brighter. Stop the bike and nothing spins, so the light goes out. Real bike dynamos are usually rated about 6 volts, 3 watts, and are built so the power only rises a little above normal riding speed.

(Simplified 3D model, slowed down: a real dynamo uses a multi-pole magnet, and the roller spins much faster than shown.)

Sources:
Wikipedia, Bottle dynamo (a roller on the sidewall of the tire; the tire spins the roller; inside, a permanent magnet turns with the friction wheel next to an induction coil; it is really a small magneto that makes AC): https://en.wikipedia.org/wiki/Bottle_dynamo
Wikipedia, Bicycle lighting (bicycle dynamos are magnetos; generally limited to about 3 W): https://en.wikipedia.org/wiki/Bicycle_lighting
Pilom, Bicycle Dynamos (permanent magnet alternators; most rated 3 W, that is 500 mA at 6 V; zero power at standstill, about 3 W at moderate speed and a little more at very high speed): http://pilom.com/BicycleElectronics/Dynamo.htm
OpenStax, University Physics Volume 2, 13.1 Faraday's Law (moving a magnet relative to a coil induces an emf; the faster the motion, the greater the emf; no emf when the magnet is still): https://openstax.org/books/university-physics-volume-2/pages/13-1-faradays-law"""
alt = ("3D animation of a bicycle front wheel with a tan-wall tire, a green fork, a silver bottle dynamo and a round black headlight, with a voiceover. Under the question How does the wheel light the lamp? the wheel spins, the headlight shines, and a red circle marks the dynamo's small roller on the tire. "
       "1, the tire spins the roller: close up, the tire's side turns the small black ribbed roller, labelled Tire, Roller and Tiny equals spins fast. "
       "2, a magnet spins inside: the dynamo is cut open with red cut faces, showing a red and blue magnet spinning in the middle of a copper coil of wire. "
       "3, spinning magnet equals electricity: the coil glows, and yellow dots of electricity run from the coil up a wire to the lamp, which lights up. "
       "4, faster equals brighter: the wheel speeds up, more dots flow and the lamp gets brighter, labelled Fast: bright; then the wheel stops, the dots stop and the lamp goes dark, labelled Stop: dark. "
       "The payoff reads The wheel spins a magnet, the magnet makes power, the wheel starts again, a follow line appears and the video loops.")
on = ['INSIDE IT', 'HOW DOES THE WHEEL', 'LIGHT THE LAMP?', 'THE TIRE SPINS THE ROLLER', 'TIRE', 'ROLLER', 'TINY = SPINS FAST', 'A MAGNET SPINS INSIDE', 'MAGNET', 'COIL OF COPPER WIRE',
      'SPINNING MAGNET = ELECTRICITY', 'ELECTRICITY', 'SPINNING MAGNET', 'LAMP', 'FASTER = BRIGHTER', 'SLOW: DIM', 'FAST: BRIGHT', 'STOP: DARK',
      'THE WHEEL SPINS A MAGNET', 'THE MAGNET MAKES POWER', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p105', track='A', group='V', slot='2026-11-27T01:00 Europe/London (planned, coordinator schedules; replaces p103 rear-view mirror, visual 4 + clarity NO)', topicKey='bike dynamo',
  topicKeyLine='topic key: bike dynamo (synonyms: bottle dynamo, sidewall dynamo, bicycle generator) - not in learnings/topics-used.md (coordinator checked 95 rows; speedometer p092 = magnet drags a cup, different object and idea)',
  outlier='scorecard rule: everyday object you see + one "how does it" question; our own model, script, words and sound',
  topic="Bicycle bottle (sidewall) dynamo: the tire spins a small roller; the roller spins a permanent magnet inside a fixed copper coil; the changing magnetic field induces a current that lights the lamp; faster = brighter, stopped = dark.",
  hook="HOW DOES THE WHEEL / LIGHT THE LAMP?", title="How Does a Spinning Wheel Light the Lamp? 🚲",
  principle="Friction roller on the tire sidewall drives a permanent-magnet rotor inside a stationary induction coil (a magneto); the rotating field changes the flux through the coil and induces an alternating emf (Faraday's law) whose size grows with the rotation speed; zero at standstill.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://en.wikipedia.org/wiki/Bottle_dynamo', 'https://en.wikipedia.org/wiki/Bicycle_lighting', 'http://pilom.com/BicycleElectronics/Dynamo.htm', 'https://openstax.org/books/university-physics-volume-2/pages/13-1-faradays-law'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
import re
from spellchecker import SpellChecker
sp = SpellChecker(); txt = ' '.join([caption, first, alt] + on + vo)
words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z']+", re.sub(r'https?://\S+', ' ', txt)))
words = {w.strip("'") for w in words}; words = {w[:-2] if w.endswith("'s") else w for w in words}
print('spell flags:', sorted(sp.unknown(words)), '| first comment chars', len(first))
