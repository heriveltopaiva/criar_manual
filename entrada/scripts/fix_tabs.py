import sys
with open('zuz.py', encoding='utf-8') as f: lines = f.readlines()

fixed_lines = []
for i, line in enumerate(lines): num = i + 1; if (93 <= num <= 94): fixed_lines.append(line.expandtabs(0).replace('\t', ' '*4)); else: fixed_lines.append(line)

with open('zuz.py.fixed', 'w') as f: f.writelines(fixed_lines); print("Fixed file written to zuz.py.fixed")
FIXPY && python3 fix_tabs.py && ls -l *.fixed 2>/dev/null || echo "Script executed, checking output..."
__ollama_status=$?
pwd -P > '/tmp/ollama-agent-cwd-682951872'
exit $__ollama_status
