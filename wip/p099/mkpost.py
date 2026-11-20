import json
caption = "Why Do You Have to Pull the Mask Down? ✈️\nGuess: what does the pull actually start? 👇\nFollow @whyloop.hq for a new machine every day\n#howitworks #engineering #aviation #airplane #mechanism"
first = """Answer: the pull fires a tiny striker ✈️

On many airliners, the oxygen for the drop-down masks does not come from a tank. It is made by a chemical oxygen generator: a small metal can above each seat row.

The masks hang on a cord (a lanyard). The cord is tied to a release pin in the can, and that pin holds back a spring-loaded striker. Pulling the mask toward your face yanks the pin out. Now the spring drives the striker into a small percussion cap, and the heat from the cap starts the chemical core (mostly sodium chlorate). The core then makes nearly pure oxygen for about 12 to 20 minutes, depending on the generator, and it flows through the tube to the masks. That is why the masks hang on a cord: you cannot put one on without starting the oxygen.

Good to know: in many systems one pulled mask starts the oxygen for every mask on that can. The bag may not inflate even when oxygen is flowing, and many masks have a small flow indicator that turns green. The can gets hot, so a burning smell can be normal.

(Simplified 3D model: parts are enlarged, the pull and the striker are shown in slow motion, and the time before oxygen flows is shortened. Some aircraft use oxygen bottles instead of chemical generators.)

Sources:
FAA, Passenger Oxygen Mask Design Study (pull on the lanyard starts the flow; 12-20 min; green flow indicator): https://www.faa.gov/sites/faa.gov/files/data_research/research/med_humanfacs/oamtechreports/202111.pdf
SKYbrary, Chemical Oxygen Generators (spring-loaded firing pin, percussion cap, sodium chlorate core, heat and smell): https://skybrary.aero/articles/chemical-oxygen-generators
ATSB depressurization guide (the bag may not inflate): https://skybrary.aero/sites/default/files/bookshelf/957.pdf
Airbus Cabin Decompression Awareness (one pull starts the whole group): https://skybrary.aero/sites/default/files/bookshelf/1269.pdf"""
alt = ("3D animation of an airplane oxygen mask, with a voiceover. Under the question Why pull the mask down? a yellow oxygen mask with a clear bag hangs from an open panel in a cabin ceiling, and it is pulled down. "
       "Then the panel is shown from the side with a small oxygen can cut in half (red cut faces). 1, the cord is tied to a pin: a cord runs from the mask up to a pin in the end of the can. "
       "2, the pin holds the striker back: inside the end of the can a coiled spring pushes a steel striker, and the pin passes through the striker, so it cannot move. "
       "3, pull: the pin comes out: in slow motion the mask is pulled down, the cord goes tight and pulls the pin out. "
       "4, the spring fires the striker: the spring drives the striker into a small brass cap, which glows, and the chemical core starts to glow orange. "
       "5, the core makes oxygen: the glowing front moves along the core, blue oxygen dots flow out of the can, down the tube, the indicator turns green and the bag fills a little; 12-20 minutes. "
       "The payoff reads Pull the mask to start the oxygen, a follow line appears and the video loops.")
on = ['INSIDE IT', 'WHY PULL', 'THE MASK DOWN?', 'THE CORD IS TIED TO A PIN', 'OXYGEN CAN', 'CORD', 'PIN', 'MASK', 'THE PIN HOLDS THE STRIKER BACK', 'STRIKER', 'SPRING', "CAN'T MOVE",
      'PULL: THE PIN COMES OUT', 'PULL', 'PIN OUT', 'SLOW MOTION', 'THE SPRING FIRES THE STRIKER', 'CAP', 'CHEMICAL CORE', 'THE CORE MAKES OXYGEN', 'OXYGEN', '12-20 MINUTES', 'TO YOUR MASK',
      'PULL THE MASK', 'TO START THE OXYGEN', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
src = ['https://www.faa.gov/sites/faa.gov/files/data_research/research/med_humanfacs/oamtechreports/202111.pdf', 'https://skybrary.aero/articles/chemical-oxygen-generators',
       'https://skybrary.aero/sites/default/files/bookshelf/957.pdf', 'https://skybrary.aero/sites/default/files/bookshelf/1269.pdf']
P = dict(id='p099', track='A', group='V', slot='2026-11-26T17:00 Europe/London (planned, coordinator schedules)', topicKey='oxygen mask',
  outlier='scorecard rule: everyday-familiar object + one "why do you have to..." question; our own model, script, words and sound',
  topic="Airplane drop-down oxygen mask: the mask's lanyard is tied to a release pin in a chemical oxygen generator; pulling the mask pulls the pin, a spring-loaded striker hits a percussion cap, and the heat starts a sodium chlorate core that makes oxygen for about 12-20 minutes.",
  hook="WHY PULL / THE MASK DOWN?", title="Why Do You Have to Pull the Mask Down? ✈️",
  principle="Passenger masks hang on a lanyard tied to the release pin of a chemical oxygen generator; the pin restrains a spring-loaded firing pin (striker); pulling the mask removes the pin, the striker sets off a percussion cap whose heat starts the decomposition of the sodium chlorate core, which then releases nearly pure oxygen for about 12-20 minutes through the tubes to the masks.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo, sources=src)
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
import re
from spellchecker import SpellChecker
sp = SpellChecker(); txt = ' '.join([caption, first, alt] + on + vo)
words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z']+", re.sub(r'https?://\S+', ' ', txt)))
words = {w.strip("'") for w in words}; words = {w[:-2] if w.endswith("'s") else w for w in words}
print('spell flags:', sorted(sp.unknown(words)), 'firstComment chars', len(first))
