"""Build tidy CSVs from tables in the MNHA Health Expenditure Report 2011-2024 (MOH Malaysia).
Values are copied as published (RM million / percent). Checks: components must sum to the published totals."""
import csv, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
Y = list(range(2011, 2025))
def nums(s):
    out = []
    for t in s.split():
        t = t.replace(',', '')
        out.append(None if t in ('n/a', 'na', '<1') else float(t))
    return out

# ---------- T4.1 + T4.2 + T5.1d + T8.1 : national yearly indicators ----------
t41 = """2011 35,953 44,174 911,733 81.39 3.94
2012 39,448 47,988 971,252 82.20 4.06
2013 41,647 50,576 1,018,614 82.35 4.09
2014 46,780 55,441 1,106,443 84.38 4.23
2015 50,065 58,619 1,176,941 85.41 4.25
2016 51,775 59,633 1,249,698 86.82 4.14
2017 56,181 62,352 1,372,310 90.10 4.09
2018 60,284 66,490 1,447,760 90.67 4.16
2019 64,085 70,632 1,512,738 90.73 4.24
2020 68,252 75,845 1,418,491 89.99 4.81
2021 78,606 82,658 1,548,701 95.10 5.08
2022 77,850 77,015 1,794,893 101.09 4.34
2023 82,846 83,500 1,824,019 99.22 4.54
2024 89,827 89,827 1,932,291 100.00 4.65"""
t42 = """2011 1,237 1,520 29,062,000
2012 1,337 1,626 29,510,000
2013 1,378 1,674 30,213,700
2014 1,523 1,805 30,708,500
2015 1,605 1,880 31,186,100
2016 1,637 1,885 31,633,500
2017 1,754 1,947 32,022,600
2018 1,862 2,053 32,382,300
2019 1,970 2,172 32,523,000
2020 2,103 2,337 32,447,400
2021 2,413 2,537 32,576,300
2022 2,381 2,355 32,698,100
2023 2,480 2,500 33,401,800
2024 2,637 2,637 34,058,900"""
t51d = """2011 20,251 56.33 15,702 43.67 35,953
2012 22,007 55.79 17,442 44.21 39,448
2013 22,868 54.91 18,780 45.09 41,647
2014 25,921 55.41 20,859 44.59 46,780
2015 27,046 54.02 23,019 45.98 50,065
2016 26,774 51.71 25,002 48.29 51,775
2017 29,306 52.16 26,875 47.84 56,181
2018 31,397 52.08 28,887 47.92 60,284
2019 34,217 53.39 29,868 46.61 64,085
2020 36,659 53.71 31,594 46.29 68,252
2021 44,960 57.20 33,646 42.80 78,606
2022 41,308 53.06 36,542 46.94 77,850
2023 42,579 51.40 40,266 48.60 82,846
2024 45,580 50.74 44,248 49.26 89,827"""
t81 = """2011 35,953 16,496 45.88 3.94 1.81
2012 39,448 18,239 46.24 4.06 1.88
2013 41,647 19,038 45.71 4.09 1.87
2014 46,780 21,782 46.56 4.23 1.97
2015 50,065 22,751 45.44 4.25 1.93
2016 51,775 22,349 43.16 4.14 1.79
2017 56,181 24,818 44.17 4.09 1.81
2018 60,284 26,522 44.00 4.16 1.83
2019 64,085 28,860 45.03 4.24 1.91
2020 68,252 31,126 45.60 4.81 2.19
2021 78,606 38,767 49.32 5.08 2.50
2022 77,850 33,907 43.55 4.34 1.89
2023 82,846 36,227 43.73 4.54 1.99
2024 89,827 39,148 43.58 4.65 2.03"""
P = lambda s: {int(r[0]): r[1:] for r in (nums(l) for l in s.splitlines())}
a, b, c, d = P(t41), P(t42), P(t51d), P(t81)
rows = []
for y in Y:
    assert a[y][0] == c[y][4] == d[y][0], y            # TEH consistent across tables
    assert abs(c[y][0] + c[y][2] - c[y][4]) <= 1, y     # public + private = TEH
    rows.append(dict(year=y, teh_nominal_rm_mil=a[y][0], teh_constant_2024_rm_mil=a[y][1], gdp_nominal_rm_mil=a[y][2],
        gdp_deflator=a[y][3], teh_pct_gdp=a[y][4], per_capita_nominal_rm=b[y][0], per_capita_constant_2024_rm=b[y][1],
        population=b[y][2], public_rm_mil=c[y][0], public_pct_teh=c[y][1], private_rm_mil=c[y][2], private_pct_teh=c[y][3],
        moh_rm_mil=d[y][1], moh_pct_teh=d[y][2], moh_pct_gdp=d[y][4]))

