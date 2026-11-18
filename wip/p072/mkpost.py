import json
caption = "How Does a Toilet Know It's Full? 🚽\nGuess: what turns the water off? 👇\nFollow @whyloop.hq for a new machine every day\n#toilet #howitworks #mechanism #engineering #satisfying"
first = """Answer: a floating ball on a lever 🔧

This is a classic ball-float valve (a ballcock). A hollow ball floats on the water in the tank. It sits on the end of a long arm, and the arm turns on a pivot next to the valve that lets water in.

Flush: the water drops and the ball drops with it. The arm tips, its short end pulls the piston back, and the rubber washer comes off the inlet hole, so water rushes in.

As the tank fills, the water lifts the ball. The arm turns the other way and its short end pushes the piston toward the hole.

The arm is a lever: in this model the long arm is about 10 times longer than the short arm, so the push on the washer is about 10 times the lift of the ball. The washer presses on the hole and the water stops.

(Simplified 3D model, slowed down and not to scale.)

Sources:
Wikipedia, Ballcock (a valve connected to a hollow, sealed float by a lever near the top of the tank; when the water rises the float rises with it, and at a set level the lever forces the valve closed; the buoyancy force on the float is passed through the arm about the pivot to the piston, pressing the washer against the valve seat; when the water falls, the float falls and the arm slides the piston away from the inlet): https://en.wikipedia.org/wiki/Ballcock
Wikipedia, Lever (the ideal mechanical advantage of a lever is the ratio of the distances from the pivot to where the forces act): https://en.wikipedia.org/wiki/Lever"""
alt = ("3D animation of a white toilet tank, with a voiceover. Under the question How does a toilet know it's full? a red circle marks a copper float ball as the water stops. "
       "The flush lever is pressed, the front of the tank is cut away and the water drops, and the float ball drops with it. The parts are named: the float ball, the long arm, the valve and the water inlet. "
       "1, ball down: the valve opens. A close-up shows the orange piston and black rubber washer pulled back from the inlet hole, and water pours into the tank. "
       "2, the water lifts the ball, shown by an arrow under it. 3, long arm, strong push: the long arm is drawn in yellow and the short arm in blue; a small lift at the ball becomes a strong push on the piston, "
       "and the washer seals the hole. A badge in the corner shows Water in: on or off. The payoff reads The floating ball turns the water off, a follow line appears and the video loops.")
on = ['INSIDE IT', 'HOW DOES A TOILET', "KNOW IT'S FULL?", 'FLUSH', 'WATER DROPS', 'FLOAT BALL', 'LONG ARM', 'VALVE', 'WATER IN', 'WATER', 'IN:', 'ON', 'OFF',
      'BALL DOWN: VALVE OPENS', 'HOLE OPEN', 'WATER RUSHES IN', 'WATER LIFTS THE BALL', 'WATER PUSHES UP', 'LONG ARM: STRONG PUSH', 'GENTLE LIFT', 'SHORT ARM', 'STRONG PUSH', 'HOLE SEALED',
      'THE FLOATING BALL', 'TURNS THE WATER OFF', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p072', track='A', group='E', slot='2026-11-20T01:00 Europe/London', topicKey='toilet fill valve',
  outlier='scorecard list #10 (everyday object + "how does it know/stop"); our own model, script, words and sound',
  topic='Toilet tank ball-float valve (ballcock): how the tank knows it is full and turns the water off.',
  hook="HOW DOES A TOILET / KNOW IT'S FULL?", title="How Does a Toilet Know It's Full? 🚽",
  principle='A hollow float on a long lever arm rides the water level; when the water is low the arm pulls the valve piston back from the inlet seat, and as the water rises the buoyancy lifts the float and the short end of the arm pushes the piston washer onto the seat with a force multiplied by the arm-length ratio, closing the inlet.',
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://en.wikipedia.org/wiki/Ballcock', 'https://en.wikipedia.org/wiki/Lever'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
