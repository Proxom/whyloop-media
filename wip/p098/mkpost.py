import json
caption = "How Does Your Car Know the Tank Is Empty? ⛽\nGuess: what's floating in your gas tank? 👇\nFollow @whyloop.hq for a new machine every day\n#howitworks #engineering #cars #mechanism #carsofinstagram"
first = """Answer: a float and a resistor ⛽

Inside the gas tank, the fuel level sender has a float on a hinged metal arm. The float rides on top of the fuel.

At the hinge, the arm moves a small metal wiper over a strip of resistive material. One end of the strip is grounded.

Full tank: the float is high, so the wiper sits near the grounded end. The current has only a short way to go through the strip, so the resistance is low and more current reaches the gauge: the needle points to F.

As the fuel is used, the float sinks and the wiper slides along the strip. Now the current has to run a long way through it: more resistance, less current, and the needle drops toward E.

Fill it up and the float rises again: short path, more current, back to F.

(Simplified 3D model, parts enlarged. Some makes wire it the other way round, with high resistance at full; the gauge is matched to its sender. Many newer cars read the sender through a computer first, and the fuel use and refill are sped up in the video.)

Sources:
HowStuffWorks, How Fuel Gauges Work (float on a thin metal rod, wiper sliding on a strip of resistive material grounded on one side; float high = small resistance = more current to the gauge; level drops = resistance increases, current decreases): https://auto.howstuffworks.com/fuel-gauge.htm
Delphi Technologies, Diagnosing a bad fuel sending unit (float, metal rod/arm, variable resistor; the direction depends on the maker): https://www.delphiautoparts.com/resource-center/article/what's-wrong-with-my-fuel-gauge-diagnosing-a-bad-fuel-sending-unit
Tanks Inc., Universal fuel sender questions (sender ohm ranges by maker, e.g. 73 ohms empty to 10 ohms full): https://www.tanksinc.com/index.cfm/page/ptype=results/category_id=159/mode=cat/cat159.htm"""
alt = ("3D animation of a car fuel gauge, with a voiceover. Under the question How does the car know it's empty? a round dash fuel gauge needle swings from F to E, with a red circle on the E. "
       "Then a gas tank is shown cut in half with red cut edges, with a small gauge drawn below it. 1, a float on a hinged arm: a white float rides on the orange fuel, on a thin metal arm hinged on the sender. "
       "2, the arm moves a wiper: close up, a brass wiper at the hinge touches a dark resistor strip on a white card; glowing dots show the current taking a short path to ground. "
       "3, fuel used, the float sinks: the fuel level drops (sped up), the float goes down, the wiper slides along the strip and the needle drops to E. "
       "4, long path equals less current: close up, the current now runs a long way through the strip, more resistance, and the dots slow down. "
       "5, fill up, short path again: fuel pours in, the float rises and the needle goes back to F. The payoff reads A float plus a resistor move the needle, a follow line appears and the video loops.")
on = ['INSIDE IT', 'HOW DOES THE CAR', "KNOW IT'S EMPTY?", 'A FLOAT ON A HINGED ARM', 'FLOAT', 'ARM', 'HINGE', 'FUEL', 'GAUGE', 'THE ARM MOVES A WIPER', 'WIPER', 'RESISTOR STRIP', 'SHORT PATH', 'TO GROUND',
      'FUEL USED: THE FLOAT SINKS', 'SPED UP', 'WIPER SLIDES', 'NEEDLE DROPS', 'LONG PATH = LESS CURRENT', 'LONG PATH', 'MORE RESISTANCE', 'LESS CURRENT', 'FILL UP: SHORT PATH AGAIN', 'FUEL IN', 'BACK TO FULL',
      'A FLOAT + A RESISTOR', 'MOVE THE NEEDLE', 'FOLLOW → A NEW MACHINE EVERY DAY', 'E', 'F', '1/2']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p098', track='A', group='V', slot='2026-11-25T21:00 Europe/London (planned, coordinator schedules)', topicKey='fuel gauge',
  outlier='scorecard rule: everyday thing you see daily (the fuel needle) + one "how does it know"; our own model, script, words and sound',
  topic="Car fuel gauge: a float on a hinged arm in the tank moves a wiper along a resistor strip; the resistance changes with the fuel level, which changes the current to the dash gauge, so the needle moves.",
  hook="HOW DOES THE CAR / KNOW IT'S EMPTY?", title="How Does Your Car Know the Tank Is Empty? ⛽",
  principle="The fuel level sender is a float on a pivoted arm that drives a wiper over a resistive strip grounded at one end (a variable resistor); with a full tank the wiper is near the grounded end, resistance is low and more current flows through the gauge (needle at F); as the level drops the wiper moves away, resistance rises, current falls and the needle drops toward E.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://auto.howstuffworks.com/fuel-gauge.htm', "https://www.delphiautoparts.com/resource-center/article/what's-wrong-with-my-fuel-gauge-diagnosing-a-bad-fuel-sending-unit", 'https://www.tanksinc.com/index.cfm/page/ptype=results/category_id=159/mode=cat/cat159.htm'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
import re
from spellchecker import SpellChecker
sp = SpellChecker(); txt = ' '.join([caption, first, alt] + on + vo)
words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z']+", re.sub(r'https?://\S+', ' ', txt)))
words = {w.strip("'") for w in words}; words = {w[:-2] if w.endswith("'s") else w for w in words}
print('spell flags:', sorted(sp.unknown(words)))
print('firstComment chars', len(first))
