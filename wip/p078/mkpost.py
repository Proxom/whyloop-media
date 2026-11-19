import json
caption = "How a Bike Pump Pushes Air One Way 🚲\nGuess: what stops the air coming back up? 👇\nFollow @whyloop.hq for a new machine every day\n#bikepump #howitworks #mechanism #engineering #cycling"
first = """Answer: a soft rubber cup on the piston (plus the tire's own valve) 🚲

A simple pump piston carries a cup-shaped seal whose open side faces down, toward the hose.

Pull the handle up: nothing presses the cup's thin edge against the wall, so outside air slips past it into the barrel.

Push the handle down: the air under the piston pushes the sides of the cup out against the barrel wall, so it seals. The trapped air has only one way out: down the hose, forcing the tire valve open.

When you pull up again, the tire valve shuts by itself, so the air in the tire can't come back. The cup works as its own one-way valve.

(Simplified 3D model, slowed down; the cup's bend and the valve movement are drawn larger than real. Real pumps differ in detail.)

Sources:
Wikipedia, Bicycle pump (a simple pump has a cupped piston; on the forward stroke the air pushes the sides of the cup against the cylinder, forming a seal, so it provides its own valve; during the up-stroke air is drawn into the pump from outside; when the handle is pulled up again the valve shuts automatically so the air cannot escape from the tire): https://en.wikipedia.org/wiki/Bicycle_pump"""
alt = ("3D animation of a red bike floor pump connected by a hose to a bicycle wheel's valve, with a voiceover. Under the question How does air go only one way? a red circle marks the soft rubber cup on the piston inside the cut-open barrel. "
       "The handle is pushed and pulled while air dots flow into the tire. 1, a soft cup on the piston: the barrel is cut open, showing the piston and a black flared rubber cup with labels rubber cup, piston and wall. "
       "2, pull, air slips past the cup: the piston rises slowly, the cup's edge bends inward away from the wall, and light blue air dots slip past it into the barrel. "
       "3, push, air presses it shut: the piston moves down, orange arrows press the cup's edge against the wall, labelled sealed, and the air dots flow down the hose to the tire. "
       "4, the tire valve shuts: a close-up of the valve on the rim, labelled shut, as the handle comes up again. "
       "The payoff reads The cup lets air in, then seals and pushes, a follow line appears and the video loops.")
on = ['INSIDE IT', 'HOW DOES AIR GO', 'ONLY ONE WAY?', 'PUSH', 'PULL', 'TIRE', 'A SOFT CUP ON THE PISTON', 'RUBBER CUP', 'PISTON', 'WALL', 'PULL: AIR SLIPS PAST THE CUP', 'EDGE BENDS IN', 'AIR SLIPS PAST',
      'PUSH: AIR PRESSES IT SHUT', 'SEALED', 'AIR → TIRE', 'THE TIRE VALVE SHUTS', 'TIRE VALVE', 'SHUT', 'THE CUP LETS AIR IN', 'THEN SEALS AND PUSHES', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p078', track='A', group='E', slot='', topicKey='bike pump',
  outlier='hand-held everyday object + one-way question (scorecard: daily objects with a one-way / click mystery win); our own model, script, words and sound',
  topic="Bike floor pump: the cup seal on the piston bends in on the up-stroke (air slips past) and seals against the wall on the down-stroke; the tire valve stops backflow.",
  hook="HOW DOES AIR GO / ONLY ONE WAY?", title="How a Bike Pump Pushes Air One Way 🚲",
  principle="A cup seal opening toward the outlet is pressed against the cylinder wall by the compressed air on the down-stroke (seals) and lets air slip past on the up-stroke; the tire valve opens under pressure and shuts on the up-stroke.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo, sources=['https://en.wikipedia.org/wiki/Bicycle_pump'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
