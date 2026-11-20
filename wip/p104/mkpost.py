import json, re
caption = "How Does a Flask Keep Coffee Hot? ☕\nGuess: what's between the two walls? 👇\nFollow @whyloop.hq for a new machine every day\n#howitworks #thermos #science #physics #coffee"
first = """Answer: almost nothing, a vacuum ☕

A vacuum flask (a Thermos) is really one bottle inside another. The two walls touch only at the neck, and the gap between them has had almost all of its air pumped out.

Heat leaves hot coffee in three ways. Conduction and convection both need stuff, like air, to carry the heat. With air in the gap, the air would carry the heat across to the outer wall and out into the room. A vacuum has almost nothing to carry it, so that path is blocked. That is also why the outside of the flask stays at about room temperature.

The third way, radiation (heat rays), can cross a vacuum, so the walls facing the gap are shiny like a mirror and bounce most of it back. The stopper blocks the top, which is where most of the heat that does escape gets out. The flask does not make heat; it just lets it out very slowly, so a hot drink stays hot for hours (and a cold one stays cold).

(Simplified 3D model; the gap is drawn wider than in a real flask, and the dots and arrows show the idea, not real air molecules.)

Sources:
Encyclopaedia Britannica, Vacuum flask (double walls with the space between evacuated; practically a nonconductor of heat; radiation reduced by silvering; the neck is the main path for heat; a hot liquid stays hot for several hours): https://www.britannica.com/technology/vacuum-flask
HowStuffWorks, How Thermoses (Vacuum Flasks) Work (without atoms you eliminate conduction and convection; silvering reduces infrared radiation; the cap is the biggest remaining path): https://home.howstuffworks.com/thermos2.htm
BBC Bitesize, The vacuum flask (vacuum prevents conduction and convection through the sides; silvered surfaces reduce radiation; the cap reduces losses through the top): https://www.bbc.co.uk/bitesize/guides/z32nf82/revision/14
University of Sydney, School of Physics, Thermos Flask (the outer wall stays at about room temperature; conduction only where the two walls meet; silvered walls reflect radiated heat back inside): https://www.physics.usyd.edu.au/super/physics_tut/activities/Thermal_Physics/Thermos_Flask.pdf"""
alt = ("3D animation of a brushed steel vacuum flask on a wooden table, with a voiceover. Under the question How does it keep coffee hot? the flask pours steaming coffee into a black cup, with a red circle on its side. "
       "Then the flask is shown cut in half with red cut faces: hot coffee inside, an inner wall, an outer wall and a gap between them labelled Vacuum: no air. "
       "1, two walls, no air between. 2, air would carry heat out: close up on the wall, the gap fills with blue air dots; orange heat dots leave the coffee, cross the gap and escape, and the outer wall glows orange: outside gets hot. "
       "3, a vacuum carries nothing: the air dots disappear and the gap turns dark; the heat dots now bounce back before the wall: heat stays in, outside stays cool. "
       "4, shiny walls and a tight lid: wavy heat rays hit the shiny wall and bounce back, then a black stopper screws into the neck: lid seals the top. "
       "The payoff reads No air in the gap, so heat can't get out, over the steaming cup, a follow line appears and the video loops.")
on = ['INSIDE IT', 'HOW DOES IT KEEP', 'COFFEE HOT?', 'TWO WALLS, NO AIR BETWEEN', 'HOT COFFEE', 'INNER WALL', 'OUTER WALL', 'VACUUM: NO AIR', 'AIR WOULD CARRY HEAT OUT', 'IF IT HAD AIR',
      'HEAT ESCAPES', 'OUTSIDE GETS HOT', 'A VACUUM CARRIES NOTHING', 'NOTHING TO CARRY IT', 'HEAT STAYS IN', 'OUTSIDE STAYS COOL', 'SHINY WALLS + A TIGHT LID', 'SHINY WALL BOUNCES IT BACK',
      'LID SEALS THE TOP', 'NO AIR IN THE GAP', "SO HEAT CAN'T GET OUT", 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p104', track='A', group='E', slot='2026-11-27T17:00 Europe/London (planned, coordinator schedules)', topicKey='vacuum flask',
  outlier='scorecard rule: everyday object you hold + one "how does it"; lathe body (rule 5); our own model, script, words and sound',
  topic="Vacuum flask: a near-vacuum between two walls leaves nothing to carry heat by conduction or convection; shiny walls reflect radiated heat; the stopper blocks the top.",
  hook="HOW DOES IT KEEP / COFFEE HOT?", title="How Does a Flask Keep Coffee Hot? ☕",
  principle="Double-walled vessel with the space between the walls evacuated: with almost no gas, heat cannot cross the gap by conduction or convection; silvered/polished walls reflect thermal radiation; the walls join only at the narrow neck and the stopper limits losses through the top.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://www.britannica.com/technology/vacuum-flask', 'https://home.howstuffworks.com/thermos2.htm', 'https://www.bbc.co.uk/bitesize/guides/z32nf82/revision/14', 'https://www.physics.usyd.edu.au/super/physics_tut/activities/Thermal_Physics/Thermos_Flask.pdf'])
try: P.update({k: v for k, v in json.load(open('post.json')).items() if k in ('qualityAudit', 'visualScore', 'reviews', 'version', 'status')})
except Exception: pass
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
from spellchecker import SpellChecker
sp = SpellChecker(); txt = ' '.join([caption, first, alt] + on + vo)
words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z']+", re.sub(r'https?://\S+', ' ', txt)))
words = {w.strip("'") for w in words}; words = {w[:-2] if w.endswith("'s") else w for w in words}
print('spell flags:', sorted(sp.unknown(words)), '| first comment chars', len(first))
