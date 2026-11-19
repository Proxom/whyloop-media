import json
caption = "Why Doesn't the Air Leak Out of Your Tire? 🚲\nGuess: what keeps the valve shut? 👇\nFollow @whyloop.hq for a new machine every day\n#bike #cars #howitworks #mechanism #engineering"
first = """Answer: the tire's own air 🚲

Inside a Schrader valve (the kind on car tires and many bikes) is a valve core: a little check valve. A rubber seal sits on a thin pin, and a small spring pushes the seal up against its seat.

The air inside the tire pushes on the seal from below too, so the higher the pressure, the harder the seal is pressed shut.

When you put a pump on, a small pusher in the pump head presses the pin down and opens the seal. The pump's air is at a higher pressure than the tire, so it flows in.

Take the pump off, and the spring and the tire pressure close the valve again. That's the short puff of air you hear when you pull the pump off.

(Simplified 3D model; real valve cores differ in detail.)

Sources:
Schrader Pacific, Valve Cores (a spring-actuated cartridge-type check valve; the hose fitting pushes the core pin inward to let air in; when it is removed, the core's spring and the internal tire pressure close the valve): https://schrader-pacific.com/wp-content/uploads/Valve-Cores.pdf
OnAllCylinders, Tires 101: What Is a Schrader Valve (a poppet valve opened by a pin in the air fitting; air flows in when the source pressure is higher than the tire; the valve snaps shut when the fitting is removed): https://www.onallcylinders.com/2023/06/02/tires-101-what-is-a-schrader-valve-and-how-to-use-a-tire-valve-core-removal-tool"""
alt = ("3D animation of a bike tire valve, with a voiceover. Under the question Why doesn't the air escape? a pump is pulled off the valve and a small seal snaps shut. "
       "The bike wheel's valve cap unscrews and the valve is cut open in red to show a brass core, a thin pin, a black rubber seal and a spring. "
       "1, inside, a tiny door: the seal on the pin sits under its seat, with the outside at the top and the tire at the bottom. 2, a spring pushes it up. 3, tire air pushes it up too: orange arrows push the seal against the seat. "
       "4, the pump presses the pin: a pump head slides on and its pusher presses the pin down, opening the seal. 5, pump air is stronger: a big blue arrow and blue air flow down past the seal into the tire while the orange tire-air arrows shrink. "
       "6, pump off, the door slams: the pump lifts, the orange arrows grow and the seal snaps up and shuts. The payoff reads The air inside holds the door shut, a follow line appears and the video loops.")
on = ['INSIDE IT', "WHY DOESN'T", 'THE AIR ESCAPE?', 'INSIDE: A TINY DOOR', 'SEAL', 'SEAT', 'PIN', 'OUTSIDE ↑', 'TIRE ↓', 'A SPRING PUSHES IT UP', 'SPRING', 'TIRE AIR PUSHES IT UP TOO', 'TIRE AIR',
      'THE PUMP PRESSES THE PIN', 'PUMP', 'OPEN', 'PUMP AIR IS STRONGER', 'PUMP AIR', 'PUMP OFF: THE DOOR SLAMS', 'SHUT', 'THE AIR INSIDE', 'HOLDS THE DOOR SHUT', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p085', track='A', group='V', slot='', topicKey='schrader valve',
  outlier='scorecard rule: everyday object you touch + one "why it stays shut" (lock/one-way theme); our own model, script, words and sound',
  topic="Schrader tire valve: a spring and the tire's own air pressure hold the core's seal against its seat; the pump's pusher opens it, the higher pump pressure flows in, and the seal recloses when the pump comes off.",
  hook="WHY DOESN'T / THE AIR ESCAPE?", title="Why Doesn't the Air Leak Out of Your Tire? 🚲",
  principle="A Schrader valve core is a spring-loaded poppet (check) valve: the spring and the internal tire pressure hold the seal against the barrel's seat; depressing the core pin (by the pump fitting) lifts the seal off the seat so higher-pressure air can flow in; when the fitting is removed the spring and tire pressure reclose it.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://schrader-pacific.com/wp-content/uploads/Valve-Cores.pdf', 'https://www.onallcylinders.com/2023/06/02/tires-101-what-is-a-schrader-valve-and-how-to-use-a-tire-valve-core-removal-tool'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
import re
from spellchecker import SpellChecker
sp = SpellChecker(); txt = ' '.join([caption, first, alt] + on + vo)
words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z']+", re.sub(r'https?://\S+', ' ', txt)))
words = {w.strip("'") for w in words}; words = {w[:-2] if w.endswith("'s") else w for w in words}
print('spell flags:', sorted(sp.unknown(words)))
