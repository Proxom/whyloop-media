import json
caption = "Why Does the Pressure Cooker Weight Dance? 🍲\nGuess: what lifts it, steam or springs? 👇\nFollow @whyloop.hq for a new machine every day\n#howitworks #pressurecooker #cooking #science #engineering"
first = """Answer: steam 🍲

On an old-style (\"jiggle-top\") pressure cooker, a heavy metal weight, the pressure regulator, sits on a thin vent pipe in the lid and plugs it.

As the water boils, the steam can't get out, so the pressure inside builds up and pushes up on the weight through the pipe's tiny hole. When that push gets bigger than the weight, the weight lifts a little, a puff of steam escapes, the pressure drops a little and the weight falls back. Up, down, again and again: that is the rocking.

So the weight sets the top pressure. On a standard US cooker it starts to rock at about 15 psi above normal air pressure. At that pressure water boils at about 121 °C (250 °F) instead of 100 °C (212 °F), so food cooks faster.

(Simplified 3D model, slowed down; the pipe and the lift are drawn bigger than real. Many newer cookers use a spring valve instead of a weight.)

Sources:
Presto, Pressure Cooking - How to Use (the pressure regulator fits on the vent pipe, allows excess pressure to be released and maintains the pressure, usually 15 pounds): https://www.gopresto.com/content/pressure-cooking/pressure-cooking-how-to-use
Presto, Pressure Cooking - FAQ (on a weighted gauge cooker the regulator begins to rock when 15 pounds pressure is reached): http://www.gopresto.com/content/pressure-cooking/pressure-cooking-faq
HyperPhysics (Georgia State University), Pressure Cooker (a controlled vent at about 15 lb/in² above atmospheric pressure raises the boiling point to about 121 °C): http://hyperphysics.phy-astr.gsu.edu/hbase/thermo/precook.html
Wikipedia, Pressure cooker (weight-modified or \"jiggler\" valve releases pressure during operation and rattles as excess steam is released; at 15 psi gauge water boils at 121 °C / 250 °F): https://en.wikipedia.org/wiki/Pressure_cooker"""
alt = ("3D animation of a steel pressure cooker on a glowing stove, with a voiceover. Under the question Why does this weight dance? a red circle marks the small black weight on top of the lid, which bobs up and down while puffs of steam come out. "
       "Then the cooker is shown cut in half with red cut faces: water at the bottom and white steam puffs above it. 1, the weight plugs the pipe: the weight sits on a thin pipe in the lid. "
       "2, steam pushes up: close up, a blue arrow labelled steam push grows under the weight while an orange arrow labelled weight pushes down. "
       "3, push beats weight, it lifts: the arrows are equal, the weight rises a little and steam puffs out from under it. "
       "4, steam out, it drops back: the push gets smaller than the weight and the weight falls back onto the pipe, then lifts and drops again. "
       "Back outside, the weight keeps dancing and the payoff reads The weight sets the top pressure, a follow line appears and the video loops.")
on = ['INSIDE IT', 'WHY DOES THIS', 'WEIGHT DANCE?', 'THE WEIGHT PLUGS THE PIPE', 'WEIGHT', 'THIN PIPE', 'STEAM TRAPPED', 'STEAM PUSHES UP', 'STEAM PUSH',
      'PUSH BEATS WEIGHT: IT LIFTS', 'STEAM OUT', 'STEAM OUT, IT DROPS BACK', 'PUSH < WEIGHT: DROPS', 'THE WEIGHT SETS', 'THE TOP PRESSURE', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p106', track='A', group='E', slot='2026-11-27T17:00 Europe/London (planned, coordinator schedules)', topicKey='pressure cooker weight',
  topicKeyLine='topic key: pressure cooker weight (synonyms: jiggler, pressure regulator weight, weighted valve) - not in learnings/topics-used.md (coordinator checked 95 rows)',
  outlier='scorecard rule: everyday object + one "why does it..." question; our own model, script, words and sound',
  topic="Pressure cooker weighted regulator (jiggler): the weight plugs the vent pipe; steam pressure x hole area lifts it when it exceeds the weight, steam escapes, pressure drops, it falls back, so the weight sets the maximum pressure.",
  hook="WHY DOES THIS / WEIGHT DANCE?", title="Why Does the Pressure Cooker Weight Dance? 🍲",
  principle="A calibrated weight rests on the vent pipe; it lifts when the steam pressure times the vent hole area exceeds its weight, releasing steam until the pressure falls back, so the cooker is held at about the pressure set by the weight (15 psi gauge on a standard US cooker).",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://www.gopresto.com/content/pressure-cooking/pressure-cooking-how-to-use', 'http://www.gopresto.com/content/pressure-cooking/pressure-cooking-faq',
           'http://hyperphysics.phy-astr.gsu.edu/hbase/thermo/precook.html', 'https://en.wikipedia.org/wiki/Pressure_cooker'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
import re
from spellchecker import SpellChecker
sp = SpellChecker(); txt = ' '.join([caption, first, alt] + on + vo)
words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z']+", re.sub(r'https?://\S+', ' ', txt)))
words = {w.strip("'") for w in words}; words = {w[:-2] if w.endswith("'s") else w for w in words}
print('spell flags:', sorted(sp.unknown(words)), '| first comment chars', len(first))
