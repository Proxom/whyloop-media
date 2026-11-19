import json
caption = "Why a Tiny Clipper Cuts So Hard ✂️\nGuess: how many levers are inside? 👇\nFollow @whyloop.hq for a new machine every day\n#howitworks #mechanism #engineering #physics #lever"
first = """Answer: two levers, stacked ✂️

A nail clipper is a compound lever: the output of one lever is the input of the next.

Lever 1 is the top lever. It turns on the top of the pin. Your thumb pushes far from that pivot and the lever presses the top jaw close to it, so the push on the jaw is much bigger than your push. In this model (the same proportions as the Wikipedia diagram) it is 8 times bigger.

Lever 2 is the top jaw itself. It bends at the back joint. The push lands a bit closer to that joint than the blades are, so the blades get a little less: 8 x 6/8 = 6 times your thumb force.

The two sharp edges meet and cut the nail.

(Simplified 3D model, slowed down; the jaw gap is drawn a little bigger than on a real clipper.)

Sources:
Wikipedia, Compound lever (the output of one lever becomes the input for the next, so the advantage is magnified; nail clipper example: a class 2 and a class 3 lever, W/F = (7+1)/1 x 6/(6+2) = 6): https://en.wikipedia.org/wiki/Compound_lever
Wikipedia, Nail clipper (two common types: pliers type and compound lever type): https://en.wikipedia.org/wiki/Nail_clipper"""
alt = ("3D animation of a steel nail clipper seen from the side, with a voiceover. Under the question Why does a tiny clipper cut so hard? a red circle marks the blades closing on a fingernail. "
       "The lever is pressed and the jaws snap shut. 1, two levers, stacked: lever 1 is the top lever and lever 2 is the top jaw. "
       "2, lever 1 gives 8 times the push: its pivot is the top of the pin, a long yellow line runs from the pivot to the thumb and a short blue line from the pivot to where the lever presses the jaw; a small arrow shows the thumb and a big arrow shows 8 times the push. "
       "3, lever 2 gives the blades 6 times: the top jaw pivots at the back joint; the push is a bit closer to that pivot than the blades, so the blades get 6 times your thumb. "
       "4, the blades meet and snip the end of the nail, which drops away. The payoff reads Two levers, 6X the force, a follow line appears and the video loops.")
on = ['INSIDE IT', 'WHY DOES A TINY CLIPPER', 'CUT SO HARD?', 'BLADES', 'LEVER', 'JAWS', 'TWO LEVERS, STACKED', 'LEVER 1', 'LEVER 2 (TOP JAW)',
      'LEVER 1: 8X THE PUSH', 'PIVOT (PIN)', 'LONG', 'SHORT', 'THUMB', '8X THE PUSH', 'LEVER 2: BLADES GET 6X', 'PIVOT', 'PUSH', '6X YOUR THUMB',
      'THE BLADES MEET', 'SNIP!', 'TWO LEVERS', '6X THE FORCE', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p074', track='A', group='E', slot='', topicKey='nail clipper',
  outlier='scorecard list #9 (nail clipper: lever + click; hand-held everyday object); our own model, script, words and sound',
  topic='Nail clipper as a compound lever: why a tiny clipper cuts so hard.',
  hook='WHY DOES A TINY CLIPPER / CUT SO HARD?', title='Why a Tiny Clipper Cuts So Hard ✂️',
  principle='Compound lever: the top lever (class 2, fulcrum on the pin top) multiplies the thumb force by effort arm / load arm = 8; that force bends the upper jaw (class 3, fulcrum at the rear joint), which passes on 6/8 of it to the blades: 8 x 0.75 = 6 times the thumb force.',
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://en.wikipedia.org/wiki/Compound_lever', 'https://en.wikipedia.org/wiki/Nail_clipper'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
