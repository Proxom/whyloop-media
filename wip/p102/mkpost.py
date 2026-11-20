import json
caption = "How Does the Stick Know Your Tire Pressure? 🚗\nGuess: what pushes the stick back in the tube? 👇\nFollow @whyloop.hq for a new machine every day\n#howitworks #cars #engineering #mechanism #carsofinstagram"
first = """Answer: a spring 🚗

A pencil (stick) tire gauge is a tube with a small rubber piston inside and a calibrated spring above it.

Press the gauge onto the tire valve and a little pin in the gauge pushes the valve's pin, so air from the tire flows into the tube. The air pushes the piston along the tube, and the spring pushes back. The higher the pressure, the further the piston has to go before the spring pushes back just as hard. That is where it stops.

The numbered stick rides on the piston but is not attached to it. The piston pushes it out of the end of the tube. When you lift the gauge off, the air escapes and the spring pushes the piston back, but the stick stays where it was, held by a little friction, so you can read the number at the end of the tube. Then you push the stick back in for the next tire.

(Simplified 3D model; the gauge is drawn thicker than a real one and the scale is 1 mm per psi. Like most stick gauges it is only accurate to a few psi.)

Sources:
HowStuffWorks, How Tire Pressure Gauges Work (pin presses the valve pin; air pushes a tight-sealing rubber piston against a calibrated spring; the calibrated rod rides on the piston, is not connected to it and stays out when the piston goes back): https://auto.howstuffworks.com/pressure-gauge.htm
Carl Oppedahl, How pencil tire pressure gauges work (piston pushed against the spring until the pressures balance; the free-floating indicator rod is pushed out by the same distance and held by a just-right amount of friction): https://blog.oppedahl.com/how-pencil-tire-pressure-gauges-work
Alberta Farm Machinery Research Centre, Tire Pressure Gauges (pencil gauges: an indicator bar slides out a distance corresponding to the tire pressure): https://open.alberta.ca/dataset/3835591c-7115-4d63-8938-d53e18ca532a/resource/b5b5c242-2af2-4f8c-8117-0115448ae7f9/download/707-afmrc.pdf"""
alt = ("3D animation of a chrome pencil tire pressure gauge, with a voiceover. Under the question How does the stick know the pressure? the gauge is pressed onto the brass valve of a wheel lying flat, and a white numbered stick shoots out of its end, circled in red. "
       "Then the gauge is shown cut in half with red cut faces. 1, press it on, air rushes in: the gauge goes down onto the valve, a pin pushes the valve open and blue air dots flow into the tube. "
       "2, air pushes the piston up: a black rubber piston slides up the tube, pushing the stick in front of it. "
       "3, a spring pushes back: the spring above the piston glows and squeezes; a blue arrow pushes up, a white arrow pushes down, and the piston stops where they balance. "
       "4, lift it off, the stick stays: the gauge lifts off, the air leaves, the spring pushes the piston back down, but the stick stays out, held by friction. "
       "5, read the number: close up, the stick shows 32 psi at the end of the tube. The payoff reads Air pushes, spring pushes back, stick shows the psi, a follow line appears and the video loops.")
on = ['INSIDE IT', 'HOW DOES THE STICK', 'KNOW THE PRESSURE?', 'PRESS IT ON: AIR RUSHES IN', 'VALVE', 'PIN OPENS IT', 'AIR IN', 'AIR PUSHES THE PISTON UP', 'RUBBER PISTON', 'PUSHES THE STICK',
      'A SPRING PUSHES BACK', 'SPRING PUSHES BACK', 'BALANCED HERE', 'LIFT IT OFF: THE STICK STAYS', 'PISTON BACK', 'STICK STAYS', 'FRICTION HOLDS IT', 'READ THE NUMBER', 'READ IT HERE: 32 PSI',
      'AIR PUSHES, SPRING PUSHES BACK', 'STICK SHOWS THE PSI', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p102', track='A', group='V', slot='2026-11-26T17:00 Europe/London (planned, coordinator schedules)', topicKey='tire pressure gauge',
  outlier='scorecard rule: everyday object you hold + one "how does it know"; our own model, script, words and sound',
  topic="Pencil (stick) tire pressure gauge: tire air pushes a rubber piston against a calibrated spring; the piston pushes a loose numbered stick out; the stick stays out by friction when the piston springs back, so you can read the pressure.",
  hook="HOW DOES THE STICK / KNOW THE PRESSURE?", title="How Does the Stick Know Your Tire Pressure? 🚗",
  principle="Pressing the chuck on the valve depresses the valve pin; tire pressure acts on a sealed piston against a calibrated spring, so the piston travel is proportional to the pressure; a free calibrated rod is pushed out by the piston and held by friction after the piston returns.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://auto.howstuffworks.com/pressure-gauge.htm', 'https://blog.oppedahl.com/how-pencil-tire-pressure-gauges-work', 'https://open.alberta.ca/dataset/3835591c-7115-4d63-8938-d53e18ca532a/resource/b5b5c242-2af2-4f8c-8117-0115448ae7f9/download/707-afmrc.pdf'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
import re
from spellchecker import SpellChecker
sp = SpellChecker(); txt = ' '.join([caption, first, alt] + on + vo)
words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z']+", re.sub(r'https?://\S+', ' ', txt)))
words = {w.strip("'") for w in words}; words = {w[:-2] if w.endswith("'s") else w for w in words}
print('spell flags:', sorted(sp.unknown(words)), '| first comment chars', len(first))
