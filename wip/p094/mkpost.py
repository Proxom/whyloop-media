import json
caption = "One Flick, No Glare? 🚗\nGuess: where does the bright reflection go? 👇\nFollow @whyloop.hq for a new machine every day\n#howitworks #engineering #cars #physics #mechanism"
first = """Answer: it goes up to the roof 🚗

The glass in a day/night rear-view mirror is a wedge: thicker at the top than at the bottom, with the shiny silver coating on the BACK.

Light from the headlights behind you reflects twice: a strong reflection from the silvered back (roughly 90 % of the light) and a weak one from the plain front of the glass (only about 4 %). Because the glass is a wedge, those two reflections leave at different angles.

By day, the mirror is aimed so the bright back reflection reaches your eyes. Flip the tab and the whole mirror tilts up a little. Now the bright reflection goes up toward the roof, and only the weak 4 % reflection from the front of the glass reaches you. Headlights look dim, but you can still see the cars behind you.

(Simplified 3D model: the wedge angle, the tilt and the car interior are exaggerated and squeezed so you can see the light paths. Real wedges are only a few degrees.)

Sources:
US patent 4,679,906, Anti-glare rear view mirror (front surface about 4 % reflectivity, rear reflecting surface about 90 %): https://patents.google.com/patent/US4679906
Wikipedia, Rear-view mirror (prismatic day/night mirror: wedge-shaped glass, the night position tilts the silvered back out of the driver's line of sight so the view comes from the low-reflection front surface): https://en.wikipedia.org/wiki/Rear-view_mirror
Indiana Public Media, A Moment of Science, Rear view mirror (flipping the switch changes the angle of the whole setup; the silvered surface then points up at the car's ceiling): https://indianapublicmedia.org/amomentofscience/rear-view-mirror/"""
alt = ("3D animation of a car's rear-view mirror, with a voiceover. Under the question One flick, no glare? two bright headlights glare in the mirror, a small tab under it flips, and the headlights turn dim. "
       "The camera moves to the side and the mirror is cut in half. 1, the glass is a wedge: the glass is thicker at the top, with a silver layer on the back. "
       "2, day: a beam from the headlights enters the glass, bounces off the silver back and goes straight to a drawn eye, marked glare; a small box called what you see shows two bright headlights. "
       "3, the front glass reflects only 4 percent: a thin blue beam bounces off the front of the glass and goes down, away from the eye. "
       "4, flip the tab, it tilts up: the tab flips and the whole mirror tilts up, and the beams swing. "
       "5, night: the bright beam now hits the roof, and only the thin 4 percent beam reaches the eye, marked dim; the headlights in the what you see box are now small and dim. "
       "Back in front of the mirror the payoff reads The bright reflection goes to the roof, a follow line appears and the video loops.")
on = ['INSIDE IT', 'ONE FLICK,', 'NO GLARE?', 'THE GLASS IS A WEDGE', 'WEDGE', 'SILVER BACK', 'DAY: SILVER BACK → YOUR EYES', 'HEADLIGHTS', 'GLARE!', 'WHAT YOU SEE',
      'FRONT GLASS REFLECTS ONLY 4%', '4%', '90%', 'FLIP THE TAB: IT TILTS UP', 'TAB', 'NIGHT: ONLY 4% REACHES YOU', 'ROOF', 'ONLY 4%: DIM', 'THE BRIGHT REFLECTION', 'GOES TO THE ROOF', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p094', track='A', group='V', slot='2026-11-21 21:00', topicKey='rearview mirror day night',
  outlier='scorecard rule: everyday thing you touch (the mirror tab) + one "why does it stop the glare"; our own model, script, words and sound',
  topic="Prismatic day/night rear-view mirror: the glass is a wedge silvered on the back; flipping the tab tilts it so the bright back reflection goes to the roof and only the ~4 % front-surface reflection reaches the driver.",
  hook="ONE FLICK, / NO GLARE?", title="One Flick, No Glare? 🚗",
  principle="A prismatic mirror's wedge glass gives two reflections at different angles: ~90 % from the silvered back and ~4 % from the uncoated front; the night position tilts the mirror so the bright back reflection misses the driver's eyes and only the dim front reflection is seen.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://patents.google.com/patent/US4679906', 'https://en.wikipedia.org/wiki/Rear-view_mirror', 'https://indianapublicmedia.org/amomentofscience/rear-view-mirror/'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
import re
from spellchecker import SpellChecker
sp = SpellChecker(); txt = ' '.join([caption, first, alt] + on + vo)
words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z']+", re.sub(r'https?://\S+', ' ', txt)))
words = {w.strip("'") for w in words}; words = {w[:-2] if w.endswith("'s") else w for w in words}
print('spell flags:', sorted(sp.unknown(words)))
