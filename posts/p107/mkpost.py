import json
caption = "How Does a Hose Connector Click On? 💦\nGuess: what holds it on, a magnet or claws? 👇\nFollow @whyloop.hq for a new machine every day\n#howitworks #garden #engineering #mechanism #satisfying"
first = """Answer: springy claws 🪝

A snap-on garden hose connector has two halves. The plug (the male part) is screwed onto the tap or the tool. It has a groove around it and an O-ring that seals the water in. The connector (the female part) sits on the hose.

Inside the connector are a few springy plastic claws (fingers). Push the connector onto the plug, and the plug's rounded nose pushes the claws outward. When the plug is all the way in, its groove lines up with the claws, and they spring back inward into the groove. That's the click. Now the claws are hooked behind the edge of the groove, so pulling on the hose can't pull it off.

To let go, pull back the spring-loaded collar (the sleeve). It moves the claws out of the groove, and the plug slides out. Let go, and the spring pushes the collar back.

Brass quick connectors often use small steel balls or pins instead of plastic claws, but the idea is the same: something springs into a groove, and a sliding sleeve frees it.

(Simplified 3D model, slowed down and not to scale; the way the collar opens the claws differs between brands.)

Sources:
LSU AgCenter, Quick Connectors for Garden Hose (push one part into the other until it snaps; release by pulling back the collar or pushing two buttons): https://www.lsuagcenter.com/topics/lawn_garden/ornamentals/equipment/irrigation/quick-connectors-for-garden-hose
Garden hose connectors patent application (quick-connect system: the male part carries an O-ring seal; the female part has engaging fingers that move resiliently; as the male part goes in, the fingers are driven back, and they return once the parts are fully engaged; a spring-loaded sleeve retracts the fingers to release): https://trea.com/information/garden-hose-connectors/patentapplication/7833a37d-6c8a-4a32-8c6d-88a7a429831e
US 2005/0067837 A1, Quick disconnect hose coupling (background: radially moving balls and a spring-biased sleeve that is pulled back to release): https://patents.google.com/patent/US20050067837A1/en"""
alt = ("3D animation of a snap-on garden hose connector, with a voiceover. A brass garden tap on a red brick wall has a grey plug screwed on; an orange connector on a green hose is pushed up onto it and clicks, under the question How does it click on? with a red circle on the grey collar. "
       "The connector and its collar are cut open with red cut faces. 1, push it on: the connector rises toward the plug, labelled Plug on the tap, Connector and Springy claws: dark claws inside the orange body. "
       "2, the nose pushes the claws out: the plug's rounded nose slides in and the claws, glowing blue, bend outward. "
       "3, the groove lines up, they snap in: the claws spring into a groove around the plug with a click; the hose is tugged and green rings mark where the hooks catch on the edge of the groove, labelled Pull: hooks catch, it holds. "
       "4, pull the collar, claws open: the grey collar slides down, its inner tube glows yellow and pushes the blue claws outward, out of the groove, and the connector slides off, labelled Plug is free. "
       "The payoff reads Springy claws snap into the groove, the view pulls back to the tap, a follow line appears and the video loops.")
on = ['INSIDE IT', 'HOW DOES IT', 'CLICK ON?', 'PUSH IT ON', 'PLUG (ON THE TAP)', 'CONNECTOR', 'SPRINGY CLAWS', 'THE NOSE PUSHES THE CLAWS OUT', 'ROUND NOSE', 'CLAWS BEND OUT',
      'GROOVE LINES UP: THEY SNAP IN', 'GROOVE', 'CLICK: CLAWS IN THE GROOVE', 'PULL: HOOKS CATCH, IT HOLDS', 'PULL THE COLLAR: CLAWS OPEN', 'COLLAR', 'ITS TUBE PUSHES THE CLAWS OPEN', 'PLUG IS FREE',
      'SPRINGY CLAWS', 'SNAP INTO THE GROOVE', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p107', track='A', group='E', slot='2026-11-27T17:00 Europe/London (planned, coordinator schedules; replaces p104 flask / p106 pressure cooker, both visual 4)', topicKey='hose quick connector',
  topicKeyLine='topic key: hose quick connector (synonyms: hose quick coupling, snap-on hose connector, click-lock hose fitting) - not in learnings/topics-used.md (coordinator checked 95 rows; p032 Oldham shaft coupling unrelated)',
  outlier='scorecard rule: everyday object you touch + "why does it click / lock" question; our own model, script, words and sound',
  topic='Snap-on garden hose connector: springy claws in the female connector are pushed out by the plug nose and spring back into the plug groove (click, locked); pulling the spring-loaded collar frees them.',
  hook='HOW DOES IT / CLICK ON?', title='How Does a Hose Connector Click On? 💦',
  principle='Resilient latch fingers in the female coupling deflect outward over the male plug nose and snap back into its circumferential groove when fully inserted, so an axial pull is blocked by the groove shoulder; retracting the spring-loaded sleeve moves the fingers out of the groove to release.',
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://www.lsuagcenter.com/topics/lawn_garden/ornamentals/equipment/irrigation/quick-connectors-for-garden-hose', 'https://trea.com/information/garden-hose-connectors/patentapplication/7833a37d-6c8a-4a32-8c6d-88a7a429831e',
           'https://patents.google.com/patent/US20050067837A1/en', 'https://www.eleyhosereels.com/products/garden-hose-quick-connectors', 'https://kindseed.com/hose-quick-connect-fittings'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
import re
from spellchecker import SpellChecker
sp = SpellChecker(); txt = ' '.join([caption, first, alt] + on + vo)
words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z']+", re.sub(r'https?://\S+', ' ', txt)))
words = {w.strip("'") for w in words}; words = {w[:-2] if w.endswith("'s") else w for w in words}
print('spell flags:', sorted(sp.unknown(words)), '| first comment chars', len(first))
