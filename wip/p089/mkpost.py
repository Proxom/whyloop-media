import json
caption = "Why Does Velcro Stick? 🧷\nGuess: hooks on the rough side or the soft side? 👇\nFollow @whyloop.hq for a new machine every day\n#howitworks #engineering #velcro #science #satisfying"
first = """Answer: tiny hooks catch tiny loops 🧷

Hook-and-loop tape has two sides. The rough side is covered in tiny, stiff hooks. The soft side is covered in loops. Press them together and the hooks catch the loops. There's no glue: it's thousands of tiny catches.

Pull the two strips flat along each other (shear) and the force is shared by all the hooks at once, so it holds hard.

Peel it from one edge and the force lands on only a few hooks at a time, the row at the moving edge. Those let go, then the next row, then the next. That's why it opens so easily, and why you hear that ripping sound.

The idea came from burdock burrs, whose tiny hooks stuck to George de Mestral's clothes and his dog's fur.

(Simplified 3D model: real hooks and loops are much smaller and messier, and only some of them catch.)

Sources:
Wikipedia, Velcro (hooks catch the loops; with a rigid or flat pull the force is spread over all hooks; peeling applies the force to relatively few hooks at a time): https://en.wikipedia.org/wiki/Velcro
Velcro Brand, How do VELCRO Brand fasteners work? (hooks connect to loops; peel = disengaging the loops from each row of hooks; shear = sliding apart): https://www.velcro.com/news-and-blog/2023/02/how-do-velcro-brand-fasteners-work
HookandLoop.com, Hook and Loop 101 (peel is the disengagement of individual rows of hooks from an edge): https://www.hookandloop.com/hook-loop-101
American Chemical Society, Hook-and-Loop Tape activity (de Mestral, burrs, stiff hooks and flexible loops): https://www.acs.org/education/celebrating-chemistry-editions/2022-ncw/hook-and-loop-tape.html"""
alt = ("3D animation of hook-and-loop tape (Velcro), with a voiceover. Under the question Why does Velcro stick? a white strap is peeled off a fuzzy blue patch on a navy bag. "
       "Then a giant close-up: 1, one side: tiny stiff hooks, rows of white J-shaped hooks hang from a white tape. "
       "2, other side: soft loops, a blue tape covered in soft loops. Press: hooks catch loops, the hook tape comes down and each hook slips a loop into its curl, tagged Caught. "
       "3, pull flat: all hooks share it, a yellow arrow pulls the top tape sideways, every hook leans a little and glows and the loops lean, tagged Every hook holds, but nothing lets go. "
       "4, peel from the edge: the top tape bends up from the left; only the row of hooks at the bend glows orange, tagged One row at a time, straightens and lets go, then the next row; the other hooks are dimmed. "
       "The payoff reads Thousands of tiny hooks, one row at a time, a follow line appears and the video loops.")
on = ['INSIDE IT', 'WHY DOES', 'VELCRO STICK?', 'ONE SIDE: TINY STIFF HOOKS', 'HOOK', 'OTHER SIDE: SOFT LOOPS', 'LOOP', 'PRESS: HOOKS CATCH LOOPS', 'CAUGHT!',
      'PULL FLAT: ALL HOOKS SHARE IT', 'PULL', 'EVERY HOOK HOLDS', 'PEEL FROM THE EDGE', 'ONE ROW AT A TIME', 'THOUSANDS OF TINY HOOKS', 'ONE ROW AT A TIME', 'FOLLOW → A NEW MACHINE EVERY DAY']
vo = [d['text'] for d in json.load(open('vo/vo.json'))]
P = dict(id='p089', track='A', group='E', slot='', topicKey='hook and loop',
  outlier='scorecard rule: everyday object you touch + one "why it holds / why it opens"; our own model, script, words and sound',
  topic="Hook-and-loop (Velcro): stiff hooks catch soft loops; a flat (shear) pull loads every hook at once so it holds hard, a peel unhooks only the row at the moving edge so it opens easily.",
  hook="WHY DOES / VELCRO STICK?", title="Why Does Velcro Stick? 🧷",
  principle="Hook-and-loop is a mechanical fastener: stiff hooks on one tape catch loops on the other; a load along the tapes is shared by all engaged hooks, while peeling concentrates the load on the few hooks at the moving separation edge, which release one row at a time.",
  caption=caption, firstComment=first, altText=alt, onScreen=on, voiceover=vo,
  sources=['https://en.wikipedia.org/wiki/Velcro', 'https://www.velcro.com/news-and-blog/2023/02/how-do-velcro-brand-fasteners-work', 'https://www.hookandloop.com/hook-loop-101',
           'https://www.acs.org/education/celebrating-chemistry-editions/2022-ncw/hook-and-loop-tape.html'])
json.dump(P, open('post.json', 'w'), indent=1, ensure_ascii=False)
import re
from spellchecker import SpellChecker
sp = SpellChecker(); txt = ' '.join([caption, first, alt] + on + vo)
words = set(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z']+", re.sub(r'https?://\S+', ' ', txt)))
words = {w.strip("'") for w in words}; words = {w[:-2] if w.endswith("'s") else w for w in words}
print('spell flags:', sorted(sp.unknown(words)))
