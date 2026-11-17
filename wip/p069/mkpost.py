import json
caption = "How a Clutch Works 🚗\nGuess: what squeezes the disc onto the engine? 👇\nFollow @whyloop.hq for a new machine every day\n#clutch #howitworks #mechanism #engineering #cars"
first = """Answer: a big spring 🔧

The flywheel is bolted to the engine, so it spins whenever the engine runs. The clutch disc sits on the gearbox shaft, which leads on to the wheels.

Pedal up: the diaphragm spring pushes the pressure plate, and the plate squeezes the disc against the flywheel. Friction locks them together, so the engine turns the wheels.

Pedal down: the release bearing pushes the middle of the spring in, the pressure plate pulls back from the disc, and a gap opens. The engine keeps spinning, but the wheels no longer have to turn with it, so the car can stop without stalling.

When you lift the pedal, the disc slips for a moment before it locks. That slip is what lets a car pull away smoothly.

(Simplified 3D model, slowed down: the gearbox between the clutch and the wheels is left out, and the gap is drawn much wider than in a real clutch.)

Sources:
Wikipedia, Clutch (a friction disk presses against the engine's flywheel by a spring mechanism; the wheels are only powered when the flywheel is in contact with the friction disk; in a push-type clutch, pressing the pedal pushes the release bearing to disengage the clutch): https://en.wikipedia.org/wiki/Clutch
HowStuffWorks, What Is a Clutch? (with your foot off the pedal, springs push the pressure plate against the clutch disc, which presses against the flywheel; pressing the pedal pushes the release bearing against the middle of the diaphragm spring, which pulls the pressure plate away from the clutch disc; the engine spins all the time but the wheels do not; the clutch controls the slippage for a smooth start): https://auto.howstuffworks.com/clutch.htm"""
alt = ("3D animation of a car clutch between an engine block and a wheel, with a voiceover. Under the question How does a clutch work? a red circle marks the rim of the clutch; "
       "the pedal comes up, the plates clamp together and the wheel starts to turn. A wide view: the engine always spins, the wheels are stopped, and a small pedal icon shows the pedal down. "
       "The cover fades away and the parts are named: flywheel, clutch disc, pressure plate, spring. 1, pedal up: the spring squeezes the disc against the spinning flywheel; up close the gap closes, "
       "the disc slips and then turns with the engine, and the wheels turn: friction equals drive. 2, pedal down: the fork pushes the release bearing into the spring, the pressure plate pulls back and a gap opens; "
       "the disc is free, the engine keeps spinning and the wheel slows to a stop. The payoff reads Squeeze equals drive, gap equals stop. A follow line appears and the video loops.")
on = ['INSIDE IT', 'HOW DOES A', 'CLUTCH WORK?', 'ENGINE: ALWAYS SPINS', 'WHEELS: STOPPED', 'WHEELS: TURNING', 'UP', 'DOWN', 'FLYWHEEL', 'CLUTCH DISC', 'PRESSURE PLATE', 'SPRING',
      'PEDAL UP: SPRING SQUEEZES', 'SQUEEZED', 'LOCKED TOGETHER', 'FRICTION = DRIVE', 'PEDAL DOWN: A GAP OPENS', 'BEARING PUSHES', 'GAP: DISC IS FREE', 'SQUEEZE = DRIVE', 'GAP = STOP', 'FOLLOW → A NEW MACHINE EVERY DAY']
P = dict(id='p069', track='A', group='V', slot='2026-11-18T17:00 Europe/London', topicKey='car clutch',
  outlier='1M+ list #9: car clutch (Physics and animation, 1.8M); our own model, script, words and sound',
  topic='Car clutch (single dry plate, diaphragm spring, push-type): how the pedal lets the engine keep running while the wheels stop.',
  hook='HOW DOES A / CLUTCH WORK?', title='How a Clutch Works 🚗',
  principle='A diaphragm spring clamps the clutch disc (splined to the gearbox input shaft) between the pressure plate and the engine flywheel, so friction makes them turn together; pressing the pedal pushes the release bearing onto the spring fingers, the spring levers the pressure plate back, the disc is freed and the engine turns independently of the wheels.',
  caption=caption, firstComment=first, altText=alt, onScreen=on,
  sources=['https://en.wikipedia.org/wiki/Clutch', 'https://auto.howstuffworks.com/clutch.htm'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
