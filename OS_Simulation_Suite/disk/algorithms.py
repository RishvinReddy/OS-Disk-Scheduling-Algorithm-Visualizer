def fcfs(requests, head):
    seq = [head] + requests
    return seq

def sstf(requests, head):
    req = requests.copy()
    seq = [head]
    curr = head
    while req:
        closest = min(req, key=lambda x: abs(x - curr))
        curr = closest
        seq.append(curr)
        req.remove(closest)
    return seq

def scan(requests, head, direction="Right", disk_size=200):
    left = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])
    seq = [head]
    if direction == "Right":
        seq += right
        if right and right[-1] != disk_size - 1:
             seq.append(disk_size - 1)
        elif not right:
             seq.append(disk_size - 1)
        seq += left[::-1]
    else:
        seq += left[::-1]
        if left and left[0] != 0:
             seq.append(0)
        elif not left:
             seq.append(0)
        seq += right
    return seq

def c_scan(requests, head, direction="Right", disk_size=200):
    left = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])
    seq = [head]
    if direction == "Right":
        seq += right
        seq += [disk_size - 1, 0]
        seq += left
    else:
        seq += left[::-1]
        seq += [0, disk_size - 1]
        seq += right[::-1]
    return seq

def look(requests, head, direction="Right"):
    left = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])
    seq = [head]
    if direction == "Right":
        seq += right + left[::-1]
    else:
        seq += left[::-1] + right
    return seq

def c_look(requests, head, direction="Right"):
    left = sorted([r for r in requests if r < head])
    right = sorted([r for r in requests if r >= head])
    seq = [head]
    if direction == "Right":
        seq += right + left
    else:
        seq += left[::-1] + right[::-1]
    return seq

def run_algorithm(algo, requests, head, direction="Right", disk_size=200):
    if algo == "FCFS":
        return fcfs(requests, head)
    elif algo == "SSTF":
        return sstf(requests, head)
    elif algo == "SCAN":
        return scan(requests, head, direction, disk_size)
    elif algo == "C-SCAN":
        return c_scan(requests, head, direction, disk_size)
    elif algo == "LOOK":
        return look(requests, head, direction)
    elif algo == "C-LOOK":
        return c_look(requests, head, direction)
    return [head]
