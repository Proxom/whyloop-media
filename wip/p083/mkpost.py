import json
caption = "Why Does This Cap Just Click? 💊\nGuess: what's hiding under the outer cap? 👇\nFollow @whyloop.hq for a new machine every day\n#howitworks #mechanism #engineering #childproof #design"
first = """Answer: a second cap 💊

A push-and-turn child-resistant cap is really two caps. The inner cap is the one screwed onto the bottle. The outer cap sits loosely over it.

Between their tops are ring-shaped, sloped (saw-tooth) teeth. Turn the outer cap to open without pushing, and its teeth just ride up the slopes and slip over them, click after click, so no turning force reaches the inner cap.

Push down while you turn, and the teeth can't ride up anymore. Now they grip, and the outer cap drives the inner cap off the thread.

Closing is easy: in that direction the steep faces of the teeth lock, so both caps turn together without a push.

(Simplified 3D model: the teeth are drawn bigger and the outer cap is cut open so you can see inside. Real caps differ in detail.)

Sources:
US patent 11104494 B2, child-resistant closure (inner cap with saw-tooth teeth; turning to open without a downward force makes the outer cap's abutments ride over the sloped surfaces with no torque passed on; with a downward force they engage and turn the inner cap; when closing, the vertical faces engage): https://patents.google.com/patent/US11104494B2/en
US patent 11279530 B2, child-resistant cap (inner cap carries the thread, held inside an outer cap so it can turn freely; one-way ratchet ramps lock when screwing on and slip in the opposite direction): https://patents.google.com/patent/US11279530B2/en
US EPA, child-resistant screw cap (two-piece closure, opened by pushing down and turning counterclockwise): https://www.epa.gov/sites/default/files/2014-03/documents/sannerchildresistantscrewcap.pdf"""
alt = ("3D animation of an amber medicine bottle with a white push-and-turn cap, with a voiceover. Under the question Why does it just click? the white cap turns on its own while the bottle stays still. "
       "1, two caps: the white outer cap lifts off and shows a blue inner cap screwed onto the bottle, with sloped teeth on its top. "
       "2, turn: the teeth slip: the outer cap is cut open, and a flat diagram of the two rows of saw teeth shows the white outer teeth riding up the blue slopes and dropping off, click after click. "
       "3, the inner cap stays still: the yellow mark on the blue inner cap does not move. "
       "4, push and turn: they grip: an arrow pushes the cap down, the teeth stay locked, both caps turn together and the cap rises off the threaded neck. "
       "The payoff reads Turn alone: it slips. Push and turn: it opens. A follow line appears and the video loops.")
on = ['INSIDE IT', 'WHY DOES IT', 'JUST CLICK?', 'TWO CAPS: INNER + OUTER', 'OUTER CAP: LOOSE', 'INNER CAP: SCREWED ON', 'SLOPED TEETH', 'TURN: THE TEETH SLIP', 'OUTER CAP', 'INNER CAP', 'TURN', 'CLICK',
      'THE INNER CAP STAYS STILL', 'NOT MOVING', 'PUSH + TURN: THEY GRIP', 'PUSH', 'TURN ALONE: IT SLIPS', 'PUSH + TURN: IT OPENS', 'FOLLOW → A NEW MACHINE EVERY DAY', 'PUSH DOWN & TURN (embossed on the cap)']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p083', track='A', group='E', slot='', topicKey='child-proof cap',
  outlier='scorecard rule: hand-held everyday object + "why does it click / only one way" question; our own model, script, words and sound',
  topic="Push-and-turn child-resistant cap: an inner cap screwed on the bottle and a loose outer cap with saw-tooth teeth between them; turning to open without pushing makes the teeth ride over the slopes (click), pushing down keeps them engaged so the outer cap turns the inner cap.",
  hook="WHY DOES IT / JUST CLICK?", title="Why Does This Cap Just Click? 💊",
  principle="A push-and-turn closure is an inner threaded cap inside a free outer cap; one-way saw-tooth ramps between their tops lock on their steep faces in the closing direction, but in the opening direction the outer ramps ride up the slopes and slip unless a downward force keeps them seated, so only push + turn passes torque to the inner cap.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://patents.google.com/patent/US11104494B2/en', 'https://patents.google.com/patent/US11279530B2/en', 'https://www.epa.gov/sites/default/files/2014-03/documents/sannerchildresistantscrewcap.pdf'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