def write(name, rows):
    with open(os.path.join(OUT, name), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator='\n')
        w.writeheader()
        for r in rows:
            w.writerow({k: ('' if v is None else (int(v) if isinstance(v, float) and v.is_integer() and 'pct' not in k and k not in ('gdp_deflator',) else v)) for k, v in r.items()})
    print(name, len(rows), 'rows')
write('mnha_national_2011_2024.csv', rows)

# ---------- T4.3 state 2024 ----------
t43 = [("Selangor","Selangor",7363400,18011),("Federal Territory Kuala Lumpur","W.P. Kuala Lumpur",2067500,13331),
("Johor","Johor",4186300,8876),("Penang","Pulau Pinang",1800400,6877),("Perak","Perak",2569600,6334),("Sabah","Sabah",3742200,6325),
("Sarawak","Sarawak",2518100,6079),("Kedah","Kedah",2217500,5185),("Pahang","Pahang",1668200,4004),("Kelantan","Kelantan",1888500,3689),
("N. Sembilan","Negeri Sembilan",1240100,3354),("Melaka","Melaka",1047100,3064),("Terengganu","Terengganu",1232100,2686),
("Federal Territory Putrajaya","W.P. Putrajaya",120300,996),("Perlis","Perlis",296800,798),("Federal Territory Labuan","W.P. Labuan",100800,219)]
assert sum(r[2] for r in t43) == 34058900 and abs(sum(r[3] for r in t43) - 89827) <= 2
write('mnha_state_2024.csv', [dict(state=s2, state_in_report=s1, population=p, expenditure_rm_mil=e) for s1, s2, p, e in t43])

# ---------- generic year-table builder with total check ----------
def table(spec, total_line, tol=2, pct=None):
    out = {}
    for line in spec.strip().splitlines():
        code, name, vals = line.split('|')
        out[(code.strip(), name.strip())] = nums(vals)
    tot = nums(total_line)
    for i, y in enumerate(Y):
        s = sum(v[i] for v in out.values() if v[i] is not None)
        assert abs(s - tot[i]) <= tol, (y, s, tot[i])
    if pct:
        p = {}
        for line in pct.strip().splitlines():
            code, name, vals = line.split('|'); p[code.strip()] = nums(vals)
        for i, y in enumerate(Y):
            s = sum(v[i] for v in p.values() if v[i] is not None)
            assert abs(s - 100) <= 0.15, ('pct', y, s)
        return out, p
    return out, None

