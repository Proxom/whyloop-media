import json
caption = "How Does a Sharpener Make a Perfect Point? ✏️\nGuess: what shape is the hole inside? 👇\nFollow @whyloop.hq for a new machine every day\n#pencil #howitworks #mechanism #engineering #school"
first = """Answer: a cone ✏️

A small pocket ("prism") sharpener has a round guide hole that keeps the pencil straight, and below it a hole shaped like a cone. A sharp blade is screwed on the side so that its edge just touches the cone.

Twist the pencil, and the blade shaves a thin strip of wood off the part that sticks out past the cone. The shaving comes out through a slot along the blade.

The pencil can only slide deeper once its wood fits inside the cone, so turn after turn the wood takes the cone's exact shape, and the lead in the middle ends up at the tip. That's why the point always comes out at the cone's angle.

(Simplified 3D model; the body is drawn clear so you can see inside. Real sharpeners differ in detail.)

Sources:
Wikipedia, Pencil sharpener (prism sharpeners: a point-shaping cone aligned to the cylindrical guide hole; a blade mounted so its edge just enters the cone tangentially; the pencil is rotated while the sharpener is held still; shavings emerge through a slot along the blade edge): https://en.wikipedia.org/wiki/Pencil_sharpener"""
alt = ("3D animation of a yellow pencil in a clear blue pocket sharpener, with a voiceover. Under the question How does it make a perfect point? a freshly sharpened pencil point rises out of the sharpener. "
       "1, a cone-shaped hole and a blade: the clear body shows a hole that narrows to a cone, and a steel blade on the side lights up. "
       "2, twist: the blade shaves wood: the blunt pencil turns and a fan-shaped wood shaving with a yellow edge curls out next to the blade. "
       "3, it only goes deeper once it fits: an arrow pushes down while the pencil end inside the cone is still too wide. "
       "4, the wood becomes the cone: turn after turn the pencil slides deeper until its end matches the cone, with the dark lead at the very tip. "
       "The payoff reads The hole is a cone, the blade shaves to fit, a follow line appears and the video loops.")
on = ['INSIDE IT', 'HOW DOES IT MAKE', 'A PERFECT POINT?', 'A CONE-SHAPED HOLE + A BLADE', 'CONE', 'BLADE', 'TWIST: THE BLADE SHAVES WOOD', 'SHAVING', 'IT ONLY GOES DEEPER ONCE IT FITS', 'STILL TOO WIDE',
      'THE WOOD BECOMES THE CONE', 'LEAD AT THE TIP', 'THE HOLE IS A CONE', 'THE BLADE SHAVES TO FIT', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p081', track='A', group='E', slot='', topicKey='pencil sharpener',
  outlier='scorecard rule: hand-held everyday object + one "why"; our own model, script, words and sound',
  topic="Prism pencil sharpener: the blade's edge lies on a cone-shaped hole; turning the pencil shaves off whatever sticks out past the cone, so the pencil can only go deeper as it takes the cone's shape.",
  hook="HOW DOES IT MAKE / A PERFECT POINT?", title="How Does a Sharpener Make a Perfect Point? ✏️",
  principle="In a prism sharpener the guide hole holds the pencil on the axis of a shaping cone whose side is touched tangentially by the blade edge; rotating the pencil makes the blade shave any wood outside the cone, and the pencil advances only as its end is cut to the cone, so the point always takes the cone's angle with the lead at the apex.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://en.wikipedia.org/wiki/Pencil_sharpener'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
