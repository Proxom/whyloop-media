import json
caption = "What Holds an Umbrella Open? ☂️\nGuess: what's hiding in the tube? 👇\nFollow @whyloop.hq for a new machine every day\n#umbrella #howitworks #mechanism #engineering #satisfying"
first = """Answer: a tiny spring catch 🔧

The ribs of the umbrella are joined to a sleeve called the runner, which slides on the shaft. Slide the runner up and the stretchers push the ribs open.

Near the top of the shaft, a small spring catch pokes out through a slit in the tube. Its lower side is slanted, so the runner pushes it into the tube on the way up.

Once the runner slides past, the spring pops the catch back out. Now the runner sits on the catch's flat top and can't slide back down, so the umbrella stays open.

To close it, press the catch into the tube and slide the runner down.

(Simplified 3D model, slowed down and not to scale. Many umbrellas also have a second catch lower down that holds them closed, and some newer designs put the catch outside the tube.)

Sources:
US Patent 8,459,281, Runner fastening device for an umbrella (a conventional umbrella has a runner that slides on the central shaft to spread and collapse the rib-and-stretcher assembly, and a spring catch in the shaft near the top notch; the runner is moved over the spring catch and is retained by it, holding the umbrella open; to close, the catch is pressed in so the runner can slide over it, and a lower spring catch holds the runner down): https://patents.google.com/patent/US8459281
US Patent 6,810,895, Umbrella having safety runner and strength-enhanced shaft tube (a conventional umbrella has the spring catch retained within the central shaft, protruding outward through a catch slit to lock the runner; pressing releases the runner to close the umbrella): https://patents.google.com/patent/US6810895"""
alt = ("3D animation of a red umbrella, with a voiceover. Under the question What holds an umbrella open? a red circle marks the spot on the shaft just under the sleeve that holds the ribs. "
       "The umbrella starts closed and a sleeve, the runner, slides up the shaft while the ribs open. The camera moves in under the canopy and the front of the shaft and the runner are cut away: "
       "a small orange spring catch pokes out of a slit in the tube, with a steel spring behind it inside. 1, push up: the runner hits the catch's slanted side and pushes it into the tube. "
       "2, it passes: the spring pops the catch back out, and the runner sits on its flat top, so it can't slide down. 3, the catch is pressed in and the runner slides down, and the umbrella closes. "
       "A small badge in the corner shows the umbrella opening, open or closed. The payoff reads A tiny spring catch holds it open, the umbrella opens again, a follow line appears and the video loops.")
on = ['INSIDE IT', 'WHAT HOLDS AN', 'UMBRELLA OPEN?', 'RUNNER', 'RIBS', 'SPRING CATCH', 'TUBE', 'SPRING', 'OPENING', 'OPEN', 'CLOSED',
      'PUSH UP: SLOPE PUSHES IT IN', 'PUSH UP', 'IN', 'IT PASSES: SPRING POPS IT OUT', 'SPRING: OUT!', "FLAT TOP: CAN'T SLIDE DOWN", 'FLAT TOP', 'BLOCKED',
      'PRESS IT IN: RUNNER SLIDES DOWN', 'PRESS', 'A TINY SPRING CATCH', 'HOLDS IT OPEN', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p071', track='A', group='E', slot='2026-11-19T01:00 Europe/London', topicKey='umbrella catch',
  outlier='scorecard list #5 (hand-held object + click/lock); our own model, script, words and sound',
  topic='Stick umbrella: what holds it open (the top spring catch under the runner).',
  hook='WHAT HOLDS AN / UMBRELLA OPEN?', title='What Holds an Umbrella Open? ☂️',
  principle='A spring catch inside the shaft pokes out through a slit; its slanted lower face lets the runner push it in on the way up, the spring pops it out once the runner has passed, and the runner then rests on its flat top, so the ribs stay spread until the catch is pressed in.',
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://patents.google.com/patent/US8459281', 'https://patents.google.com/patent/US6810895'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