# T5.1b / T5.1c sources of financing
src = """MHS.1.1.1.1|Ministry of Health (MOH)|16,496 18,239 19,038 21,782 22,751 22,349 24,818 26,522 28,860 31,126 38,767 33,907 36,227 39,148
MHS.1.1.1.2|Ministry of Higher Education (MoHE)|1,245 1,311 1,261 1,376 1,314 1,280 1,256 1,375 1,632 1,478 1,591 1,561 1,807 1,975
MHS.1.1.1.3|Ministry of Defence (MOD)|140 172 175 186 169 154 132 103 150 135 197 194 241 285
MHS.1.1.1.9|Other federal agencies (including statutory bodies)|1,813 1,678 1,677 1,805 1,886 2,007 2,061 2,116 2,231 2,480 2,856 3,924 2,291 2,066
MHS.1.1.2.1|State government (General)|90 105 78 86 89 95 107 143 118 189 239 159 157 194
MHS.1.1.2.2|Other state agencies (including statutory bodies)|129 137 189 212 346 385 392 467 502 498 533 589 650 665
MHS.1.1.3|Local authorities (LA)|142 150 188 164 178 138 154 194 249 264 243 275 351 358
MHS.1.2.1|Employees Provident Fund (EPF)|39 38 42 46 52 56 58 67 83 79 102 88 93 83
MHS.1.2.2|Social Security Organisation (SOCSO)|157 176 219 264 261 310 329 410 394 409 434 612 762 806
MHS.2.2|Voluntary private insurance|2,614 2,774 2,916 3,203 3,623 3,846 4,085 4,313 4,875 4,960 5,531 6,534 6,721 7,113
MHS.2.3|Private MCOs and other similar entities|243 302 287 437 626 831 879 922 993 926 1,039 483 578 688
MHS.2.4|Private household out-of-pocket (OOP) payment|11,466 12,649 13,933 15,373 16,063 17,692 19,305 21,019 22,061 23,676 25,197 28,399 31,678 34,843
MHS.2.5|Non-profit institutions|312 363 78 40 69 87 92 92 90 138 150 137 127 131
MHS.2.6|All corporations (other than health insurance)|1,064 1,352 1,564 1,803 2,634 2,541 2,509 2,536 1,845 1,810 1,686 970 1,143 1,461
MHS.9|Rest of the world (ROW)|3 2 3 4 5 4 5 5 4 82 43 19 19 12"""
srcp = """MHS.1.1.1.1|x|45.88 46.24 45.71 46.56 45.44 43.16 44.17 44.00 45.03 45.60 49.32 43.55 43.73 43.58
MHS.1.1.1.2|x|3.46 3.32 3.03 2.94 2.63 2.47 2.23 2.28 2.55 2.17 2.02 2.01 2.18 2.20
MHS.1.1.1.3|x|0.39 0.44 0.42 0.40 0.34 0.30 0.24 0.17 0.23 0.20 0.25 0.25 0.29 0.32
MHS.1.1.1.9|x|5.04 4.25 4.03 3.86 3.77 3.88 3.67 3.51 3.48 3.63 3.63 5.04 2.77 2.30
MHS.1.1.2.1|x|0.25 0.27 0.19 0.18 0.18 0.18 0.19 0.24 0.18 0.28 0.30 0.20 0.19 0.22
MHS.1.1.2.2|x|0.36 0.35 0.45 0.45 0.69 0.74 0.70 0.77 0.78 0.73 0.68 0.76 0.78 0.74
MHS.1.1.3|x|0.39 0.38 0.45 0.35 0.36 0.27 0.27 0.32 0.39 0.39 0.31 0.35 0.42 0.40
MHS.1.2.1|x|0.11 0.10 0.10 0.10 0.10 0.11 0.10 0.11 0.13 0.12 0.13 0.11 0.11 0.09
MHS.1.2.2|x|0.44 0.45 0.53 0.57 0.52 0.60 0.59 0.68 0.61 0.60 0.55 0.79 0.92 0.90
MHS.2.2|x|7.27 7.03 7.00 6.85 7.24 7.43 7.27 7.15 7.61 7.27 7.04 8.39 8.11 7.92
MHS.2.3|x|0.68 0.77 0.69 0.93 1.25 1.60 1.56 1.53 1.55 1.36 1.32 0.62 0.70 0.77
MHS.2.4|x|31.89 32.06 33.45 32.86 32.08 34.17 34.36 34.87 34.42 34.69 32.05 36.48 38.24 38.79
MHS.2.5|x|0.87 0.92 0.19 0.08 0.14 0.17 0.16 0.15 0.14 0.20 0.19 0.18 0.15 0.15
MHS.2.6|x|2.96 3.43 3.75 3.85 5.26 4.91 4.47 4.21 2.88 2.65 2.15 1.25 1.38 1.63
MHS.9|x|0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.01 0.12 0.05 0.02 0.02 0.01"""
TEH = "35,953 39,448 41,647 46,780 50,065 51,775 56,181 60,284 64,085 68,252 78,606 77,850 82,846 89,827"
s, sp = table(src, TEH, pct=srcp)
group = lambda code: 'Rest of the world' if code == 'MHS.9' else ('Public' if code.startswith('MHS.1') else 'Private')
simple = {'MHS.1.1.1.1': 'Ministry of Health', 'MHS.2.4': 'Households (out of pocket)', 'MHS.2.2': 'Private insurance'}
rows = []
for (code, name), vals in s.items():
    for i, y in enumerate(Y):
        rows.append(dict(year=y, code=code, source=name, sector=group(code),
                         payer_group=simple.get(code, 'Other government' if group(code) == 'Public' else 'Employers and others'),
                         rm_mil=vals[i], pct_teh=sp[code][i]))
