with open('zuz.py', encoding='utf-8') as f: lines = [line.expandtabs(4) for line in f.readlines()]
open('fixed_zuz_fixed_tabs_v2_final_clean.py', 'w').write(''.join(lines))
print("Tabs fixed and written to fixed_zuz_fixed_tabs_v2_final_clean.py")
