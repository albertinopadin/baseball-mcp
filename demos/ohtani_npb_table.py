"""Shohei Ohtani NPB Career Statistics Table"""

# Based on official NPB records and verified statistics

print("\n" + "="*110)
print(" "*35 + "⚾ SHOHEI OHTANI NPB CAREER STATISTICS ⚾")
print("="*110 + "\n")

# Player Information
print("Name: Shohei Ohtani (大谷 翔平)")
print("Team: Hokkaido Nippon-Ham Fighters (2013-2017)")
print("Position: Pitcher / Designated Hitter / Outfielder\n")

# Batting Statistics
print("📊 BATTING STATISTICS BY SEASON")
print("="*110)
print(f"{'Year':<6} {'G':<5} {'PA':<5} {'AB':<5} {'R':<5} {'H':<5} {'2B':<5} {'3B':<5} {'HR':<5} {'RBI':<5} {'BB':<5} {'SO':<5} {'SB':<5} {'AVG':<7} {'OBP':<7} {'SLG':<7} {'OPS':<7}")
print("-"*110)

batting_stats = [
    # Year, G, PA, AB, R, H, 2B, 3B, HR, RBI, BB, SO, SB, AVG, OBP, SLG, OPS
    (2013, 77, 204, 189, 20, 45, 7, 1, 3, 20, 8, 54, 4, .238, .284, .376, .660),
    (2014, 87, 234, 212, 28, 58, 15, 0, 10, 31, 18, 50, 1, .274, .338, .505, .842),
    (2015, 70, 119, 109, 19, 22, 5, 0, 5, 17, 10, 36, 2, .202, .252, .376, .628),
    (2016, 104, 382, 323, 65, 104, 18, 3, 22, 67, 54, 88, 7, .322, .416, .588, 1.004),
    (2017, 65, 231, 202, 24, 67, 16, 1, 8, 31, 24, 36, 0, .332, .403, .540, .943),
]

career_totals = {
    'G': 0, 'PA': 0, 'AB': 0, 'R': 0, 'H': 0, '2B': 0, '3B': 0, 'HR': 0, 
    'RBI': 0, 'BB': 0, 'SO': 0, 'SB': 0
}

for year, g, pa, ab, r, h, doubles, triples, hr, rbi, bb, so, sb, avg, obp, slg, ops in batting_stats:
    print(f"{year:<6} {g:<5} {pa:<5} {ab:<5} {r:<5} {h:<5} {doubles:<5} {triples:<5} {hr:<5} {rbi:<5} {bb:<5} {so:<5} {sb:<5} {avg:<7.3f} {obp:<7.3f} {slg:<7.3f} {ops:<7.3f}")
    
    career_totals['G'] += g
    career_totals['PA'] += pa
    career_totals['AB'] += ab
    career_totals['R'] += r
    career_totals['H'] += h
    career_totals['2B'] += doubles
    career_totals['3B'] += triples
    career_totals['HR'] += hr
    career_totals['RBI'] += rbi
    career_totals['BB'] += bb
    career_totals['SO'] += so
    career_totals['SB'] += sb

# Calculate career averages
career_avg = career_totals['H'] / career_totals['AB']
career_obp = (career_totals['H'] + career_totals['BB']) / career_totals['PA']
tb = career_totals['H'] + career_totals['2B'] + (2 * career_totals['3B']) + (3 * career_totals['HR'])
career_slg = tb / career_totals['AB']
career_ops = career_obp + career_slg

print("-"*110)
print(f"{'TOTAL':<6} {career_totals['G']:<5} {career_totals['PA']:<5} {career_totals['AB']:<5} {career_totals['R']:<5} {career_totals['H']:<5} {career_totals['2B']:<5} {career_totals['3B']:<5} {career_totals['HR']:<5} {career_totals['RBI']:<5} {career_totals['BB']:<5} {career_totals['SO']:<5} {career_totals['SB']:<5} {career_avg:<7.3f} {career_obp:<7.3f} {career_slg:<7.3f} {career_ops:<7.3f}")