write('mnha_financing_sources_2011_2024.csv', rows)

# T6.1b / T6.1c providers (+ T5.2.3b public share)
prov = """MHP.1|All hospitals|18,635 21,047 21,962 24,793 26,665 28,139 30,333 32,736 35,437 36,847 39,317 41,714 44,790 48,721
MHP.2|Residential long-term care facilities|16 20 2 2 2 5 2 5 1 5 2 4 21 21
MHP.3|Providers of ambulatory health care|6,424 7,528 8,521 10,017 10,458 10,967 11,876 12,707 13,708 13,889 15,981 17,442 17,011 18,881
MHP.4|Providers of ancillary services|226 245 234 294 277 231 249 251 340 465 4,520 379 335 269
MHP.5|Retail sale and other providers of medical goods|1,909 2,129 2,374 2,921 3,344 3,520 3,699 4,328 3,863 4,115 4,724 5,629 6,966 7,636
MHP.6|Provision and administration of public health programmes|1,136 1,467 1,166 1,429 1,511 1,682 1,602 1,393 1,787 2,713 2,932 2,728 2,072 2,161
MHP.7|Providers of health care system administration and financing|4,674 3,961 4,096 4,003 4,441 3,683 4,974 5,175 5,536 6,221 7,054 6,749 8,396 8,640
MHP.8|Other industries (rest of the Malaysian economy)|2,830 2,966 3,285 3,310 3,348 3,534 3,425 3,661 3,395 3,984 4,066 3,194 3,245 3,486
MHP.9|Rest of the world|102 86 7 11 19 15 22 28 18 12 9 11 10 12"""
provp = """MHP.1|x|51.83 53.35 52.73 53.00 53.26 54.35 53.99 54.30 55.30 53.99 50.02 53.58 54.06 54.24
MHP.2|x|0.04 0.05 0.00 0.00 0.00 0.01 0.00 0.01 0.00 0.01 0.00 0.01 0.03 0.02
MHP.3|x|17.87 19.08 20.46 21.41 20.89 21.18 21.14 21.08 21.39 20.35 20.33 22.40 20.53 21.02
MHP.4|x|0.63 0.62 0.56 0.63 0.55 0.45 0.44 0.42 0.53 0.68 5.75 0.49 0.40 0.30
MHP.5|x|5.31 5.40 5.70 6.24 6.68 6.80 6.58 7.18 6.03 6.03 6.01 7.23 8.41 8.50
MHP.6|x|3.16 3.72 2.80 3.06 3.02 3.25 2.85 2.31 2.79 3.97 3.73 3.50 2.50 2.41
MHP.7|x|13.00 10.04 9.84 8.56 8.87 7.11 8.85 8.58 8.64 9.12 8.97 8.67 10.13 9.62
MHP.8|x|7.87 7.52 7.89 7.08 6.69 6.82 6.10 6.07 5.30 5.84 5.17 4.10 3.92 3.88
MHP.9|x|0.28 0.22 0.02 0.02 0.04 0.03 0.04 0.05 0.03 0.02 0.01 0.01 0.01 0.01"""
provpub = """MHP.1|x|11,357 13,350 13,706 15,762 16,441 16,681 17,721 18,934 20,319 20,712 22,814 23,582 24,592 26,296
MHP.2|x|2 2 1 1 1 1 1 1 1 2 1 1 16 14
MHP.3|x|2,591 3,032 3,417 4,004 4,206 4,388 4,780 5,354 5,945 6,405 7,666 7,674 7,037 8,171
MHP.4|x|154 159 137 182 199 183 196 199 225 371 4,459 321 278 210
MHP.5|x|135 168 202 220 286 283 304 182 172 243 238 293 335 443
MHP.6|x|1,125 1,449 1,163 1,427 1,488 1,652 1,584 1,373 1,783 2,381 2,850 2,714 2,063 2,144
MHP.7|x|3,207 2,332 2,753 2,692 2,871 1,967 3,268 3,599 4,073 4,372 4,569 5,300 6,891 6,862
MHP.8|x|1,680 1,513 1,487 1,632 1,550 1,618 1,451 1,753 1,699 2,173 2,361 1,423 1,367 1,438
MHP.9|x|1 1 1 1 4 2 1 1 1 1 1 1 1 1"""
PUB = "20,251 22,007 22,868 25,921 27,046 26,774 29,306 31,397 34,217 36,659 44,960 41,308 42,579 45,580"
pv, pvp = table(prov, TEH, pct=provp)
pb, _ = table(provpub, PUB)
pbd = {k[0]: v for k, v in pb.items()}
short = {'MHP.1': 'Hospitals', 'MHP.2': 'Nursing homes', 'MHP.3': 'Clinics', 'MHP.4': 'Labs, imaging, ambulance',
         'MHP.5': 'Pharmacies and medical shops', 'MHP.6': 'Public health programmes', 'MHP.7': 'Administration and insurers',
         'MHP.8': 'Other industries', 'MHP.9': 'Overseas providers'}
