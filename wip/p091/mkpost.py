import json
caption = "Why Doesn't the Blind Fall? 🪟\nGuess: what grabs the cord when you let go? 👇\nFollow @whyloop.hq for a new machine every day\n#howitworks #engineering #mechanism #blinds #satisfying"
first = """Answer: a tiny toothed roller that wedges itself 🪟

Inside the top rail (the headrail) of a corded blind there is a small cord lock. The lift cords run over a smooth guide, then between that guide and a small toothed (serrated) roller. The roller is not fixed: its axle sits loose in a slanted slot.

Pull the cord down, and the cord drags the roller down to the bottom of the slot. Down there the gap is wide, so the cord runs freely and the blind goes up.

Let go, and the blind's weight pulls the cord back up through the lock. The cord grips the toothed roller and drags it up the slanted slot. Higher up the slot the gap is narrower, so the roller ends up squeezing the cord against the guide. The cord is pinched and stops, and the blind stays where it is.

To lower the blind, pull the cord toward the middle of the window. The cord then runs away from the roller, the roller drops to the wide end, and the cord can slide back up.

(Simplified 3D model; real cord locks differ in shape and size.)

Sources:
US Patent 4,180,118, Cord lock mechanism for venetian blind (cord gripped between a guide and a serrated locking pin that moves in slots; pulling down drops the pin away, the blind's weight pulls the cord up and moves the pin into the gripping position): https://patents.justia.com/patent/4180118
US Patent 6,899,156, Headrail with reversible cord lock position (toothed roller in a chamber that is wider at the bottom; as the roller moves up the gap gets smaller until the cords are squeezed and locked; pulling the cords moves the roller down and opens the gap): https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6899156
US Patent 4,955,420, Cord locking mechanism (knurled roller drawn up its slots until the cords are pinched against a fixed gripping pin; to release, the cords are angled and pulled down and the roller drops to the bottom of its channels): https://patents.justia.com/patent/4955420
Direct Online Blinds, Wood Venetian operating guide (to lower, pull the cord toward the center of the blind until the cord lock releases): https://directonlineblinds.com.au/images/uploads/images/Wood_Venetian.pdf"""
alt = ("3D animation of a window blind cord lock, with a voiceover. Under the question Why doesn't the blind fall? a white venetian blind in a window rises as its cord is pulled, then stops and stays when the cord is let go. "
       "Then the cord lock inside the top rail is shown cut open from the side: the cord runs over a smooth guide and past a brass toothed roller that sits in a slanted slot. "
       "1, the cord passes a toothed roller. 2, pull: the cord rolls the roller down the slot and the gap opens, so the cord runs free and a small blind icon shows the blind going up. "
       "3, let go: the blind's weight pulls the cord back up. 4, in slow motion the cord rolls the roller up the slot, the gap closes and the cord is pinched, so it stops. "
       "5, to lower: the cord is pulled toward the middle, misses the roller and slides back up while the blind goes down. The payoff reads A tiny rolling wedge holds the blind, a follow line appears and the video loops.")
on = ['INSIDE IT', "WHY DOESN'T", 'THE BLIND FALL?', 'CORD PASSES A TOOTHED ROLLER', 'TOOTHED ROLLER', 'GUIDE', 'CORD', 'SLANTED SLOT', 'BLIND',
      'PULL: ROLLER DROPS, GAP OPENS', 'WIDE GAP', 'PULL', 'LET GO: WEIGHT PULLS CORD UP', "BLIND'S WEIGHT", 'ROLLER CLIMBS: GAP CLOSES', 'SLOW MOTION', 'PINCHED',
      'TO LOWER: PULL TOWARD THE MIDDLE', 'MISSES THE ROLLER', 'A TINY ROLLING WEDGE', 'HOLDS THE BLIND', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
src = ['https://patents.justia.com/patent/4180118', 'https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/6899156', 'https://patents.justia.com/patent/4955420', 'https://directonlineblinds.com.au/images/uploads/images/Wood_Venetian.pdf']
P = dict(id='p091', track='A', group='E', slot='2026-11-22T21:00:00 Europe/London (planned)', topicKey='blind cord lock',
  outlier='scorecard rule: everyday object you touch + one "why does it lock"; our own model, script, words and sound',
  topic="Venetian blind cord lock: a toothed roller in a slanted slot; the blind's weight pulls the cord up, the cord rolls the roller up the slot until the narrowing gap pinches the cord against the guide.",
  hook="WHY DOESN'T / THE BLIND FALL?", title="Why Doesn't the Blind Fall? 🪟",
  principle="In a blind's cord lock the cord passes between a fixed guide and a serrated roller that floats in a slanted slot; when released, the blind's weight pulls the cord up, which rolls the roller up the slot into the narrowing gap until the cord is wedged between roller and guide; pulling down (or toward the middle) drops the roller to the wide end and frees the cord.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo, sources=src)
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
import re
from spellchecker import SpellChecker
sp = SpellChecker(); txt = ' '.join([caption, first, alt] + on + vo)
words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z']+", re.sub(r'https?://\S+', ' ', txt)))
words = {w.strip("'") for w in words}; words = {w[:-2] if w.endswith("'s") else w for w in words}
print('spell flags:', sorted(sp.unknown(words)))