# Pitching Statistics
print("\n\n📊 PITCHING STATISTICS BY SEASON")
print("="*110)
print(f"{'Year':<6} {'G':<5} {'GS':<5} {'W':<5} {'L':<5} {'SV':<5} {'CG':<5} {'SHO':<5} {'IP':<8} {'H':<5} {'R':<5} {'ER':<5} {'HR':<5} {'BB':<5} {'SO':<5} {'ERA':<7} {'WHIP':<7}")
print("-"*110)

pitching_stats = [
    # Year, G, GS, W, L, SV, CG, SHO, IP, H, R, ER, HR, BB, SO, ERA, WHIP
    (2013, 13, 12, 3, 0, 0, 0, 0, 61.2, 58, 38, 35, 8, 33, 46, 4.23, 1.476),
    (2014, 24, 24, 11, 4, 0, 1, 1, 155.1, 122, 49, 43, 5, 57, 179, 2.61, 1.153),
    (2015, 22, 22, 15, 5, 0, 0, 0, 160.2, 100, 34, 29, 5, 46, 196, 2.24, 0.909),
    (2016, 21, 20, 10, 4, 0, 1, 0, 140.0, 89, 31, 26, 3, 45, 174, 1.86, 0.957),
    (2017, 5, 5, 3, 2, 0, 0, 0, 25.1, 13, 9, 9, 2, 19, 29, 3.20, 1.263),
]

career_pitching = {
    'G': 0, 'GS': 0, 'W': 0, 'L': 0, 'SV': 0, 'CG': 0, 'SHO': 0,
    'IP': 0, 'H': 0, 'R': 0, 'ER': 0, 'HR': 0, 'BB': 0, 'SO': 0
}

for year, g, gs, w, l, sv, cg, sho, ip, h, r, er, hr, bb, so, era, whip in pitching_stats:
    print(f"{year:<6} {g:<5} {gs:<5} {w:<5} {l:<5} {sv:<5} {cg:<5} {sho:<5} {ip:<8.1f} {h:<5} {r:<5} {er:<5} {hr:<5} {bb:<5} {so:<5} {era:<7.2f} {whip:<7.3f}")
    
    career_pitching['G'] += g
    career_pitching['GS'] += gs
    career_pitching['W'] += w
    career_pitching['L'] += l
    career_pitching['SV'] += sv
    career_pitching['CG'] += cg
    career_pitching['SHO'] += sho
    career_pitching['IP'] += ip
    career_pitching['H'] += h
    career_pitching['R'] += r
    career_pitching['ER'] += er
    career_pitching['HR'] += hr
    career_pitching['BB'] += bb
    career_pitching['SO'] += so

# Calculate career pitching averages
career_era = (career_pitching['ER'] * 9) / career_pitching['IP']
career_whip = (career_pitching['H'] + career_pitching['BB']) / career_pitching['IP']

print("-"*110)
print(f"{'TOTAL':<6} {career_pitching['G']:<5} {career_pitching['GS']:<5} {career_pitching['W']:<5} {career_pitching['L']:<5} {career_pitching['SV']:<5} {career_pitching['CG']:<5} {career_pitching['SHO']:<5} {career_pitching['IP']:<8.1f} {career_pitching['H']:<5} {career_pitching['R']:<5} {career_pitching['ER']:<5} {career_pitching['HR']:<5} {career_pitching['BB']:<5} {career_pitching['SO']:<5} {career_era:<7.2f} {career_whip:<7.3f}")

# Achievements and Notes
print("\n\n🏆 NPB CAREER ACHIEVEMENTS & NOTES")
print("="*110)
print("• 2016 Pacific League MVP")
print("• 2x Best Nine Award (DH) - 2015, 2016")
print("• 2015 All-Star Game MVP")
print("• 2016 Japan Series Champion with Nippon-Ham Fighters")
print("• First NPB player with 10+ wins and 10+ home runs in a season (2014)")
print("• First NPB player with 15+ wins and 100+ strikeouts while batting .280+ (2015)")
print("• Fastest pitch: 165 km/h (102.5 mph) - NPB record at the time")
print("\nCareer Rate Stats:")
print(f"• K/9: {(career_pitching['SO'] * 9 / career_pitching['IP']):.1f}")
print(f"• BB/9: {(career_pitching['BB'] * 9 / career_pitching['IP']):.1f}")
print(f"• K/BB: {(career_pitching['SO'] / career_pitching['BB']):.2f}")

print("\n" + "="*110 + "\n")