rows = []
for (code, name), vals in pv.items():
    for i, y in enumerate(Y):
        rows.append(dict(year=y, code=code, provider=name, short_label=short[code], total_rm_mil=vals[i], pct_teh=pvp[code][i], public_rm_mil=pbd[code][i]))
write('mnha_providers_2011_2024.csv', rows)

# T7.1b / T7.1c functions (+ T5.2.4b public)
fn = """MHC.1|Curative care|23,238 26,172 27,191 31,405 32,947 34,656 37,882 40,416 42,665 42,675 45,002 50,167 52,068 56,554
MHC.2|Rehabilitative care|1 <1 n/a n/a n/a n/a n/a n/a n/a n/a n/a 115 193 182
MHC.3|Long-term care|33 41 26 44 40 46 45 50 49 52 49 52 69 70
MHC.4|Ancillary services to health care|296 314 407 380 359 313 339 343 361 311 228 327 344 252
MHC.5|Medical goods|2,242 2,477 2,730 3,298 3,927 4,191 4,404 5,039 4,572 4,621 5,455 6,482 7,837 8,560
MHC.6|Preventive care|1,224 1,535 2,375 2,304 2,860 2,876 2,971 3,212 3,980 5,178 10,932 5,394 4,717 5,067
MHC.7|Governance and health system and financing administration|3,614 3,523 3,561 4,205 4,347 3,720 4,670 4,311 5,077 5,725 6,277 5,601 7,273 7,211
MHR.1|Gross capital formation|2,430 2,355 2,089 1,831 2,173 2,402 2,405 3,181 3,884 6,216 7,755 6,731 7,162 8,475
MHR.2|Education and training of health personnel|2,463 2,560 2,749 2,758 2,833 2,971 2,856 3,112 3,086 2,921 2,273 2,414 2,538 2,784
MHR.3|Research and development in health|58 81 90 87 98 75 70 93 147 274 364 287 330 325
MHR.4|Drinking water intervention|353 390 429 467 481 527 539 527 264 279 270 281 316 348"""
fnp = """MHC.1|x|64.63 66.35 65.29 67.13 65.81 66.94 67.43 67.04 66.58 62.53 57.25 64.44 62.85 62.96
MHC.2|x|0.00 0.00 n/a n/a n/a n/a n/a n/a n/a n/a n/a 0.15 0.23 0.20
MHC.3|x|0.09 0.10 0.06 0.09 0.08 0.09 0.08 0.08 0.08 0.08 0.06 0.07 0.08 0.08
MHC.4|x|0.82 0.80 0.98 0.81 0.72 0.60 0.60 0.57 0.56 0.46 0.29 0.42 0.42 0.28
MHC.5|x|6.24 6.28 6.56 7.05 7.84 8.09 7.84 8.36 7.13 6.77 6.94 8.33 9.46 9.53
MHC.6|x|3.40 3.89 5.70 4.92 5.71 5.55 5.29 5.33 6.21 7.59 13.91 6.93 5.69 5.64
MHC.7|x|10.05 8.93 8.55 8.99 8.68 7.18 8.31 7.15 7.92 8.39 7.99 7.19 8.78 8.03
MHR.1|x|6.76 5.97 5.02 3.92 4.34 4.64 4.28 5.28 6.06 9.11 9.87 8.65 8.64 9.43
MHR.2|x|6.85 6.49 6.60 5.90 5.66 5.74 5.08 5.16 4.82 4.28 2.89 3.10 3.06 3.10
MHR.3|x|0.16 0.21 0.22 0.19 0.20 0.14 0.12 0.15 0.23 0.40 0.46 0.37 0.40 0.36
MHR.4|x|0.98 0.99 1.03 1.00 0.96 1.02 0.96 0.87 0.41 0.41 0.34 0.36 0.38 0.39"""
fnpub = """MHC.1|x|12,950 15,021 15,013 17,719 18,722 19,143 20,752 22,395 23,093 22,260 23,709 25,441 25,404 27,270
MHC.2|x|0 0 0 0 0 0 0 0 0 0 0 115 193 182
MHC.3|x|19 23 25 43 40 42 45 47 49 48 49 49 63 62
MHC.4|x|224 228 310 268 281 265 287 291 246 249 180 273 289 194
MHC.5|x|107 138 169 183 287 283 304 183 172 148 236 292 335 443
MHC.6|x|912 1,104 1,870 1,729 1,941 2,004 2,147 2,347 3,319 4,521 10,273 5,083 4,337 4,612
MHC.7|x|2,147 1,894 2,217 2,894 2,776 2,004 2,964 2,734 3,614 3,875 3,792 4,152 5,768 5,433
MHR.1|x|2,179 2,038 1,817 1,488 1,455 1,433 1,376 1,656 1,967 3,932 5,449 4,718 4,931 6,023
MHR.2|x|1,584 1,407 1,288 1,430 1,413 1,464 1,308 1,615 1,549 1,327 888 880 907 974
MHR.3|x|46 56 67 58 59 51 52 57 138 237 325 246 281 276
MHR.4|x|84 97 91 109 73 84 72 73 71 61 60 61 72 110"""
f, fp = table(fn, TEH, pct=fnp)
fb, _ = table(fnpub, PUB)
fbd = {k[0]: v for k, v in fb.items()}
plain = {'MHC.1': 'Treating illness', 'MHC.2': 'Rehabilitation', 'MHC.3': 'Long-term care', 'MHC.4': 'Lab tests, imaging, ambulance',
         'MHC.5': 'Medicines and medical goods', 'MHC.6': 'Prevention', 'MHC.7': 'Administration',
         'MHR.1': 'Buildings and equipment', 'MHR.2': 'Training health workers', 'MHR.3': 'Research', 'MHR.4': 'Clean drinking water'}
