"""MOH operating budget allocation vs expenditure by programme, from MOH Annual Reports 2020-2025 (Finance chapter, Table 3.1 / 4.1 / 3.7).
Values in RM exactly as published. Check: programmes sum to the published total."""
import csv, os
data = {
2020: ("Table 3.1, MOH Annual Report 2020", 26052530900, 27010594516, [
 ("Management",1932770800,1918203399),("Medical",14229062747,14751856537),("Public Health",5747911239,6158221536),
 ("Oral Health",979350458,1003537403),("Pharmaceutical Services",210417616,212487238),("Research and Technical Support",334113153,329894992),
 ("Food Safety and Quality",93039587,99491543),("Special Programme",2525865300,2536901868)]),
2021: ("Table 3.1, MOH Annual Report 2021", 22835325600, 24650411189, [
 ("Management",1874394149,1861785570),("Medical",11379579785,12097248814),("Public Health",5031878598,5666706554),
 ("Oral Health",977037796,1043806374),("Pharmaceutical Services",207142091,211418117),("Research and Technical Support",344225079,332660489),
 ("Food Safety and Quality",95918602,103440283),("Special Programme",2925149500,3333344988)]),
2022: ("Table 4.1, MOH Annual Report 2022", 28030000000, 30265662227, [
 ("Medical",11671740451,12250121911),("Special Programme",5892396730,6984627719),("Public Health",5310457746,5667262973),
 ("Management",1988470274,1915859819),("Financial Commitment",1400000000,1692134715),("Oral Health",1072967874,1075367923),
 ("Research and Technical Support",365633169,354333137),("Pharmaceutical Services",222061135,220910892),("Food Safety and Quality",106272621,105043138)]),
2023: ("Table 3.1, MOH Annual Report 2023", 31500000000, 32193223023, [
 ("Medical",11960070390,13147980510),("Special Programme",6813106080,7291769819),("Public Health",5534712000,5966445101),
 ("Management",2117587090,2294748909),("New Policy",1722420000,None),("Financial Commitment",1600000000,1618652715),
 ("Oral Health",1055819660,1167043962),("Research and Technical Support",371149600,369975978),("Pharmaceutical Services",219057200,227923919),
 ("Food Safety and Quality",106077980,108682109)]),
2024: ("Table 3.1, MOH Annual Report 2024", 35150181800, 33957216274, [
 ("Medical",14153378308,14019785759),("Special Programme",8044523300,7357139915),("Public Health",6415729100,6381635570),
 ("Management",2569856800,2270639330),("New Policy",123000000,122256605),("Financial Commitment",1800000000,1785825493),
 ("Oral Health",1256323711,1250913138),("Research and Technical Support",424009289,410233084),("Pharmaceutical Services",246354400,244140605),
 ("Food Safety and Quality",117006892,114646776)]),
2025: ("Table 3.7, MOH Annual Report 2025 (amended allocation as of 31 Dec 2025)", 37134087200, 36131258777, [
 ("Management",2831970050,2453981812),("Medical",15208670971,15094783088),("Public Health",6960236600,6917435858),
 ("Oral Health",1373006482,1371895938),("Pharmaceutical Services",263113700,260991176),("Research and Technical Support",433320118,408421353),
 ("Food Safety and Quality",125476629,123491550),("Special Programme",7677932650,7380796685),("New Policy",200560000,61304679),
 ("One-off",9800000,9315187),("Financial Commitment",2050000000,2048841450)]),
}
core = {"Medical","Public Health","Oral Health","Pharmaceutical Services","Research and Technical Support","Food Safety and Quality","Management"}
rows = []
for y,(src,ta,te,progs) in data.items():
    sa = sum(p[1] for p in progs); se = sum(p[2] or 0 for p in progs)
    assert abs(sa-ta) <= 2 and abs(se-te) <= 2, (y, sa-ta, se-te)
    for name,al,ex in progs:
        rows.append(dict(year=y, programme=name, group=name if name in core else "Other (special, new policy, commitments)",
                         allocation_rm=al, expenditure_rm='' if ex is None else ex, source=src))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'moh_programme_budget_2020_2025.csv'), 'w', newline='') as f:
    w=csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n'); w.writeheader(); w.writerows(rows)
print(len(rows),'rows; totals match published totals for every year')
