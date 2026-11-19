import json
caption = "How Does the Needle Know Your Speed? 🚗\nGuess: does the magnet touch the cup? 👇\nFollow @whyloop.hq for a new machine every day\n#howitworks #cars #engineering #mechanism #physics"
first = """Answer: no, it never touches it 🧲

In a classic mechanical speedometer, a flexible cable from the gearbox (or a front wheel) spins a small permanent magnet behind the dial. The faster the car goes, the faster the magnet spins.

The magnet sits inside an aluminum "speed cup" with a small air gap between them. Aluminum is not magnetic, but the spinning magnet's field makes little swirling electric currents (eddy currents) flow in the cup. Those currents make their own magnetic field, and the result is a drag that pulls the cup around in the same direction the magnet spins, without any contact.

A fine hairspring holds the cup and the needle back toward zero. The cup turns only until the spring's pull balances the drag, then stops. Faster spin means stronger drag, so the cup and the needle turn further. When the car stops, the spring brings the needle back to zero.

(Simplified 3D model; in a real car the magnet spins much faster than shown here.)

Sources:
HowStuffWorks, Eddy-Current Speedometer (the spinning magnet creates eddy currents in the speed cup; their drag turns the cup and needle until the hairspring balances it; faster means more deflection): https://auto.howstuffworks.com/car-driving-safety/safety-regulatory-devices/speedometer3.htm
Wikipedia, Speedometer (a magnet on the speedometer cable drags an aluminum speedcup by eddy currents with no mechanical connection; a torsion spring holds the pointer toward zero): https://en.wikipedia.org/wiki/Speedometer
Explain that Stuff, How do speedometers work? (the magnet and the speed cup are separated by air; the hairspring lets the cup turn only a little): https://www.explainthatstuff.com/how-speedometer-works.html"""
alt = ("3D animation of a car speedometer, with a voiceover. Under the question How does the needle know your speed? the orange needle on a dashboard dial climbs from about 54 to 75 miles per hour. "
       "Then the gauge is shown standing up and cut open, with a small dial in the corner showing the same speed as the needle. 1, a cable spins a magnet: a red and blue round magnet starts spinning on the cable inside a polished aluminum cup, and the needle sits on top of the cup's shaft. "
       "2, air gap, they never touch: a gap tag points at the space between the magnet and the cup. "
       "3, spinning magnet drags the cup: glowing amber loops in the cup wall show tiny electric currents and an arrow shows the cup being pulled along with the magnet. "
       "4, a spring holds the cup back: the coiled hairspring on the shaft winds up and stops the cup at 25 miles per hour. "
       "5, faster spin equals needle higher: a card compares slow spin 25 miles per hour with fast spin 54 miles per hour as the magnet speeds up and the cup and needle turn further. "
       "The payoff reads A spinning magnet drags the needle over the dashboard dial at 54 miles per hour, a follow line appears and the video loops.")
on = ['INSIDE IT', 'HOW DOES THE NEEDLE', 'KNOW YOUR SPEED?', 'MPH', 'RPM x1000', 'A CABLE SPINS A MAGNET', 'MAGNET', 'CABLE', 'NEEDLE (ON THE CUP)', 'AIR GAP: THEY NEVER TOUCH', 'ALUMINUM CUP', 'GAP',
      'SPINNING MAGNET DRAGS THE CUP', 'CURRENTS IN THE CUP', 'A SPRING HOLDS THE CUP BACK', 'HAIRSPRING', 'FASTER SPIN = NEEDLE HIGHER', 'SLOW SPIN: 25 MPH', 'FAST SPIN: 54 MPH', 'A SPINNING MAGNET', 'DRAGS THE NEEDLE', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p092', track='A', group='V', slot='', topicKey='speedometer',
  outlier='new V topic (car dashboard everyone looks at) + one "how does it know" question; our own model, script, words and sound',
  topic="Eddy-current (mechanical) speedometer: the cable spins a magnet inside an aluminum speed cup; eddy currents drag the cup (no contact) against a hairspring, so the needle angle grows with speed.",
  hook="HOW DOES THE NEEDLE / KNOW YOUR SPEED?", title="How Does the Needle Know Your Speed? 🚗",
  principle="A magnet spun by the speedometer cable induces eddy currents in a non-magnetic aluminum cup around it; the resulting drag torque, proportional to the spin speed, turns the cup and needle against a hairspring until the two torques balance, so the needle angle is proportional to speed without any mechanical contact.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://auto.howstuffworks.com/car-driving-safety/safety-regulatory-devices/speedometer3.htm', 'https://en.wikipedia.org/wiki/Speedometer', 'https://www.explainthatstuff.com/how-speedometer-works.html'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
import re
from spellchecker import SpellChecker
sp = SpellChecker(); txt = ' '.join([caption, first, alt] + on + vo)
words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z']+", re.sub(r'https?://\S+', ' ', txt)))
words = {w.strip("'") for w in words}; words = {w[:-2] if w.endswith("'s") else w for w in words}
print('spell flags:', sorted(sp.unknown(words)))
