import json
caption = "How One Cable Squeezes Both Sides 🚲\nGuess: what pushes the left arm? 👇\nFollow @whyloop.hq for a new machine every day\n#bike #howitworks #mechanism #engineering #cycling"
first = """Answer: the cable's own outer casing 🔧

This is a V-brake (a linear-pull rim brake). Two arms pivot on the fork, one on each side of the rim, each with a rubber pad.

The cable comes down inside an outer casing (the housing). The casing ends at a bent metal guide (the "noodle") on the left arm, and the inner cable runs across to the right arm.

Squeeze the lever: the inner cable slides into the casing and pulls the right arm in, and the casing pushes back on the left arm just as hard, so it moves in too. The gap between the two arm tops gets shorter, like a drawstring. Both pads close on the rim at once.

The arms are long and the pads sit lower, closer to the pivots, so the cable moves more than the pads do and the pads squeeze harder than the cable pulls: in this model about 2 times harder, and the cable moves about 22 mm while each pad moves 6 mm. Friction between the pads and the rim slows the wheel.

(Simplified 3D model, slowed down and not to scale; the gap between the pads and the rim is drawn bigger than on a real bike.)

Sources:
Wikipedia, Bicycle brake (V-brakes: the cable housing is attached to one arm and the cable to the other; as the cable pulls against the housing, the arms are drawn together; the housing is extended by a rigid tube with a 90° bend, the noodle; the arms move the same distance as the cable moves relative to its housing, hence "linear-pull"; V-brakes have a higher mechanical advantage and need brake levers with longer cable travel; brakes press surfaces together to turn the bike's motion into heat by friction): https://en.wikipedia.org/wiki/Bicycle_brake
Wikipedia, Lever (the mechanical advantage of a lever is the ratio of the distances from the pivot to where the forces act): https://en.wikipedia.org/wiki/Lever"""
alt = ("3D animation of the front of a bike with a blue fork and a V-brake, with a voiceover. Under the question How does one cable squeeze both sides? a red circle marks a brake pad next to the spinning rim. "
       "The whole front of the bike: the brake lever is squeezed, the cable pulls and the wheel stops. A front close-up with the front of the wheel cut away names the two arms, the two pads and the rim. "
       "1, cable pulls, casing pushes: the inner cable and the outer casing are named; yellow marks on the inner cable slide into the casing, an arrow shows the cable pulling the right arm in, another shows the casing pushing the left arm in, and a live readout shows the gap between the arm tops getting shorter. 2, both pads hit the rim at the same time. "
       "3, long arms, hard squeeze: the pivots are marked, a long yellow line runs from the pivot to the cable and a short blue line from the pivot to the pad, the squeeze is about 2 times the pull, and live readouts show the cable moving about 22 mm while each pad moves 6 mm; then friction stops the wheel. A badge in the corner shows the wheel spinning or stopped. "
       "The payoff reads One pull, two arms, both sides squeezed, a follow line appears and the video loops.")
on = ['INSIDE IT', 'HOW DOES ONE CABLE', 'SQUEEZE BOTH SIDES?', 'BRAKE LEVER', 'CABLE', 'BRAKE', 'ARM', 'PAD', 'RIM', 'WHEEL:', 'SPIN', 'STOP',
      'TIRE (CUT OPEN)', 'CABLE PULLS, CASING PUSHES', 'OUTER CASING', 'INNER CABLE', 'INNER CABLE PULLS', 'CASING PUSHES', 'GAP: 66 MM', 'PIVOT', 'SQUEEZE ≈ 2× THE PULL', 'BOTH PADS HIT THE RIM', 'SQUEEZE!', 'LONG ARMS: HARD SQUEEZE', 'CABLE: 22 MM', 'EACH PAD: 6 MM', 'FRICTION STOPS THE WHEEL',
      'ONE PULL, TWO ARMS', 'BOTH SIDES SQUEEZED', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p073', track='A', group='V', slot='2026-11-20T17:00 Europe/London', topicKey='bike v-brake',
  outlier='group V (one tiny mechanism in a bike), hand-operated + squeeze; our own model, script, words and sound',
  topic='Bicycle V-brake (linear-pull rim brake): how one cable closes both arms at once.',
  hook='HOW DOES ONE CABLE / SQUEEZE BOTH SIDES?', title='How One Cable Squeezes Both Sides 🚲',
  principle='The inner cable is fixed to one arm and its housing (via the noodle) bears on the other arm; pulling the cable against the housing draws the two arm tops together, each arm pivots on its boss and its pad, closer to the pivot than the cable, presses the rim with a force multiplied by the arm-length ratio.',
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://en.wikipedia.org/wiki/Bicycle_brake', 'https://en.wikipedia.org/wiki/Lever'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
