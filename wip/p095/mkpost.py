import json
caption = "What Flips the Key Out? 🔑\nGuess: what's hiding in the pivot? 👇\nFollow @whyloop.hq for a new machine every day\n#howitworks #engineering #mechanism #cars #satisfying"
first = """Answer: a wound-up spring 🔑

A flip key (a folding car key) swings on a pivot. Around that pivot sits a coiled torsion spring. When the blade is folded, the spring is wound up, so it is always trying to swing the blade out.

The button on the pivot holds it back. Under the button are two little teeth. A small spring pushes the button up, so the teeth sit in notches in the case, and the blade can't turn.

Press the button and the teeth drop out of the notches. Now nothing holds the wound spring, so it snaps the blade out until it hits a stop. Then the little spring pushes the button back up, the teeth drop into the notches again, and the blade is locked open.

To fold it, press the button and push the blade back in. That winds the spring up again, ready for next time.

(Simplified 3D model; the teeth and spring are enlarged, and the exact parts differ between car makers.)

Sources:
US Patent 7,370,501, Key unit (a torsion spring urges the key from the retracted to the projecting position; pushing in the release button frees it and it pivots out by the spring force; at the projecting position the button is pushed out by its coil spring so a projection fits into a recess and retains the key): https://patents.google.com/patent/US7370501
US Patent 8,978,429, Flip key for an automotive vehicle (the push button is held up by a spring; its legs sit in anchoring grooves of the housing; pushing the button makes the legs exit the grooves, freeing the rotating bearing of the key insert): https://patents.google.com/patent/US8978429"""
alt = ("3D animation of a folding car key, with a voiceover. Under the question What flips the key out? a black key fob sits on a dark table; a finger press on the round button at the pivot and the steel key blade snaps out. "
       "Then the pivot is shown cut in half with red cut faces. 1, a wound spring pushes the blade: a coiled spring around the pivot glows and a curved arrow shows it pushing. "
       "2, button teeth sit in notches: two small gold teeth on the button sit in notches in the case, so it is locked. "
       "3, press, teeth leave the notches: the button goes down and the teeth drop out, free. "
       "4, the spring snaps it out: seen from above in slow motion, the blade swings out until it rests on a stop. "
       "5, teeth pop back, locked open: the button rises and the teeth drop back into the notches. "
       "Finally the blade is pushed back in, winding the spring. The payoff reads A wound-up spring flips the key out, a follow line appears and the video loops.")
on = ['INSIDE IT', 'WHAT FLIPS', 'THE KEY OUT?', 'A WOUND SPRING PUSHES THE BLADE', 'WOUND SPRING', 'BLADE', 'BUTTON TEETH SIT IN NOTCHES', 'TOOTH', 'NOTCH IN THE CASE', 'LOCKED',
      'PRESS: TEETH LEAVE THE NOTCHES', 'TEETH OUT: FREE', 'THE SPRING SNAPS IT OUT', 'SLOW MOTION', 'STOP', 'TEETH POP BACK: LOCKED OPEN', 'BACK IN THE NOTCH',
      'WINDS THE SPRING', 'A WOUND-UP SPRING', 'FLIPS THE KEY OUT', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p095', track='A', group='V', slot='2026-11-21T21:00 Europe/London (planned, coordinator schedules)', topicKey='flip key',
  outlier='scorecard rule: everyday object you hold + one "what makes it snap / lock"; our own model, script, words and sound',
  topic="Flip (folding) car key: a torsion spring around the pivot is wound when the blade is folded; the button's teeth sit in notches in the case and lock it; pressing the button frees it, the spring snaps the blade out, and the teeth pop back into the notches to lock it open.",
  hook="WHAT FLIPS / THE KEY OUT?", title="What Flips the Key Out? 🔑",
  principle="A torsion spring around the pivot urges the key blade from folded to open; a spring-loaded push button on the pivot has legs that engage grooves in the housing and lock the rotating bearing; pressing the button disengages them so the spring swings the blade out, and at the open position the button returns and re-engages, retaining the blade.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://patents.google.com/patent/US7370501', 'https://patents.google.com/patent/US8978429'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
import re
from spellchecker import SpellChecker
sp = SpellChecker(); txt = ' '.join([caption, first, alt] + on + vo)
words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z']+", re.sub(r'https?://\S+', ' ', txt)))
words = {w.strip("'") for w in words}; words = {w[:-2] if w.endswith("'s") else w for w in words}
print('spell flags:', sorted(sp.unknown(words)))
