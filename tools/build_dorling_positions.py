"""Compute compact Dorling cartogram positions for the state spending map (m1).

Usage: python tools/build_dorling_positions.py .
Writes geo/malaysia_dorling_positions.csv.

How it works (all in screen pixels of the 580 x 300 chart):
1. Each state starts at a rough sketch of where it sits on the map (SKETCH below).
   Circle area = population, matching the size scale in the spec (largest = AREA_MAX px^2).
2. Neighbouring states (states that share a border) are pulled together until their
   circles touch, so the circles form one compact block shaped like the country.
3. Circles that overlap are pushed apart (small circles move more).
4. Borneo is held near its sketch position and never closer than SEA_GAP to the peninsula.
5. A weak pull back to the sketch keeps the overall shape (north stays at the top).
6. Pixel positions are turned back into longitude and latitude, using the same
   fixed projection as the chart (scale, centre and translate below).
"""
import csv, math, sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
W, H = 580, 300                  # chart size in the spec
SCALE = 1800                     # projection scale in the spec
CENTER = (106.0, 4.2)            # projection centre in the spec (longitude, latitude)
AREA_MAX = 5200                  # size range maximum in the spec
PAD = 0.8                        # gap between touching circles
SEA_GAP = 80                     # gap kept between the peninsula and Borneo

# states that share a border (Kuala Lumpur and Putrajaya sit inside Selangor).
# Pahang-Johor is left out so Johor stays at the southern tip instead of being pulled up.
NEIGHBOURS = [
    ('Perlis', 'Kedah'), ('Kedah', 'Pulau Pinang'), ('Kedah', 'Perak'), ('Kedah', 'Kelantan'),
    ('Pulau Pinang', 'Perak'), ('Perak', 'Kelantan'), ('Perak', 'Pahang'), ('Perak', 'Selangor'),
    ('Kelantan', 'Terengganu'), ('Kelantan', 'Pahang'), ('Terengganu', 'Pahang'),
    ('Pahang', 'Selangor'), ('Pahang', 'Negeri Sembilan'),
    ('Selangor', 'W.P. Kuala Lumpur'), ('Selangor', 'W.P. Putrajaya'), ('Selangor', 'Negeri Sembilan'),
    ('Negeri Sembilan', 'Melaka'), ('Negeri Sembilan', 'Johor'), ('Melaka', 'Johor'),
    ('Sarawak', 'Sabah'), ('Sabah', 'W.P. Labuan'), ('Sarawak', 'W.P. Labuan'),
]
BORNEO = {'Sarawak', 'Sabah', 'W.P. Labuan'}
SEA = [('Johor', 'Sarawak'), ('Pahang', 'Sarawak'), ('Terengganu', 'Sarawak')]

merc = lambda la: math.log(math.tan(math.pi / 4 + math.radians(la) / 2))
inv = lambda y: math.degrees(2 * math.atan(math.exp(y)) - math.pi / 2)

pop = {r['state']: int(r['population']) for r in csv.DictReader(open(f'{ROOT}/data/mnha_state_2024.csv'))}
pmax = max(pop.values())

# Starting points: a rough sketch of where each state sits, in pixels (north at the top).
# It follows the real map, except that Kuala Lumpur and Putrajaya (which sit inside Selangor)
# start just east of it, and Borneo starts closer to the peninsula than its real 600 km.
# Labuan starts in the notch between Sarawak and Sabah, as it does off the Borneo coast.
SKETCH = {
    'Perlis': (104, 34), 'Kedah': (132, 50), 'Pulau Pinang': (90, 66), 'Perak': (125, 100),
    'Kelantan': (170, 80), 'Terengganu': (200, 108), 'Pahang': (166, 124), 'Selangor': (100, 165),
    'W.P. Kuala Lumpur': (162, 167), 'W.P. Putrajaya': (132, 205), 'Negeri Sembilan': (148, 208),
    'Melaka': (160, 240), 'Johor': (195, 275),
    'Sarawak': (330, 140), 'Sabah': (384, 120), 'W.P. Labuan': (356, 104),
}
# the sketch was drawn for AREA_MAX = 6000; scale it if the circles are resized
f = math.sqrt(AREA_MAX / 6000)
SKETCH = {s: (x * f, y * f) for s, (x, y) in SKETCH.items()}
S = {s: dict(x=x, y=y, x0=x, y0=y, r=math.sqrt(pop[s] / pmax * AREA_MAX / math.pi))
     for s, (x, y) in SKETCH.items()}


def move(a, b, amount):
    """Move circles a and b towards each other by `amount` pixels (negative = apart).
    The smaller circle moves more."""
    A, B = S[a], S[b]
    dx, dy = B['x'] - A['x'], B['y'] - A['y']
    d = math.hypot(dx, dy) or 1e-6
    ux, uy = dx / d, dy / d
    wa = B['r'] ** 2 / (A['r'] ** 2 + B['r'] ** 2); wb = 1 - wa
    A['x'] += ux * amount * wa; A['y'] += uy * amount * wa
    B['x'] -= ux * amount * wb; B['y'] -= uy * amount * wb


