import json
caption = "Why Do Wipers Always Stop at the Bottom? 🚗\nGuess: what tells the motor where to stop? 👇\nFollow @whyloop.hq for a new machine every day\n#howitworks #engineering #cars #mechanism #carsofinstagram"
first = """Answer: a gap in a copper ring 🚗

Your wipers are driven by an electric motor. Through a worm gear it turns a big plastic gear, and one full turn of that gear moves the wipers up and back down once.

On the face of that gear there is a copper contact plate, and a small spring contact rubs on it. The plate has one gap, lined up with the "parked" position.

When you switch the wipers off mid-swipe, the switch stops feeding the motor directly. But the motor still gets power through that rubbing contact and the copper plate, so it keeps turning.

When the gap arrives under the contact, the copper path is broken: no contact, no power. The motor stops (many motors are also braked at that moment by shorting them, so they don't coast past), and the wipers sit right at the bottom.

In many newer cars a control module reads the same park switch and keeps the motor running until the wipers reach park.

(Simplified 3D model, inside shown in slow motion; real park switches vary: cam-pushed switches or sliding contacts.)

Sources:
Speedy Jim's Windshield Wiper Page (sliding contacts in the worm wheel keep the motor running after the switch is turned off; when the wipers reach park the contacts transfer and the motor is short-circuited, "dynamic braking"): http://www.nls.net/mp/volks/schem/wiper.htm
Dan Masters, Windshield Wiper Motors (with the dash switch off, power reaches the motor through the parking switch until the drive gear reaches the park position): https://www.gomog.com/BLAIR2/tech/electrical/wipers/2speed/2SpeedWiperMotor.html
GT6 Windscreen Wiper System (a cam under the gear wheel operates the park switch once per turn; the motor stops in the park position): https://gt6mk2.com/wiper.html
Saab WIS, Wiper/Washer System Description (the module keeps the motor running until the park switch shows the wipers at the bottom of the glass): https://saabwisonline.com/9-5-9650/2010/3-electrical-system/wash-wipe-systems/technical-description/wiper-washer-system-description-and-operation"""
alt = ("3D animation of a car's windshield wipers and their motor, with a voiceover. Under the question Why do wipers stop at the bottom? a wiper blade settles at the bottom of a dark windshield. "
       "1, switch off mid-swipe: a small panel shows the wiper switch turning from ON to OFF while the blade is halfway up, and the blade keeps moving, now in slow motion. "
       "2, a copper ring with one gap: the wiper gearbox is shown opened from above, with a black motor, a cream plastic gear, and a copper ring on the gear that has one gap. "
       "3, power still flows through it: glowing dots run from a red power wire through a brass contact finger, across the copper ring, and through a yellow wire to the motor, and the gear keeps turning. "
       "4, until the gap reaches the contact: an arrow shows the gap moving toward the contact. "
       "5, no contact equals no power: the gap reaches the contact, the dots stop, a red X marks the contact, and the motor stops. "
       "6, parked at the bottom: outside, the blade rests at the bottom of the glass. The payoff reads One gap in a copper ring parks your wipers, a follow line appears and the video loops.")
on = ['INSIDE IT', 'WHY DO WIPERS', 'STOP AT THE BOTTOM?', 'SWITCH OFF MID-SWIPE', 'STILL MOVING', 'SWITCH', 'ON', 'OFF', 'SLOW MOTION', 'A COPPER RING WITH ONE GAP', 'MOTOR', 'GEAR', 'COPPER RING', 'GAP',
      'POWER STILL FLOWS THROUGH IT', 'CONTACT', 'POWER IN', 'TO MOTOR', 'UNTIL THE GAP REACHES THE CONTACT', 'NO CONTACT = NO POWER', 'NO POWER', 'STOPPED', 'PARKED AT THE BOTTOM', 'PARKED',
      'ONE GAP IN A COPPER RING', 'PARKS YOUR WIPERS', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p090', track='A', group='V', slot='2026-11-21T21:00 Europe/London (planned by coordinator)', topicKey='wiper park switch',
  outlier='V group: one tiny hidden mechanism inside a car (AGENT.md 4.10 example "how a car\'s wipers park"); our own model, script, words and sound',
  topic="Windshield wiper park switch: after the dash switch is turned off, the motor keeps getting power through a contact riding on a copper plate on the final gear; one gap in the plate, lined up with the park position, breaks the circuit there, so the wipers always stop at the bottom.",
  hook="WHY DO WIPERS / STOP AT THE BOTTOM?", title="Why Do Wipers Always Stop at the Bottom? 🚗",
  principle="A self-parking wiper motor has a park switch on its final gear (sliding contacts or a cam): with the dash switch off, the motor is still fed through this switch until the gear reaches the park position, where the contact opens (and the armature is usually shorted to brake it), so the blades stop at the bottom.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['http://www.nls.net/mp/volks/schem/wiper.htm', 'https://www.gomog.com/BLAIR2/tech/electrical/wipers/2speed/2SpeedWiperMotor.html', 'https://gt6mk2.com/wiper.html',
           'https://saabwisonline.com/9-5-9650/2010/3-electrical-system/wash-wipe-systems/technical-description/wiper-washer-system-description-and-operation'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
import re
from spellchecker import SpellChecker
sp = SpellChecker(); txt = ' '.join([caption, first, alt] + on + vo)
words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z']+", re.sub(r'https?://\S+', ' ', txt)))
words = {w.strip("'") for w in words}; words = {w[:-2] if w.endswith("'s") else w for w in words}
print('spell flags:', sorted(sp.unknown(words)))