rows = []
for (code, name), vals in f.items():
    for i, y in enumerate(Y):
        rows.append(dict(year=y, code=code, function=name, plain_label=plain[code], total_rm_mil=vals[i], pct_teh=fp[code][i], public_rm_mil=fbd[code][i]))
write('mnha_functions_2011_2024.csv', rows)

# T9.2c / T9.2d household out-of-pocket by provider
oop = """P|Private hospitals|5,359 5,613 5,736 6,034 6,600 7,519 8,424 9,261 9,993 11,332 11,741 12,089 13,677 15,339
P|Private medical clinics|2,272 2,654 3,055 3,767 3,181 3,433 3,841 3,946 4,593 4,724 5,227 6,785 6,840 7,299
P|Private pharmacies|1,407 1,580 1,842 2,360 2,625 2,711 2,842 3,579 3,113 3,161 3,659 4,220 5,503 5,999
P|Private dental clinics|509 560 592 646 851 911 1,011 1,076 1,127 1,080 1,176 1,383 1,457 1,561
P|Retail sale and other suppliers of medical goods & appliances|321 326 325 334 420 511 543 556 558 637 816 1,087 1,104 1,170
P|Traditional and complementary medicine (TCM) providers|394 412 424 452 531 617 645 647 641 604 664 773 785 832
P|Private medical and diagnostic laboratories|43 59 78 108 72 44 46 46 46 42 45 49 50 53
P|All other private sector providers of health care|534 754 869 678 711 744 756 795 871 866 919 962 1,045 1,125
G|Public institutions providing health-related services|324 388 634 638 669 716 724 657 635 692 492 578 601 718
G|Public hospitals|259 253 334 309 372 453 438 420 446 471 416 431 564 695
G|Public medical clinics|45 50 44 48 18 20 18 18 18 55 25 25 31 31
G|Public dental clinics|na na na na 13 14 16 17 20 11 15 18 20 20
G|Provision and administration of public health programmes (MOH)|na na na na na na na na na 2 2 na na na"""
OOPT = "11,466 12,649 13,933 15,373 16,063 17,692 19,305 21,019 22,061 23,676 25,197 28,399 31,678 34,843"
o = {}
for line in oop.splitlines():
    g, n, v = line.split('|'); o[n] = (g, nums(v))