for it in range(6000):
    pull = 0.05 if it < 5000 else 0.0
    # 2. neighbours attract until they touch
    for a, b in NEIGHBOURS:
        d = math.hypot(S[b]['x'] - S[a]['x'], S[b]['y'] - S[a]['y'])
        need = S[a]['r'] + S[b]['r'] + PAD
        if d > need: move(a, b, (d - need) * pull)
    # 4. Borneo kept a fixed sea gap away from the peninsula
    for a, b in SEA:
        d = math.hypot(S[b]['x'] - S[a]['x'], S[b]['y'] - S[a]['y'])
        need = S[a]['r'] + S[b]['r'] + SEA_GAP
        if d < need: move(a, b, (d - need) * pull)   # only pushes apart; Borneo's sketch position sets the rest
    # 5. weak pull back to the sketch keeps the overall shape
    for s, A in S.items():
        k = pull * 0.06
        A['x'] += (A['x0'] - A['x']) * k; A['y'] += (A['y0'] - A['y']) * k
    # 3b. gentle gravity: each circle drifts towards the centre of its own landmass,
    #     which closes small holes between circles that are not direct neighbours
    for group in (BORNEO, set(S) - BORNEO):
        cx = sum(S[s]['x'] for s in group) / len(group); cy = sum(S[s]['y'] for s in group) / len(group)
        for s in group:
            S[s]['x'] += (cx - S[s]['x']) * pull * 0.0; S[s]['y'] += (cy - S[s]['y']) * pull * 0.0
    # 3. overlapping circles pushed apart
    names = list(S)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            d = math.hypot(S[b]['x'] - S[a]['x'], S[b]['y'] - S[a]['y'])
            need = S[a]['r'] + S[b]['r'] + PAD
            if d < need: move(a, b, -(need - d))

overlaps = [(a, b) for a in S for b in S if a < b and
            math.hypot(S[a]['x'] - S[b]['x'], S[a]['y'] - S[b]['y']) < S[a]['r'] + S[b]['r']]
print('overlaps:', overlaps, file=sys.stderr)

# place the layout on the left of the chart (legends go on the right)
minx = min(A['x'] - A['r'] for A in S.values()); maxx = max(A['x'] + A['r'] for A in S.values())
miny = min(A['y'] - A['r'] for A in S.values()); maxy = max(A['y'] + A['r'] for A in S.values())
print(f'layout size {maxx - minx:.0f} x {maxy - miny:.0f} px', file=sys.stderr)
OX, OY = 55 - minx, (H - (maxy - miny)) / 2 - miny
for A in S.values():
    A['x'] += OX; A['y'] += OY

# label placement from the circle centre:
#   'in' = inside, 'L'/'R' = just outside on that side, 'B'/'T' = just below/above,
#   ('lead', dx, dy, align) = label placed dx, dy pixels away, joined by a leader line
LBL = {s: 'in' for s in SKETCH}
LBL.update({'Perlis': 'L', 'W.P. Labuan': 'T', 'W.P. Putrajaya': ('lead', -52, 20, 'right')})

# short codes shown inside the circles (the common three-letter state codes);
# the three smallest circles keep their full name outside, and the tooltip shows every full name
CODE = {
    'Johor': 'JHR', 'Kedah': 'KDH', 'Kelantan': 'KTN', 'Melaka': 'MLK', 'Negeri Sembilan': 'NSN',
    'Pahang': 'PHG', 'Pulau Pinang': 'PNG', 'Perak': 'PRK', 'Perlis': 'PLS', 'Sabah': 'SBH',
    'Sarawak': 'SWK', 'Selangor': 'SGR', 'Terengganu': 'TRG', 'W.P. Kuala Lumpur': 'KUL',
    'W.P. Putrajaya': 'PJY', 'W.P. Labuan': 'LBN',
}


def to_lonlat(x, y):
    lon = CENTER[0] + math.degrees((x - W / 2) / SCALE)
    lat = inv(merc(CENTER[1]) - (y - H / 2) / SCALE)
    return round(lon, 4), round(lat, 4)


w = csv.writer(open(f'{ROOT}/geo/malaysia_dorling_positions.csv', 'w', newline=''))
w.writerow(['state', 'longitude', 'latitude', 'radius_px', 'x_px', 'y_px',
            'code', 'label_longitude', 'label_latitude', 'label_align', 'leader',
            'leader_longitude', 'leader_latitude', 'leader_end_longitude', 'leader_end_latitude'])
for s, A in S.items():
    side = LBL[s]; leader = 0; dy = 0
    if side == 'in': dx, al = 0, 'inside'
    elif side == 'L': dx, al = -(A['r'] + 3), 'right'
    elif side == 'R': dx, al = A['r'] + 3, 'left'
    elif side == 'B': dx, dy, al = 0, A['r'] + 8, 'center'
    elif side == 'T': dx, dy, al = 0, -(A['r'] + 8), 'center'
    else: _, dx, dy, al = side; leader = 1
    lon, lat = to_lonlat(A['x'], A['y'])
    llon, llat = to_lonlat(A['x'] + dx, A['y'] + dy)
    # leader line runs from the circle's edge to just before the label
    d = math.hypot(dx, dy) or 1
    edge = to_lonlat(A['x'] + dx / d * (A['r'] + 1), A['y'] + dy / d * (A['r'] + 1)) if leader else (lon, lat)
    end = to_lonlat(A['x'] + dx - math.copysign(3, dx), A['y'] + dy) if leader else (llon, llat)
    w.writerow([s, lon, lat, round(A['r'], 1), round(A['x'], 1), round(A['y'], 1), CODE[s],
                llon, llat, al, leader, edge[0], edge[1], end[0], end[1]])
    print(f"{s:20s} r={A['r']:5.1f} x={A['x']:6.1f} y={A['y']:6.1f}", file=sys.stderr)
