import json
caption = "Why Does This Cap Just Click? 💊\nGuess: what's hiding under the outer cap? 👇\nFollow @whyloop.hq for a new machine every day\n#howitworks #mechanism #engineering #childproof #design"
first = """Answer: a second cap 💊

A push-and-turn child-resistant cap is really two caps. The inner cap is the one screwed onto the bottle. The outer cap sits loosely over it, and a spring holds it up a little.

Between their tops are sloped (saw-tooth) teeth. Turn the outer cap to open without pushing, and its teeth ride up the slopes and slip off, click after click, so no turning force reaches the inner cap.

Push down, and the outer cap's flat lugs drop in next to the inner cap's lugs. Flat faces can't slip, so now both caps turn together and the cap comes off the thread.

Closing needs no push: in that direction the steep sides of the teeth catch, so both caps turn together.

That's why small kids can't easily open it: turning alone just slips.

(Simplified 3D model: teeth, lugs and spring are drawn bigger and the outer cap is cut open so you can see inside. Real caps differ in detail.)

Sources:
US patent 11104494 B2, child-resistant closure (saw-tooth teeth on the inner cap; turning to open without a downward force makes the outer cap ride over the sloped surfaces with no torque passed on; when closing, the vertical faces engage and both caps turn): https://patents.google.com/patent/US11104494B2/en
US patent 8857638 B2, push-and-turn child-resistant closure (driving lugs inside the outer shell and driven lugs on the inner shell stay disengaged unless the outer shell is pushed down; spring fingers slip over ramps when the outer shell is turned on its own): https://patents.google.com/patent/US8857638B2/en
US patent application 2020/0385182 A1 (elastic members between the tops push the outer cap away from the inner cap; the outer cap must be pushed down before the closure can be unscrewed): https://patents.google.com/patent/US20200385182A1/en
US patent 11279530 B2, child-resistant cap (inner threaded cap held inside an outer cap so it can turn freely; one-way ratchet ramps lock when screwing on and slip in the opposite direction): https://patents.google.com/patent/US11279530B2/en
US EPA, child-resistant screw cap (two-piece closure, opened by pushing down and turning counterclockwise): https://www.epa.gov/sites/default/files/2014-03/documents/sannerchildresistantscrewcap.pdf"""
alt = ("3D animation of an amber medicine bottle with a white push-and-turn cap, with a voiceover. Under the question Why does it just click? the white cap turns while an orange mark on it is circled. "
       "1, two caps and a spring: the white outer cap lifts off and shows a blue inner cap screwed onto the bottle, with sloped teeth, flat lugs and a small spring on top. "
       "2, turn: the teeth slip: the outer cap is cut open, and a flat diagram shows the white sloped teeth riding up the blue slopes and dropping off while the white lugs pass over the blue lugs. "
       "3, the inner cap stays still: the yellow mark on the blue inner cap does not move. "
       "4, push: flat lugs lock: an arrow pushes the cap down, the lugs drop in next to each other, both caps turn and the cap rises off the threaded neck. "
       "A card reads So kids can't easily open it. Turn alone: it slips. Push and turn: it opens. "
       "5, closing: no push needed: the cap comes back and turns the other way, and the steep sides of the teeth catch. A follow line appears and the video loops.")
on = ['INSIDE IT', 'WHY DOES IT', 'JUST CLICK?', 'TWO CAPS + A SPRING', 'OUTER CAP: LOOSE', 'INNER CAP: SCREWED ON', 'SLOPED TEETH', 'SPRING', 'TURN: THE TEETH SLIP', 'FLAT LUGS', 'OPEN',
      'THE INNER CAP STAYS STILL', 'NOT MOVING', 'PUSH: FLAT LUGS LOCK', 'PUSH', 'LUGS LOCK', "SO KIDS CAN'T EASILY OPEN IT", 'TURN ALONE: IT SLIPS', 'PUSH + TURN: IT OPENS',
      'CLOSING: NO PUSH NEEDED', 'CLOSE', 'FOLLOW → A NEW MACHINE EVERY DAY', 'PUSH DOWN & TURN (embossed on the cap)']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p083', track='A', group='E', slot='', topicKey='child-proof cap',
  outlier='scorecard rule: hand-held everyday object + "why does it click / only one way" question; our own model, script, words and sound',
  topic="Push-and-turn child-resistant cap: an inner cap screwed on the bottle and a loose, spring-held outer cap; turning to open alone makes the sloped teeth between them ride over and slip (click); pushing down drops flat drive lugs into place so the outer cap turns the inner cap; closing, the steep tooth sides catch.",
  hook="WHY DOES IT / JUST CLICK?", title="Why Does This Cap Just Click? 💊",
  principle="A push-and-turn closure is an inner threaded cap inside a free outer cap held up by a spring element; one-way saw-tooth ramps between their tops catch on their steep faces in the closing direction and ride over (slip) in the opening direction, while flat drive lugs on both caps only overlap when the outer cap is pushed down, so only push + turn passes opening torque to the inner cap.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://patents.google.com/patent/US11104494B2/en', 'https://patents.google.com/patent/US8857638B2/en', 'https://patents.google.com/patent/US20200385182A1/en', 'https://patents.google.com/patent/US11279530B2/en', 'https://www.epa.gov/sites/default/files/2014-03/documents/sannerchildresistantscrewcap.pdf'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
