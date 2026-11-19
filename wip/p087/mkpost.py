import json
caption = "Why Doesn't the Door Slam? 🚪\nGuess: what slows it down? 👇\nFollow @whyloop.hq for a new machine every day\n#howitworks #engineering #mechanism #doors #satisfying"
first = """Answer: oil and a tiny hole 🚪

The box at the top of the door is a door closer. When you open the door, the arm turns a small gear (a pinion). Its teeth push a toothed piston (the rack) along the closer's body, and the piston squeezes a strong spring.

Let go, and the spring pushes the piston back. That turns the gear the other way and pulls the door shut.

On its own, the spring would slam the door. But the closer's body is full of oil. As the piston moves back, the oil in front of it has to squeeze through small valve channels to get to the other side. The oil can only flow through so fast, so the door closes slowly and gently.

Small adjusting screws on the closer make those channels narrower or wider, which sets how fast the door closes. That's also why a closer that leaks its oil lets the door slam.

(Simplified 3D model; real closers have more valves and channels.)

Sources:
Yale, Door Closer catalog (rack and pinion: the arm rotates the pinion, which drives the piston and compresses the spring; the stored energy closes the door; the fluid flows freely as the door opens but must return through adjustable valves that control the closing and latching speed): https://www.yalehome.com/in/en/documents/catalouge/Yale%20Door%20Closer.pdf
LCN, Door Closer Reference Guide (the piston compresses the main spring; as the door closes the spring pushes the piston back and fluid is forced through the speed regulation valves; the flow of fluid through the valves controls the speed): https://www.lcnclosers.com/content/dam/allegion-us-2/web-files/lcn/information-documents/LCN_4040XP_Brochure_015520.pdf
Door Closers USA, Door closer adjustments (adjustment valves limit how much oil passes through the channels; a closer leaking oil lets the door slam): https://www.doorclosersusa.com/Commercial-Door-Closers-s/243.htm"""
alt = ("3D animation of a door closer, with a voiceover. Under the question Why doesn't the door slam? a wooden door closes gently while the closer arm swings. "
       "Then the closer box is shown opened from above. 1, open, the spring gets squeezed: a small top-view drawing shows the door swinging open while a gear turns and pushes a steel piston to the right, squeezing a spring. "
       "2, let go, the spring pushes back: the piston starts sliding slowly to the left, and the box is full of amber oil. "
       "3, without oil, slam: seen from above, the door with no oil slams shut in a fraction of a second. "
       "4, oil must squeeze through a tiny hole: back inside, the piston moves slowly to the left while amber oil dots crowd up in the channel, squeeze through a tiny hole above a brass screw, and spread out on the spring side. "
       "5, so the door closes gently. The payoff reads A tiny hole full of oil stops the slam, a follow line appears and the video loops.")
on = ['INSIDE IT', "WHY DOESN'T", 'THE DOOR SLAM?', 'OPEN: THE SPRING GETS SQUEEZED', 'SPRING', 'PISTON', 'GEAR', 'LET GO: THE SPRING PUSHES BACK', 'OIL', 'WITHOUT OIL: SLAM!', 'NO OIL',
      'OIL MUST SQUEEZE THROUGH A TINY HOLE', 'TINY HOLE', 'DOOR', 'SO THE DOOR CLOSES GENTLY', 'SLOW', 'A TINY HOLE FULL OF OIL', 'STOPS THE SLAM', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p087', track='A', group='E', slot='', topicKey='door closer',
  outlier='scorecard rule: everyday object you touch + one "why it does not slam"; our own model, script, words and sound',
  topic="Overhead hydraulic door closer: opening turns the pinion, the rack-piston squeezes the spring; the spring closes the door, but the piston must push oil through a tiny adjustable hole, so it closes gently.",
  hook="WHY DOESN'T / THE DOOR SLAM?", title="Why Doesn't the Door Slam? 🚪",
  principle="A rack-and-pinion door closer stores the opening energy in a spring; on closing the spring drives the piston back and the hydraulic fluid in front of it must pass through small adjustable valve passages, which limits the piston (and door) speed.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://www.yalehome.com/in/en/documents/catalouge/Yale%20Door%20Closer.pdf', 'https://www.lcnclosers.com/content/dam/allegion-us-2/web-files/lcn/information-documents/LCN_4040XP_Brochure_015520.pdf', 'https://www.doorclosersusa.com/Commercial-Door-Closers-s/243.htm'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
import re
from spellchecker import SpellChecker
sp = SpellChecker(); txt = ' '.join([caption, first, alt] + on + vo)
words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z']+", re.sub(r'https?://\S+', ' ', txt)))
words = {w.strip("'") for w in words}; words = {w[:-2] if w.endswith("'s") else w for w in words}
print('spell flags:', sorted(sp.unknown(words)))
