import json
caption = "What Makes the Toast Pop Up? 🍞\nGuess: what holds it down? 👇\nFollow @whyloop.hq for a new machine every day\n#toaster #howitworks #mechanism #engineering #kitchen"
first = """Answer: an electromagnet 🧲

In many modern pop-up toasters, pushing the lever down lowers the tray with the bread and stretches a spring that wants to pull it back up. At the bottom, a metal plate on the lever reaches an electromagnet, and contacts switch the power on.

The electromagnet holds the plate, so the bread stays down while the heating wires glow.

A small timer circuit counts. The browning dial only changes how long it waits. When time is up, the timer cuts the magnet's power, the magnet lets go, and the stretched spring pulls the toast up (and the power switches off).

That's also why on many of these toasters the lever won't stay down when the toaster is unplugged: no power, no magnet. (Older toasters used a catch and a bimetal strip instead.)

(Simplified 3D model; real toasters differ in detail. The pop is shown in slow motion.)

Sources:
HowStuffWorks, How Toasters Work (a piece of metal on the handle is attracted to an electromagnet that holds the bread down; a capacitor timer cuts the power to the electromagnet and the spring pulls the bread up; the darkness control changes the timer): https://www.howstuffworks.com/toaster.htm
Restarters Wiki, Toasters (in more modern toasters the lever is held down against the spring by an electromagnet, energized with the element, and the current is interrupted after a preset time): https://wiki.restarters.net/index.php?title=Toasters
NZASE, Science of Toasters (modern toasters hold the tray down with electromagnets; some levers won't stay down when the toaster is unplugged): https://nzase.org.nz/wp-content/uploads/2025/10/NZASE-Background-Article-Toaster.pdf"""
alt = ("3D animation of a stainless steel pop-up toaster with a voiceover. Under the question What makes the toast pop? two slices of toast pop up. "
       "The front of the toaster is cut away to show the inside. "
       "1, push: a spring stretches. The lever goes down, the tray with the bread goes down, and a spring above it stretches. "
       "2, a magnet holds it down: a steel plate on the lever lands on a copper-wound electromagnet, which glows blue with field lines and holds it. "
       "3, it heats, a timer counts: the heating wires glow orange, the toast browns and a timer ring counts down. "
       "4, timer ends, magnet off: the ring reaches zero and the magnet turns off. "
       "5, the spring yanks it up: in slow motion the spring pulls the tray and toast up out of the slot. "
       "The payoff reads A magnet holds it down, the timer lets go, a follow line appears and the video loops.")
on = ['INSIDE IT', 'WHAT MAKES', 'THE TOAST POP?', 'PUSH: A SPRING STRETCHES', 'SPRING', 'A MAGNET HOLDS IT DOWN', 'STEEL PLATE', 'ELECTROMAGNET', 'MAGNET ON',
      'IT HEATS, A TIMER COUNTS', 'TIMER', 'HEATER', 'TIMER ENDS: MAGNET OFF', 'MAGNET OFF', 'THE SPRING YANKS IT UP', 'PULLS UP', 'SLOW MOTION', 'THE TIMER LETS GO', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p086', track='A', group='E', slot='', topicKey='toaster pop-up',
  outlier='scorecard rule: everyday object you touch every day + one "why it pops / what holds it"; our own model, script, words and sound',
  topic="Pop-up toaster (modern electronic type): the lever lowers the carriage and stretches a spring; a steel plate on the carriage meets an electromagnet that holds it down while the element heats; a timer cuts the magnet current and the spring pulls the toast up.",
  hook="WHAT MAKES / THE TOAST POP?", title="What Makes the Toast Pop Up? 🍞",
  principle="Lowering the carriage stretches the return spring and closes the power contacts; the electromagnet, energized with the element, holds a steel plate on the carriage down against the spring; an RC/electronic timer (set by the browning control) interrupts the magnet current after the preset time, so the spring returns the carriage and the contacts open.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://www.howstuffworks.com/toaster.htm', 'https://wiki.restarters.net/index.php?title=Toasters', 'https://nzase.org.nz/wp-content/uploads/2025/10/NZASE-Background-Article-Toaster.pdf'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
import re
from spellchecker import SpellChecker
sp = SpellChecker(); txt = ' '.join([caption, first, alt] + on + vo)
words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z']+", re.sub(r'https?://\S+', ' ', txt)))
words = {w.strip("'") for w in words}; words = {w[:-2] if w.endswith("'s") else w for w in words}
print('spell flags:', sorted(sp.unknown(words)))
