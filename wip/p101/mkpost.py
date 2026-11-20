import json
caption = "How Does the Shoe Click In? 🚲\nGuess: push down or twist to get out? 👇\nFollow @whyloop.hq for a new machine every day\n#howitworks #cycling #mechanism #engineering #bike"
first = """Answer: push down to click in, twist your heel out to get free 🚲

A clipless (SPD-style) pedal has two jaws. A small metal cleat is bolted under the shoe. You put the front of the cleat under the front jaw first, then push your heel down.

The back jaw is held shut by a spring. The edge of the cleat pushes it back out of the way, and once the cleat is past, the spring snaps the jaw over the end of the cleat. Click: now both jaws hold the cleat's ends from above, so pulling up on the pedal doesn't free it (with the standard single-release cleats).

To get out, twist your heel outward. The turning cleat pushes the back jaw open and the shoe lifts free. A screw at the back of each binding sets the spring tension, so you choose how hard that twist is.

(Simplified 3D model, side view and top view; the real binding shapes and springs differ between pedal models.)

Sources:
Shimano SPD Pedals user's manual UM-45F0A (press the cleats into the pedals with a forward and downward motion; release by twisting your heels outward; the adjustment bolt at the rear of each binding sets the spring force of the binding): https://si.shimano.com/en/pdfs/um/45F0A/UM-45F0A-002-00-ENG.pdf
Shimano SPD Pedals user's manual UM-L800B (single release mode cleats only release when the heel is moved outward; upward force may be applied to the pedal, since the cleat will not release unless the foot is twisted): https://si.shimano.com/en/pdfs/um/L800B/UM-L800B-000-ENG.pdf
Shimano, SPD technology page (step down firmly to engage, kick your heel outward to exit; adjustable spring tension): https://bike.shimano.com/en-NA/technologies/details/spd.html
US Patent 6,341,540, Clipless pedal (pressing the cleat's camming surfaces against the spring plates forces them apart, then they spring back and capture the cleat): https://patents.google.com/patent/US6341540"""
alt = ("3D animation of a bike shoe on a clipless pedal, with a voiceover. Under the question How does the shoe click in? the shoe steps onto the pedal and clicks in. "
       "Then a side view of the pedal: a gold metal cleat under the sole, a fixed front jaw, a back jaw on a pin and two black springs behind it. "
       "1, cleat hooks under the front jaw: the cleat slides forward, toe first, under the front jaw. "
       "2, heel down, cleat pushes the back jaw: an arrow pushes the heel down, the end of the cleat pushes the back jaw backward and the springs squeeze. "
       "3, the spring snaps it shut, click: in slow motion the back jaw snaps over the end of the cleat, click, locked. "
       "4, pull up, still locked: an arrow pulls up and both jaws hold the cleat's ends. "
       "5, twist the heel out, free: seen from above, the heel swings outward, the cleat's corner pushes the back jaw open and the shoe lifts free. "
       "The payoff reads Push down: click in, twist heel: out, a follow line appears and the video loops.")
on = ['INSIDE IT', 'HOW DOES THE SHOE', 'CLICK IN?', 'CLEAT HOOKS UNDER THE FRONT JAW', 'CLEAT', 'FRONT JAW', 'BACK JAW', 'HEEL DOWN: CLEAT PUSHES THE BACK JAW', 'SPRING SQUEEZED',
      'THE SPRING SNAPS IT SHUT: CLICK', 'CLICK: LOCKED', 'SLOW MOTION', 'PULL UP: STILL LOCKED', 'HELD HERE', 'AND HERE', 'TWIST THE HEEL OUT: FREE', 'HEEL OUT', 'CORNER PUSHES THE JAW', 'FREE',
      'PUSH DOWN: CLICK IN', 'TWIST HEEL: OUT', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p101', track='A', group='V', slot='2026-11-26T17:00 Europe/London (planned, coordinator schedules)', topicKey='clipless pedal',
  outlier='scorecard rule: everyday object you use + one "why does it click / lock"; our own model, script, words and sound',
  topic="Clipless (SPD-style) bike pedal: the cleat hooks under the front jaw, pushing the heel down cams the spring-loaded back jaw open until it snaps over the cleat; pulling up cannot free it; twisting the heel outward pushes the back jaw open and releases the cleat.",
  hook="HOW DOES THE SHOE / CLICK IN?", title="How Does the Shoe Click In? 🚲",
  principle="The cleat is pressed into the binding toe first with a forward and downward motion; its edge cams the spring-loaded rear binding open until the binding springs back and captures the cleat; the single-release cleat cannot be released by an upward pull, only by twisting the heel outward, which cams the binding open; an adjustment bolt at the rear of each binding sets the spring force.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://si.shimano.com/en/pdfs/um/45F0A/UM-45F0A-002-00-ENG.pdf', 'https://si.shimano.com/en/pdfs/um/L800B/UM-L800B-000-ENG.pdf', 'https://bike.shimano.com/en-NA/technologies/details/spd.html', 'https://patents.google.com/patent/US6341540'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
import re
from spellchecker import SpellChecker
sp = SpellChecker(); txt = ' '.join([caption, first, alt] + on + vo)
words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z']+", re.sub(r'https?://\S+', ' ', txt)))
words = {w.strip("'") for w in words}; words = {w[:-2] if w.endswith("'s") else w for w in words}
print('spell flags:', sorted(sp.unknown(words)))