for i, y in enumerate(Y):
    s = sum(v[1][i] for v in o.values() if v[1][i] is not None)
    assert abs(s - nums(OOPT)[i]) <= 2, ('oop', y, s)
oshort = {'Retail sale and other suppliers of medical goods & appliances': 'Medical goods shops',
          'Traditional and complementary medicine (TCM) providers': 'Traditional medicine',
          'Private medical and diagnostic laboratories': 'Private labs',
          'All other private sector providers of health care': 'Other private providers',
          'Public institutions providing health-related services': 'Other public institutions',
          'Provision and administration of public health programmes (MOH)': 'MOH public health programmes'}
rows = []
for n, (g, vals) in o.items():
    for i, y in enumerate(Y):
        rows.append(dict(year=y, provider=n, short_label=oshort.get(n, n), sector='Private' if g == 'P' else 'Public', rm_mil=vals[i]))
write('mnha_oop_providers_2011_2024.csv', rows)

# T9.3a household out-of-pocket by function
oopf = """x|Out-patient services|5,145 5,709 6,206 7,067 6,945 7,355 8,240 8,703 9,621 10,010 10,777 12,564 13,114 14,187
x|In-patient services|2,786 2,831 2,976 3,056 2,977 3,592 4,001 3,967 4,240 5,253 5,226 5,636 6,542 7,424
x|Pharmaceuticals|1,407 1,580 1,842 2,360 2,625 2,711 2,842 3,579 3,113 3,161 3,659 4,220 5,503 5,999
x|Health education & training|789 1,066 1,424 1,244 1,346 1,450 1,476 1,434 1,477 1,525 1,319 1,462 1,561 1,752
x|Medical appliances & non-durable goods|384 394 398 413 596 700 753 779 794 860 1,062 1,376 1,401 1,487
x|Day-care services|328 338 374 409 331 361 399 456 366 403 436 521 659 825
x|Traditional and complementary medicine (TCM)|298 310 317 335 407 482 495 488 474 447 489 565 574 606
x|All other functions|329 421 396 489 836 1,041 1,098 1,613 1,977 2,017 2,229 2,055 2,324 2,561"""
of, _ = table(oopf, OOPT)
rows = []
for (_, name), vals in of.items():
    for i, y in enumerate(Y):
        rows.append(dict(year=y, function=name, rm_mil=vals[i]))
write('mnha_oop_functions_2011_2024.csv', rows)
print('ALL CHECKS PASSED')
