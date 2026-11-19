import json
caption = "How a Kettle Knows It's Boiling ☕\nGuess: what flips the switch? 👇\nFollow @whyloop.hq for a new machine every day\n#kettle #howitworks #mechanism #engineering #physics"
first = """Answer: a strip made of two metals, bent by the steam 🔥

When the water boils it makes a lot of steam. A tube carries some of that steam down to the switch at the bottom of the handle.

There the steam heats a bimetallic strip: a strip of two different metals joined together (often steel and copper). When it heats up, one metal grows more than the other, so the joined strip has to bend.

The bending strip pushes a rod, the rod flips the spring-loaded switch, and the electrical contacts open: the power is cut. Before the water boils there is very little steam, so the switch waits for a real boil.

The first fully automatic kettle with this idea was the Russell Hobbs K1 (1955).

(Simplified 3D model, slowed down; real kettle switches differ in detail.)

Sources:
Wikipedia, Kettle (Russell Hobbs K1, 1955: a bimetallic strip, heated through a pipe by the steam produced as the water comes to the boil, flexes and cuts off the current; little steam is produced before boiling): https://en.wikipedia.org/wiki/Kettle
Wikipedia, Bimetallic strip (two strips of different metals, usually steel and copper, that expand at different rates as they are heated; the different expansion forces the flat strip to bend; used to open or close electrical contacts): https://en.wikipedia.org/wiki/Bimetallic_strip"""
alt = ("3D animation of a steel electric kettle with a voiceover. Under the question How does a kettle know it's boiling? a red circle marks a small metal strip inside the switch housing, which bends and flips the switch off. "
       "The kettle is switched on, the badge shows power on, and it clicks off by itself. 1, steam goes down a tube: the kettle is cut open, the water boils, and steam puffs travel down a tube inside the handle. "
       "2, it heats a two-metal strip: the strip is steel on top and copper below and starts to glow. "
       "3, copper grows more, so it bends: a flat diagram shows the copper bar growing more than the steel bar, then the joined strip curling up. "
       "4, the strip flips the switch: the bending strip lifts a rod, the switch clicks up, the contacts move apart and the badge shows power off. "
       "The payoff reads Steam bends the strip, the strip turns it off, a follow line appears and the video loops.")
on = ['INSIDE IT', 'HOW DOES A KETTLE KNOW', "IT'S BOILING?", 'METAL STRIP', 'SWITCH', 'POWER:', 'ON', 'OFF', 'STEAM GOES DOWN A TUBE', 'STEAM', 'STEAM TUBE', 'BOILING WATER',
      'IT HEATS A TWO-METAL STRIP', 'STEEL', 'COPPER', 'COPPER GROWS MORE: IT BENDS', 'STEEL: GROWS A LITTLE', 'COPPER: GROWS MORE', 'HOT!', 'JOINED: IT HAS TO BEND', 'BENDS UP!',
      'THE STRIP FLIPS THE SWITCH', 'ROD', 'CONTACTS APART', 'CLICK!', 'STEAM BENDS THE STRIP', 'THE STRIP TURNS IT OFF', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p075', track='A', group='E', slot='', topicKey='kettle switch',
  outlier='everyday object + click (scorecard: hand-held / daily objects with a click win); our own model, script, words and sound',
  topic="Electric kettle automatic switch-off: steam heats a bimetallic strip that bends and trips the switch.",
  hook="HOW DOES A KETTLE KNOW / IT'S BOILING?", title="How a Kettle Knows It's Boiling ☕",
  principle='Steam from the boiling water is led through a tube onto a bimetallic strip (steel + copper); copper expands more, so the strip bends, lifts a rod and trips the spring-loaded switch, opening the contacts.',
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://en.wikipedia.org/wiki/Kettle', 'https://en.wikipedia.org/wiki/Bimetallic_strip'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
