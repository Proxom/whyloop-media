import json
caption = "How Does the Radiator Knob Know the Room Is Warm? 🌡️\nGuess: what's hiding inside the knob? 👇\nFollow @whyloop.hq for a new machine every day\n#howitworks #engineering #mechanism #heating #satisfying"
first = """Answer: a little capsule of wax 🌡️

That white knob on a radiator is a thermostatic radiator valve (TRV). The valve under it lets hot water from the boiler flow into the radiator.

Inside the knob there is a small sealed capsule filled with wax (some knobs use a liquid or a gas instead). As the room warms up, the wax expands. The growing capsule pushes a pin down into the valve, and the pin presses a little disc toward its seat, so less and less hot water gets into the radiator, until the flow is shut off.

When the room cools down, the wax shrinks again. A spring in the valve pushes the pin back up, the valve opens, and hot water flows in again. No batteries, no wires: the wax does the measuring.

Turning the knob to a higher number makes the valve close at a warmer room temperature (the numbers are settings, not exact degrees).

(Simplified 3D model: the pin's movement is enlarged so you can see it; in a real valve it moves much less.)

Sources:
Danfoss, Domestic Heating Controls Are Easy, Part 5 (no external power; a wax, liquid or gas charged capsule in the sensor head expands and contracts with room temperature, operating a piston that acts on the valve pin; a spring returns it when it cools): https://assets.danfoss.com/documents/latest/44965/AM000086447758en-010101.pdf
Building Services Tutor, How Thermostatic Radiator Valves Work (the expansion mass pushes a transmission pin that closes the valve; when it contracts the valve opens again; the knob levels set the room temperature): https://www.buildingservicestutor.com/how-thermostatic-radiator-valves-work/
PHPI Online, Inside a Thermostatic Radiator Valve (the sensor pushes the pin down and the disc toward the valve seat; when the room cools a spring pushes it back and the valve opens): https://phpionline.co.uk/feature-articles/inside-a-thermostatic-radiator-valve
EUA Consumer Guide, Thermostatic Radiator Valves (the numbers on a TRV do not represent specific room temperatures): https://eua.org.uk/uploads/5E1EC0897C97B.pdf"""
alt = ("3D animation of a radiator valve, with a voiceover. Under the question How does it know the room is warm? the knob is shown cut open: a wax capsule grows and a pin shuts the valve. "
       "Then a white radiator with a chrome valve and a white numbered knob, circled in red. Then the valve is shown cut in half. "
       "1, hot water flows in: orange hot water flows from the pipe, up through the valve and out to the radiator, and a room thermometer card reads cool. "
       "2, inside the knob: wax. A tall capsule of pale wax sits inside the knob, above a thin pin. "
       "3, room warms, wax grows: the thermometer turns red and the wax capsule grows downward. "
       "4, wax pushes the pin, valve shuts: the pin and a black disc move down onto the valve seat and the hot water stops flowing. "
       "5, room cools, spring opens it: the thermometer turns blue, the wax shrinks and a spring pushes the pin back up, so the water flows again. "
       "The payoff reads Warm wax grows and shuts the valve, a follow line appears and the video loops.")
on = ['INSIDE IT', 'HOW DOES IT KNOW', 'THE ROOM IS WARM?', 'HOT WATER FLOWS IN', 'HOT WATER', 'VALVE', 'TO RADIATOR', 'ROOM', 'COOL', 'WARM', 'INSIDE THE KNOB: WAX', 'WAX', 'PIN',
      'ROOM WARMS: WAX GROWS', 'WAX PUSHES THE PIN: VALVE SHUTS', 'SHUT', 'ROOM COOLS: SPRING OPENS IT', 'SPRING', 'WARM WAX GROWS', 'AND SHUTS THE VALVE', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
src = ['https://assets.danfoss.com/documents/latest/44965/AM000086447758en-010101.pdf', 'https://www.buildingservicestutor.com/how-thermostatic-radiator-valves-work/',
       'https://phpionline.co.uk/feature-articles/inside-a-thermostatic-radiator-valve', 'https://eua.org.uk/uploads/5E1EC0897C97B.pdf']
P = dict(id='p093', track='A', group='E', slot='2026-11-24T17:00 Europe/London (planned, coordinator schedules)', topicKey='thermostatic radiator valve',
  outlier='scorecard rule: everyday object you touch + one "how does it know"; our own model, script, words and sound',
  topic="Thermostatic radiator valve: a wax capsule in the knob expands as the room warms and pushes a pin that closes the hot-water valve; when the room cools the wax shrinks and a spring reopens the valve.",
  hook="HOW DOES IT KNOW / THE ROOM IS WARM?", title="How Does the Radiator Knob Know the Room Is Warm? 🌡️",
  principle="A TRV head holds a wax (or liquid/gas) filled capsule that expands with room temperature and pushes the valve pin toward the seat, throttling the hot-water flow to zero; on cooling it contracts and the valve's return spring pushes the pin back, reopening the valve.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo, sources=src)
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
import re
from spellchecker import SpellChecker
sp = SpellChecker(); txt = ' '.join([caption, first, alt] + on + vo)
words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z']+", re.sub(r'https?://\S+', ' ', txt)))
words = {w.strip("'") for w in words}; words = {w[:-2] if w.endswith("'s") else w for w in words}
print('spell flags:', sorted(sp.unknown(words)))
