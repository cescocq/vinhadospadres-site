# Silhouette glyphs: single colour (currentColor). Negative-space details use var(--bgc).
# Drawn freely in ~0..100 space; normalised later (same max size, centred) by measuring bboxes.
import math
B='var(--bgc,#E6DED0)'
def leaf(cx,cy,l,w,a):
    return f'<path transform="translate({cx} {cy}) rotate({a})" d="M0 0 Q{w} {-l/2} 0 {-l} Q{-w} {-l/2} 0 0Z"/>'
def star(cx,cy,n,R,r,rot=-90):
    pts=[]
    for i in range(2*n):
        rr=R if i%2==0 else r; a=math.radians(rot+i*180/n); pts.append(f'{cx+rr*math.cos(a):.1f},{cy+rr*math.sin(a):.1f}')
    return '<polygon points="'+' '.join(pts)+'"/>'
G={
'stone': '<circle cx="50" cy="56" r="34"/>'+leaf(52,24,26,10,35)+f'<path d="M50 26 Q38 56 50 88" fill="none" stroke="{B}" stroke-width="4"/>',
'peach': '<circle cx="50" cy="56" r="34"/>'+leaf(50,24,24,9,40)+leaf(50,24,22,8,-35)+f'<path d="M50 26 Q38 56 50 88" fill="none" stroke="{B}" stroke-width="4"/>',
'dried': '<circle cx="50" cy="50" r="38"/>'+f'<ellipse cx="50" cy="50" rx="14" ry="18" fill="{B}"/><ellipse cx="50" cy="50" rx="7" ry="10"/>',
'almond': '<path d="M50 8 Q82 44 72 72 Q62 94 50 94 Q38 94 28 72 Q18 44 50 8Z"/>',
'walnut': '<ellipse cx="50" cy="50" rx="36" ry="40"/>'+f'<path d="M50 10 Q40 22 50 34 Q60 46 50 58 Q40 70 50 90" fill="none" stroke="{B}" stroke-width="4"/>',
'blossom': ''.join(f'<ellipse cx="50" cy="26" rx="13" ry="22" transform="rotate({a} 50 50)"/>' for a in range(0,360,72))+f'<circle cx="50" cy="50" r="9" fill="{B}"/><circle cx="50" cy="50" r="4.5"/>',
'pollen': ''.join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x,y,r in [(30,30,12),(62,24,9),(50,52,15),(78,52,10),(24,66,10),(58,80,10),(84,80,6)]),
'pepper': ''.join(f'<circle cx="{x}" cy="{y}" r="17"/><path d="M{x-8} {y-3} Q{x} {y+7} {x+8} {y-3}" fill="none" stroke="{B}" stroke-width="3"/>' for x,y in [(30,34),(70,34),(50,70)]),
'anise': star(50,50,8,44,20)+''.join(f'<circle cx="{50+28*math.cos(math.radians(a*45-90)):.1f}" cy="{50+28*math.sin(math.radians(a*45-90)):.1f}" r="4" fill="{B}"/>' for a in range(8)),
'cinnamon': '<rect x="14" y="30" width="72" height="16" rx="8" transform="rotate(-20 50 38)"/><rect x="14" y="56" width="72" height="16" rx="8" transform="rotate(-20 50 64)"/>'+f'<circle cx="19" cy="49" r="4" fill="{B}"/><circle cx="19" cy="75" r="4" fill="{B}"/>',
'hay': '<path d="M50 96 V30" stroke="currentColor" stroke-width="8" fill="none"/>'+''.join(leaf(50,y,24,12,a) for y in (34,48,62,76) for a in (-28,28))+leaf(50,30,24,8,0),
'smoke': ''.join(f'<path d="M{x} 92 Q{x-14} 74 {x} 56 Q{x+14} 38 {x} 20" fill="none" stroke="currentColor" stroke-width="8" stroke-linecap="round"/>' for x in (28,50,72)),
'earth': '<path d="M6 86 Q22 40 50 50 Q66 26 94 86Z"/>',
'clay': '<path d="M36 8 H64 L62 16 Q88 32 84 62 Q80 92 50 94 Q20 92 16 62 Q12 32 38 16Z"/>'+f'<path d="M24 34 H76" stroke="{B}" stroke-width="3.5"/>',
'apple': '<path d="M50 26 Q30 12 16 30 Q6 54 20 76 Q32 96 50 88 Q68 96 80 76 Q94 54 84 30 Q70 12 50 26Z"/><path d="M50 26 Q50 14 58 6" stroke="currentColor" stroke-width="5" fill="none" stroke-linecap="round"/>'+leaf(56,14,18,7,70),
'baked': '<path d="M50 40 Q32 28 20 44 Q12 64 24 82 Q34 98 50 90 Q66 98 76 82 Q88 64 80 44 Q68 28 50 40Z"/>'+''.join(f'<path d="M{x} 30 Q{x-6} 20 {x} 12 Q{x+6} 4 {x} -2" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"/>' for x in (36,50,64)),
'pear': '<path d="M50 14 Q40 16 40 34 Q40 44 28 58 Q18 90 50 94 Q82 90 72 58 Q60 44 60 34 Q60 16 50 14Z"/><path d="M50 16 V4" stroke="currentColor" stroke-width="5" fill="none" stroke-linecap="round"/>',
'plum': '<ellipse cx="50" cy="56" rx="30" ry="36"/><path d="M50 22 Q54 10 62 6" stroke="currentColor" stroke-width="5" fill="none" stroke-linecap="round"/>'+f'<path d="M60 34 Q68 50 64 70" fill="none" stroke="{B}" stroke-width="4" stroke-linecap="round"/>',
'pineapple': '<ellipse cx="50" cy="64" rx="24" ry="30"/>'+f'<path d="M30 50 L70 80 M70 50 L30 80 M28 65 H72" stroke="{B}" stroke-width="3"/>'+leaf(50,36,30,8,0)+leaf(50,36,26,7,-30)+leaf(50,36,26,7,30),
'blueberry': '<circle cx="50" cy="52" r="40"/>'+f'<polygon points="50,22 55,32 66,32 57,39 61,50 50,43 39,50 43,39 34,32 45,32" fill="{B}"/>',
'elder': '<path d="M50 6 V30 M50 30 L22 50 M50 30 L78 50 M50 30 V58" stroke="currentColor" stroke-width="6" fill="none"/>'+''.join(f'<circle cx="{x}" cy="{y}" r="8"/>' for x,y in [(22,58),(36,70),(50,64),(64,70),(78,58),(30,84),(50,86),(70,84),(42,48),(58,48)]),
'cherry': '<circle cx="28" cy="72" r="20"/><circle cx="72" cy="76" r="20"/><path d="M28 54 Q40 24 62 8 Q64 40 72 58" stroke="currentColor" stroke-width="5" fill="none" stroke-linecap="round"/>'+leaf(62,8,22,8,60),
'blackberry': ''.join(f'<circle cx="{x}" cy="{y}" r="11"/>' for x,y in [(38,30),(62,30),(28,50),(50,50),(72,50),(38,70),(62,70),(50,88)])+leaf(50,20,16,6,-40)+leaf(50,20,16,6,40),
'herb': '<path d="M50 96 V12" stroke="currentColor" stroke-width="8" fill="none"/>'+''.join(leaf(50,y,34,16,a) for y,a in [(84,-50),(70,50),(56,-50),(42,50),(28,-45)])+leaf(50,14,22,8,0),
'mint': '<path d="M50 96 V40" stroke="currentColor" stroke-width="8" fill="none"/>'+leaf(50,74,40,18,-55)+leaf(50,74,40,18,55)+leaf(50,46,40,17,0),
'cedar': '<polygon points="50,4 76,38 64,38 86,66 70,66 92,88 8,88 30,66 14,66 36,38 24,38"/><rect x="44" y="86" width="12" height="12"/>',
'citrus': '<circle cx="50" cy="50" r="44"/>'+f'<circle cx="50" cy="50" r="34" fill="{B}"/>'+''.join(f'<path d="M50 50 L{50+30*math.cos(math.radians(a*45+22)):.1f} {50+30*math.sin(math.radians(a*45+22)):.1f} A30 30 0 0 1 {50+30*math.cos(math.radians(a*45+60)):.1f} {50+30*math.sin(math.radians(a*45+60)):.1f}Z"/>' for a in range(8)),
'drop': '<path d="M50 6 Q80 46 80 64 A30 30 0 0 1 20 64 Q20 46 50 6Z"/>'+f'<path d="M34 64 Q34 78 46 82" fill="none" stroke="{B}" stroke-width="5" stroke-linecap="round"/>',
'sun': '<circle cx="50" cy="50" r="20"/>'+''.join(f'<path d="M{50+30*math.cos(math.radians(a)):.1f} {50+30*math.sin(math.radians(a)):.1f} L{50+44*math.cos(math.radians(a)):.1f} {50+44*math.sin(math.radians(a)):.1f}" stroke="currentColor" stroke-width="7" stroke-linecap="round"/>' for a in range(0,360,45)),
'grain': ''.join(f'<circle cx="{x}" cy="{y}" r="5.5"/>' for x in range(14,90,18) for y in range(14,90,18) if (x-50)**2+(y-50)**2<44**2),
'arrow': '<path d="M8 50 H76" stroke="currentColor" stroke-width="9" stroke-linecap="round"/><polygon points="66,26 96,50 66,74"/><path d="M8 34 V66" stroke="currentColor" stroke-width="9" stroke-linecap="round"/>',
'feather': '<path d="M20 90 Q22 40 86 8 Q80 60 26 80Z"/>'+f'<path d="M14 96 L76 20" stroke="{B}" stroke-width="3.5"/><path d="M14 96 L26 80" stroke="currentColor" stroke-width="4"/>',
'scale': '<path d="M50 14 V86 M28 90 H72 M12 26 H88" stroke="currentColor" stroke-width="6" stroke-linecap="round"/><path d="M12 26 L2 54 H22Z M88 26 L78 54 H98Z"/><circle cx="50" cy="12" r="7"/>',
'barrel': '<path d="M26 8 H74 Q90 50 74 92 H26 Q10 50 26 8Z"/>'+f'<path d="M14 28 H86 M14 72 H86" stroke="{B}" stroke-width="5"/>',
'crunch': '<circle cx="44" cy="58" r="30"/><path d="M80 10 V28 M71 19 H89 M84 38 L94 44 M62 14 L66 4" stroke="currentColor" stroke-width="6" stroke-linecap="round"/>',
'rock': '<polygon points="8,82 20,40 46,20 78,30 94,62 84,86"/>'+f'<path d="M20 40 L48 52 L46 20 M48 52 L94 62 M48 52 L36 84" stroke="{B}" stroke-width="3" fill="none"/>',
'salt': '<polygon points="36,20 62,32 62,60 36,72 10,60 10,32"/><polygon points="72,48 92,58 92,82 72,92 52,82 52,58"/>'+f'<path d="M10 32 L36 44 L62 32 M36 44 V72 M52 58 L72 68 L92 58 M72 68 V92" stroke="{B}" stroke-width="3" fill="none"/>',
'chalk': '<rect x="10" y="38" width="80" height="26" rx="5" transform="rotate(-28 50 51)"/>'+''.join(f'<circle cx="{x}" cy="88" r="3.5"/>' for x in (22,36,50,64)),
}
TERM={'apricot':'stone','peach':'peach','dried fruit':'dried','almond':'almond','walnut':'walnut','orange blossom':'blossom','pollen':'pollen','white pepper':'pepper',
'aniseed':'anise','spice':'cinnamon','hay':'hay','smoky':'smoke','earthy':'earth','clay':'clay','apple':'apple','baked apple':'baked','pear':'pear','yellow plum':'plum','plum':'plum',
'tropical':'pineapple','blueberry':'blueberry','elderberry':'elder','red cherry':'cherry','fruit-driven':'cherry','dark fruit':'blackberry','forest fruit':'blackberry',
'wild herbs':'herb','dried herbs':'herb','savoury':'herb','mint':'mint','pennyroyal':'mint','cedar':'cedar','citrus':'citrus','fresh':'drop','clean':'drop','dry':'sun','bone-dry':'sun',
'fine tannins':'grain','refined tannins':'grain','grainy':'grain','textured':'grain','long finish':'arrow','elegant':'feather','ethereal':'feather','light':'feather','balanced':'scale',
'light oak':'barrel','crunchy':'crunch','mineral':'rock','granite mineral':'rock','stony':'rock','saline':'salt','chalk':'chalk','chalky':'chalk','chalky finish':'chalk'}
# ---- extra glyphs so every term has its own symbol ----
G.update({
'plumhalf': '<ellipse cx="50" cy="54" rx="34" ry="38"/>'+f'<ellipse cx="50" cy="56" rx="14" ry="20" fill="{B}"/><ellipse cx="50" cy="56" rx="8" ry="13"/>'+'<path d="M50 16 Q54 6 62 2" stroke="currentColor" stroke-width="5" fill="none" stroke-linecap="round"/>',
'grapes': ''.join(f'<circle cx="{x}" cy="{y}" r="10"/>' for x,y in [(30,32),(50,32),(70,32),(40,50),(60,50),(50,68),(30,50),(70,50),(40,84-16),(60,84-16),(50,86)])+'<path d="M50 22 V6" stroke="currentColor" stroke-width="5" stroke-linecap="round"/>'+leaf(50,10,26,10,60),
'strawberry': '<path d="M50 94 Q16 66 18 42 Q22 24 50 28 Q78 24 82 42 Q84 66 50 94Z"/>'+''.join(f'<circle cx="{x}" cy="{y}" r="2.6" fill="{B}"/>' for x,y in [(36,44),(50,42),(64,44),(42,58),(58,58),(50,72),(34,60),(66,60)])+leaf(50,30,20,9,-50)+leaf(50,30,20,9,50)+leaf(50,30,20,9,0),
'bundle': '<path d="M50 50 L22 94 M50 50 L36 96 M50 50 L50 96 M50 50 L64 96 M50 50 L78 94" stroke="currentColor" stroke-width="7" stroke-linecap="round"/>'+leaf(50,50,40,14,-25)+leaf(50,50,40,14,25)+leaf(50,50,40,14,0)+'<rect x="36" y="44" width="28" height="12" rx="4"/>'+'<path d="M50 44 V8" stroke="currentColor" stroke-width="4"/>',
'mushroom': '<path d="M8 52 Q14 14 50 12 Q86 14 92 52Z"/><path d="M38 52 H62 L66 90 Q50 96 34 90Z"/>'+f'<circle cx="32" cy="34" r="5" fill="{B}"/><circle cx="58" cy="26" r="4" fill="{B}"/><circle cx="72" cy="42" r="4" fill="{B}"/>',
'pennyroyal': '<path d="M50 98 V8" stroke="currentColor" stroke-width="7" stroke-linecap="round"/>'+''.join(f'<circle cx="{50+s*16}" cy="{y}" r="11"/>' for y in (78,52,26) for s in (-1,1))+'<circle cx="50" cy="10" r="9"/>',
'sparkle': star(40,52,4,40,10,-90)+star(78,22,4,18,5,-90)+star(80,78,4,12,3.5,-90),
'bone': '<rect x="24" y="42" width="52" height="16" rx="4"/>'+''.join(f'<circle cx="{x}" cy="{y}" r="12"/>' for x,y in [(18,38),(18,62),(82,38),(82,62)]),
'silk': '<path d="M6 30 Q28 6 50 30 T94 30 L94 50 Q72 26 50 50 T6 50Z"/><path d="M6 60 Q28 36 50 60 T94 60 L94 80 Q72 56 50 80 T6 80Z"/>',
'sand': ''.join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x,y,r in [(20,30,5),(42,18,4),(66,26,6),(84,44,4),(30,52,6),(54,46,4),(72,64,5),(18,76,4),(46,74,6),(64,88,4),(86,82,5),(38,92,3.5)]),
'weave': '<rect x="8" y="8" width="84" height="84" rx="10"/>'+''.join(f'<rect x="{18+i*22}" y="{18+j*22}" width="{14 if (i+j)%2 else 6}" height="{6 if (i+j)%2 else 14}" fill="{B}" transform="translate({0 if (i+j)%2 else 4} {4 if (i+j)%2 else 0})"/>' for i in range(3) for j in range(3)),
'cloud': '<path d="M24 76 Q6 76 8 60 Q10 44 28 46 Q30 22 54 24 Q74 24 78 42 Q96 42 94 60 Q92 76 76 76Z"/>',
'balloon': '<ellipse cx="50" cy="38" rx="28" ry="32"/><polygon points="44,70 56,70 50,78"/><path d="M50 78 Q42 88 52 98" stroke="currentColor" stroke-width="4" fill="none" stroke-linecap="round"/>',
'gem': '<polygon points="20,30 36,12 64,12 80,30 50,92"/>'+f'<path d="M20 30 H80 M36 12 L44 30 L50 92 L56 30 L64 12" stroke="{B}" stroke-width="3" fill="none"/>',
'cairn': '<ellipse cx="50" cy="84" rx="40" ry="12"/><ellipse cx="50" cy="60" rx="30" ry="11"/><ellipse cx="50" cy="38" rx="21" ry="10"/><ellipse cx="50" cy="18" rx="12" ry="8"/>',
'chalkdust': '<rect x="36" y="16" width="26" height="62" rx="5" transform="rotate(30 49 47)"/>'+''.join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x,y,r in [(18,84,4),(30,90,3),(42,86,4),(8,92,3),(54,94,3)]),
'chalkblock': '<polygon points="50,10 88,28 88,70 50,90 12,70 12,28"/>'+f'<path d="M12 28 L50 46 L88 28 M50 46 V90" stroke="{B}" stroke-width="3.5" fill="none"/>'+''.join(f'<circle cx="{x}" cy="{y}" r="2.5" fill="{B}"/>' for x,y in [(28,52),(34,64),(24,62),(66,54),(74,62),(68,70)]),
})
TERM.update({'yellow plum':'plumhalf','fruit-driven':'grapes','forest fruit':'strawberry','dried herbs':'bundle','savoury':'mushroom','pennyroyal':'pennyroyal',
'clean':'sparkle','bone-dry':'bone','refined tannins':'silk','grainy':'sand','textured':'weave','ethereal':'cloud','light':'balloon','mineral':'gem','stony':'cairn',
'chalky finish':'chalkdust','chalky':'chalkblock'})
G['silk']='<path d="M6 24 Q28 4 50 24 Q72 44 94 24 V42 Q72 62 50 42 Q28 22 6 42Z"/><path d="M6 58 Q28 38 50 58 Q72 78 94 58 V76 Q72 96 50 76 Q28 56 6 76Z"/>'
G['dried']=''.join(f'<ellipse cx="{x}" cy="{y}" rx="22" ry="14" transform="rotate(-30 {x} {y})"/><path d="M{x-12} {y+2} Q{x} {y-8} {x+12} {y-6}" fill="none" stroke="{B}" stroke-width="3"/>' for x,y in [(28,72),(50,50),(72,28)])
