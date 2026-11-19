import json
caption = "Why Do a Corkscrew's Wings Go Up? 🍷\nGuess: what's hiding between the wings? 👇\nFollow @whyloop.hq for a new machine every day\n#corkscrew #howitworks #mechanism #engineering #gears"
first = """Answer: a rack and pinion 🍷

The shaft of a winged corkscrew has rings of teeth (the rack), and each wing ends in a small gear (the pinion) that meshes with those teeth.

The base sits on the bottle. When you twist the top, the screw (the "worm") winds down into the cork and pulls the shaft down through the body. The shaft's teeth turn both gears, so both wings swing up.

It works the other way too: push the wings down, the gears drive the shaft back up, and the cork comes up with the screw.

(Simplified 3D model; real corkscrews differ in detail.)

Sources:
Wikipedia, Corkscrew (winged corkscrew: as the worm is twisted into the cork, the levers are raised; pushing down the levers draws the cork; the most common design has a rack and pinion connecting the levers to the body): https://en.wikipedia.org/wiki/Corkscrew
US Patent Application 2017/0043989 (winged corkscrew: the rack portion of the shaft engages the gear teeth of the two levers; the base engages the neck of the bottle): https://patents.google.com/patent/US20170043989A1/en
L'Atelier du Vin, How to use a corkscrew (twist the handle, the wings rise as the worm enters the cork; push both wings down to pull the worm and cork up): https://www.atelierduvin.com/en/how-to-use-a-corkscrew"""
alt = ("3D animation of a chrome winged corkscrew on a green wine bottle, with a voiceover. Under the question Why do the wings go up? the wings are pushed down and the cork rises out of the neck. "
       "1, twist: the screw goes in: the top handle turns, the spiral screw winds into the cork and both wings start to rise. "
       "2, close-up of the head: rings of teeth on the shaft, highlighted gold, mesh with a small gear at the root of each wing. "
       "3, shaft sinks, wings rise: arrows show the shaft moving down, both gears turning and both wings swinging up. "
       "4, wings down, cork up: the wings are pushed down, the gears drive the shaft back up and the cork slides up out of the bottle. "
       "The payoff reads Shaft down equals wings up, wings down equals cork out, a follow line appears and the video loops.")
on = ['INSIDE IT', 'WHY DO THE', 'WINGS GO UP?', 'TWIST: THE SCREW GOES IN', 'CORK', 'WINGS RISE?', 'SHAFT TEETH + WING GEARS', 'TEETH ON THE SHAFT', 'GEAR', 'WING',
      'SHAFT SINKS → WINGS RISE', 'WINGS DOWN → CORK UP', 'CORK COMES UP', 'SHAFT DOWN = WINGS UP', 'WINGS DOWN = CORK OUT', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p079', track='A', group='E', slot='', topicKey='wing corkscrew',
  outlier='scorecard rule: hand-held everyday object + one "why" (wings rise); our own model, script, words and sound',
  topic="Winged corkscrew: rings of teeth on the shaft (rack) mesh with a gear (pinion) on each wing; the worm pulls the shaft down -> wings rise; wings pushed down -> shaft and cork rise.",
  hook="WHY DO THE / WINGS GO UP?", title="Why Do a Corkscrew's Wings Go Up? 🍷",
  principle="A winged corkscrew is a rack and pinion: the base rests on the bottle, the worm screwing into the cork pulls the toothed shaft down through the body, which turns the pinion at each wing root so the wings rise; pushing the wings down turns the pinions back and drives the shaft, worm and cork up.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://en.wikipedia.org/wiki/Corkscrew', 'https://patents.google.com/patent/US20170043989A1/en', 'https://www.atelierduvin.com/en/how-to-use-a-corkscrew'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
