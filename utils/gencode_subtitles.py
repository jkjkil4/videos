
lines: list[str] = []
i = 1

while line := input(f'In[{i}]: '):
    lines.append(line)
    i += 1

no = int(input('No. '))

for i, line in enumerate(lines, start=no):
    quoted = line.replace("'", r"\'")
    print(f't = self.aas(\'{i}.mp3\', \'{quoted}\')')
    print('self.forward_to(t.end)')
