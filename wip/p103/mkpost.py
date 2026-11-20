import json
caption = "Why Does the Mirror Tab Stop the Glare? 🚗\nGuess: does the tab darken the glass, or tilt it? 👇\nFollow @whyloop.hq for a new machine every day\n#howitworks #cars #engineering #physics #carsofinstagram"
first = """Answer: it tilts it 🚗

A manual day/night rear-view mirror (a prismatic mirror) is made of glass shaped like a thin wedge: thicker at the top, with a shiny silver coating on the back.

Light from the cars behind you reflects twice: very brightly off the silver back, and weakly off the plain glass front (only about 4% of the light). Because the wedge's two surfaces are not parallel, the two reflections leave at slightly different angles.

Day position: the bright reflection from the silver back is aimed at your eyes, and the weak one goes elsewhere.

Flip the tab and the whole mirror tilts a little. Now the bright silver reflection misses your eyes (from where you sit, the silver only shows the dark roof), and the weak 4% reflection from the glass front lines up with your eyes. The headlights behind you look dim, but you can still see them.

(Simplified 3D diagram, not to scale: the wedge angle is exaggerated, the car behind and your eye are drawn close, and the small bend of the light inside the glass is left out.)

Sources:
Wikipedia, Rearview mirror (prismatic day/night mirror: wedge-shaped glass; day: the reflective back gives a strong reflection; night: the back is tilted out of line with the driver's view and the low-reflection front surface is seen): https://en.wikipedia.org/wiki/Rearview_mirror
HowStuffWorks, How does a car's rearview mirror work when it's in the glare-resistant setting? (wedge-shaped, thicker edge at the top; flipped, the mirrored back points toward the dark ceiling and you see the dimmer front-surface reflection): https://auto.howstuffworks.com/question20.htm
Science World, How does the rearview mirror antiglare work? (the front glass surface reflects only about four percent of incoming light; flipping the tab sends the headlights off the silvered surface away from your eyes): https://www.scienceworld.ca/stories/how-does-rearview-mirror-antiglare-work
University of Michigan Transportation Research Institute report on rearview mirrors (in the antiglare setting the image comes from the front glass surface, about 4% reflectivity for glass with an index of refraction of about 1.5): https://backend.production.deepblue-documents.lib.umich.edu/server/api/core/bitstreams/edd4df2a-220d-4982-9513-6127467b47a1/content"""
alt = ("3D animation of a car's rear-view mirror at night, with a voiceover. Under the question Why does the tab dim the lights? two headlights blaze in the mirror with a big glare; a red circle marks the small tab under the mirror, the tab flips and the glare drops to two dim lights. "
       "Then the mirror is shown from the side, cut open: 1, the glass is a wedge: the light blue glass is thick at the top and thin at the bottom, with a silver back. "
       "2, day: the silver shines in: a yellow beam from the car behind enters the glass, bounces off the silver back and goes straight to a drawn eye, labeled silver: bright; a thin pale beam bounces off the glass front and goes low, labeled glass: only 4%. "
       "3, flip the tab: it all tilts: close up, the tab under the mirror swings and the whole mirror tilts a little; the bright beam now passes above the eye, labeled bright: misses your eye. "
       "4, night: only the glass: the thin pale beam now reaches the eye, labeled only 4% reaches you, and back in the mirror the headlights are dim but still visible. "
       "The payoff reads You see the weak glass, not the bright silver, a follow line appears and the video loops.")
on = ['INSIDE IT', 'WHY DOES THE TAB', 'DIM THE LIGHTS?', 'THE GLASS IS A WEDGE', 'THICK TOP', 'THIN BOTTOM', 'SILVER BACK', 'PLAIN GLASS', 'DAY: THE SILVER SHINES IN', 'CAR BEHIND', 'YOUR EYE',
      'SILVER: BRIGHT', 'GLASS: ONLY 4%', 'FLIP THE TAB: IT ALL TILTS', 'TAB', 'BRIGHT: MISSES YOUR EYE', 'NIGHT: ONLY THE GLASS', 'ONLY 4% REACHES YOU', 'DIM, BUT STILL VISIBLE',
      'YOU SEE THE WEAK GLASS', 'NOT THE BRIGHT SILVER', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p103', track='A', group='V', slot='2026-11-27T01:00 Europe/London (planned, coordinator schedules)', topicKey='rearview mirror dimming',
  topicKeyLine='topic key: rearview mirror dimming (synonyms: prismatic day/night mirror, rear-view mirror flip tab) - not in learnings/topics-used.md (coordinator checked 95 lines; no mirror/optics row)',
  outlier='scorecard rule: hand-sized everyday object + one "why does it" question; our own model, script, words and sound',
  topic="Prismatic day/night rear-view mirror: the glass is a wedge with a silvered back; the tab tilts the whole mirror so the bright silver reflection misses the eye and only the ~4% front-glass reflection reaches it.",
  hook="WHY DOES THE TAB / DIM THE LIGHTS?", title="Why Does the Mirror Tab Stop the Glare? 🚗",
  principle="A prismatic mirror's front glass surface and silvered back are not parallel (a wedge), so their reflections leave at different angles; flipping the tab tilts the mirror so the weak front-surface reflection (about 4%) instead of the strong silvered-back reflection reaches the driver's eye.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://en.wikipedia.org/wiki/Rearview_mirror', 'https://auto.howstuffworks.com/question20.htm', 'https://www.scienceworld.ca/stories/how-does-rearview-mirror-antiglare-work',
           'https://backend.production.deepblue-documents.lib.umich.edu/server/api/core/bitstreams/edd4df2a-220d-4982-9513-6127467b47a1/content', 'https://driving.ca/column/how-it-works/how-it-works-mirrors'])
old = {}
try: old = json.load(open('post.json'))
except Exception: pass
for k in ('qualityAudit', 'visualScore', 'clarity', 'media'):
    if k in old: P[k] = old[k]
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
import re
from spellchecker import SpellChecker
sp = SpellChecker(); txt = ' '.join([caption, first, alt] + on + vo)
words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z']+", re.sub(r'https?://\S+', ' ', txt)))
words = {w.strip("'") for w in words}; words = {w[:-2] if w.endswith("'s") else w for w in words}
print('spell flags:', sorted(sp.unknown(words)), '| first comment chars', len(first), '| caption chars', len(caption))
