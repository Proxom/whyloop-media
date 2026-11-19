import json
caption = "How Does a Can Opener Cut the Lid? 🥫\nGuess: does the opener move, or the can? 👇\nFollow @whyloop.hq for a new machine every day\n#canopener #howitworks #mechanism #engineering #kitchen"
first = """Answer: the can moves 🥫

A hand can opener has two wheels that pinch the can's rim between them.

Squeeze the handles, and the sharp cutting wheel on top punches through the lid, just inside the rim. Under the rim sits a small wheel with teeth (the traction or feed wheel), fixed to the key.

Turn the key, and those teeth grip the rim and drag the can around. The blade stays in one place and rolls along, so the cut runs all the way around the lid until it comes free.

(Simplified 3D model of a top-cutting opener; real openers differ in detail, and side-cut "safety" openers cut in a different place.)

Sources:
Sciencing, Mechanism Description of a Manual Can Opener (traction gear beneath the lip, cutting wheel above it; turning the crank turns the traction gear and propels the cutting wheel around the rim): https://www.sciencing.com/mechanism-description-of-a-manual-can-opener-12587926
The Home Depot, How to Use a Can Opener (squeeze the arms and the cutting wheel punctures the lid; as the knob turns, the feed wheel grips the lip, the opener cuts through the lid and the can rotates): https://www.homedepot.com/c/ah/how-to-use-a-can-opener/9ba683603be9fa5395fab90152074b28
US Patent 6,058,613, background (first type of opener: the traction wheel engages the under surface of the rim; the cutter blade cuts through the end slightly inward of the rim, so the end comes off after one full turn of the can): https://patents.google.com/patent/US6058613A/en"""
alt = ("3D animation of a steel hand can opener on a red tomato can, with a voiceover. Under the question How does it cut the lid? the can turns, the cut closes and the lid drops free. "
       "1, squeeze: the blade punches in: the handles close and a sharp wheel pushes through the lid just inside the rim. "
       "2, a close-up from below shows a small toothed wheel, highlighted gold, pressed under the can's rim. "
       "3, turn: the teeth drag the can: the black key turns, the toothed wheel turns and the whole can rotates. "
       "4, the blade stays, the cut goes round: from above, an orange cut line grows all the way around the lid while the blade stays in one place. "
       "The payoff reads One wheel pulls the can, one wheel cuts, a follow line appears and the video loops.")
on = ['INSIDE IT', 'HOW DOES IT', 'CUT THE LID?', 'SQUEEZE: THE BLADE PUNCHES IN', 'BLADE', 'PUNCHED THROUGH', 'A TOOTHED WHEEL UNDER THE RIM', 'TEETH', 'RIM',
      'TURN: THE TEETH DRAG THE CAN', 'CAN TURNS', 'THE BLADE STAYS, THE CUT GOES ROUND', 'BLADE STAYS HERE', 'CUT', 'ONE WHEEL PULLS THE CAN', 'ONE WHEEL CUTS', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p080', track='A', group='E', slot='', topicKey='can opener',
  outlier='scorecard rule: hand-held everyday object + one "why"; our own model, script, words and sound',
  topic="Hand can opener: squeezing pushes the cutting wheel through the lid; the key turns a toothed traction wheel under the rim that drags the can around past the fixed blade.",
  hook="HOW DOES IT / CUT THE LID?", title="How Does a Can Opener Cut the Lid? 🥫",
  principle="The handles clamp the can's rim between a sharp cutting wheel above (which pierces the lid just inside the rim) and a toothed traction wheel below; turning the key spins the traction wheel, whose teeth grip the rim and rotate the can, so the lid slides past the stationary, free-rolling cutting wheel and is cut all the way around.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://www.sciencing.com/mechanism-description-of-a-manual-can-opener-12587926', 'https://www.homedepot.com/c/ah/how-to-use-a-can-opener/9ba683603be9fa5395fab90152074b28', 'https://patents.google.com/patent/US6058613A/en'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
