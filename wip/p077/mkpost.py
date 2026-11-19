import json
caption = "How Does the Gas Pump Know It's Full? ⛽\nGuess: what stops it, a sensor or air? 👇\nFollow @whyloop.hq for a new machine every day\n#gasstation #howitworks #mechanism #engineering #physics"
first = """Answer: air, not electronics ⛽

Near the tip of the nozzle there is a small sensing hole. A thin tube runs from it back into the handle.

Inside the handle, the fuel flows through a narrow spot (a Venturi), and that flow sucks air in through the little hole the whole time you are filling.

When the tank is full, fuel covers the hole, so no more air can get in. The suction inside the handle then pulls on a rubber disc (a diaphragm). The disc trips a latch, and a spring snaps the main valve shut: click. It is fully mechanical.

(Simplified 3D model, slowed down; real nozzles differ in detail. Foam or a splash can cover the hole too, which is why some pumps click off early.)

Sources:
Wikipedia, Gasoline pump: automatic cut-off with an auxiliary sensing tube from just inside the mouth of the nozzle to a Venturi pump in the handle; a mechanical valve in the handle detects the pressure change and closes: https://en.wikipedia.org/wiki/Fuel_dispenser
HowStuffWorks, How Does a Gas Pump Know When to Stop? (small hole near the tip, a small pipe back to the handle, suction from a Venturi; when gasoline blocks the hole, a mechanical linkage senses the change in suction and flips the nozzle off): https://auto.howstuffworks.com/fuel-efficiency/fuel-consumption/gas-pump-full-tank.htm
VST Hose, Automatic Nozzle Shutoff (the vacuum from the fuel flow draws air in through the sensing tube; when it meets liquid the vacuum increases, a diaphragm moves and disengages the trigger): https://vsthose.com/wp-content/uploads/2022/09/Q3_09_2022_Automatic-Nozzle-Shutoff.pdf"""
alt = ("3D animation of a green gas pump nozzle in a car's filler pipe, with a voiceover. Under the question How does the pump know it's full? a red circle marks the spout where it goes into the pipe, and the nozzle clicks off. "
       "The lever is squeezed, fuel flows, the fuel level rises and the nozzle clicks off by itself. 1, a tiny hole at the tip: the spout and pipe are cut open, showing a small sensing hole near the tip and a thin air tube running back to the handle. "
       "2, flowing fuel sucks air in: amber fuel drops flow through the handle and down the spout, while light blue air bubbles stream in through the hole, up the tube and into the handle. "
       "3, fuel covers the hole, no air: the fuel level rises over the hole and the air bubbles stop. "
       "4, suction pulls the disc, click: inside the handle a rubber disc bends upward, a latch lets go, the lever drops and a spring pushes the valve shut. "
       "The payoff reads Fuel covers the hole, suction shuts it off, a follow line appears and the video loops.")
on = ['INSIDE IT', 'HOW DOES THE PUMP', "KNOW IT'S FULL?", 'CLICK!', 'SQUEEZE', 'A TINY HOLE AT THE TIP', 'SENSING HOLE', 'AIR TUBE', 'FLOWING FUEL SUCKS AIR IN', 'AIR IN', 'FUEL FLOW',
      'FUEL COVERS THE HOLE: NO AIR', 'NO AIR GETS IN', 'FUEL RISING', 'SUCTION PULLS THE DISC: CLICK', 'RUBBER DISC', 'LATCH', 'SPRING SHUTS THE VALVE', 'FUEL COVERS THE HOLE', 'SUCTION SHUTS IT OFF', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p077', track='A', group='E', slot='', topicKey='fuel nozzle shutoff',
  outlier='classic "how does the gas pump know" question (many 1M+ explainers); our own model, script, words and sound',
  topic="Gas pump nozzle automatic shut-off: Venturi suction draws air through a sensing hole; fuel covering the hole lets the vacuum pull a diaphragm that trips the latch.",
  hook="HOW DOES THE PUMP / KNOW IT'S FULL?", title="How Does the Gas Pump Know It's Full? ⛽",
  principle="Fuel flowing through a Venturi in the handle sucks air through a sensing hole near the spout tip; when fuel covers the hole the vacuum rises, a diaphragm moves and releases the latch, and the main valve spring closes the valve.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://en.wikipedia.org/wiki/Fuel_dispenser', 'https://auto.howstuffworks.com/fuel-efficiency/fuel-consumption/gas-pump-full-tank.htm', 'https://vsthose.com/wp-content/uploads/2022/09/Q3_09_2022_Automatic-Nozzle-Shutoff.pdf'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
