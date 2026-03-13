// Initialize Chart JS
let diskChart = null;

function parseQueue(queueStr, maxCylinders) {
    return queueStr.split(',')
        .map(n => parseInt(n.trim(), 10))
        .filter(n => !isNaN(n) && n >= 0 && n <= maxCylinders);
}

function initChart() {
    const ctx = document.getElementById('diskChart').getContext('2d');

    // Set global defaults for premium look
    Chart.defaults.color = '#475569';
    Chart.defaults.font.family = "'Inter', sans-serif";

    diskChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Disk Head Path',
                data: [],
                borderColor: '#0ea5e9',
                backgroundColor: 'rgba(14, 165, 233, 0.15)',
                borderWidth: 3,
                pointBackgroundColor: '#f43f5e',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 8,
                fill: true,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            plugins: {
                legend: {
                    display: true,
                    labels: { color: '#0f172a', font: { size: 13, weight: 600 } }
                },
                tooltip: {
                    backgroundColor: 'rgba(255, 255, 255, 0.9)',
                    titleColor: '#0f172a',
                    bodyColor: '#475569',
                    borderColor: 'rgba(0,0,0,0.1)',
                    borderWidth: 1,
                    padding: 12,
                    cornerRadius: 8,
                    displayColors: false
                }
            },
            scales: {
                x: {
                    title: { display: true, text: 'Cylinder Number', color: '#475569', font: { size: 13 } },
                    grid: { color: 'rgba(0, 0, 0, 0.05)' },
                    ticks: { color: '#a1a1aa' }
                },
                y: {
                    reverse: true // Start from top and go down
                }
            },
            animation: {
                x: {
                    type: 'number',
                    easing: 'linear',
                    duration: 1500,
                    from: NaN, // the point is initially skipped
                    delay(ctx) {
                        if (ctx.type !== 'data' || ctx.xStarted) {
                            return 0;
                        }
                        ctx.xStarted = true;
                        return ctx.index * 150; // stagger line draw
                    }
                },
                y: {
                    type: 'number',
                    easing: 'linear',
                    duration: 1500,
                    from: (ctx) => { return ctx.index === 0 ? ctx.chart.scales.y.getPixelForValue(100) : ctx.chart.getDatasetMeta(ctx.datasetIndex).data[ctx.index - 1].getProps(['y'], true).y; },
                    delay(ctx) {
                        if (ctx.type !== 'data' || ctx.yStarted) {
                            return 0;
                        }
                        ctx.yStarted = true;
                        return ctx.index * 150;
                    }
                }
            }
        }
    });
}

function updateChart(sequence, maxCylinders) {
    const labels = sequence.map((_, i) => i.toString());

    diskChart.data.labels = labels;
    diskChart.data.datasets[0].data = sequence;
    diskChart.options.scales.x.max = maxCylinders;
    diskChart.options.scales.x.min = 0;

    diskChart.update();
}

function calculateSeekTime(sequence) {
    let seek = 0;
    for (let i = 1; i < sequence.length; i++) {
        seek += Math.abs(sequence[i] - sequence[i - 1]);
    }
    return seek;
}

// ------ ALGORITHMS ------

function fcfs(queue, head) {
    const sequence = [head, ...queue];
    return sequence;
}

function sstf(queue, head) {
    const sequence = [head];
    let current = head;
    let pending = [...queue];

    while (pending.length > 0) {
        let closestIdx = 0;
        let minDiff = Math.abs(current - pending[0]);

        for (let i = 1; i < pending.length; i++) {
            const diff = Math.abs(current - pending[i]);
            if (diff < minDiff) {
                minDiff = diff;
                closestIdx = i;
            }
        }

        current = pending[closestIdx];
        sequence.push(current);
        pending.splice(closestIdx, 1);
    }
    return sequence;
}

function scan(queue, head, maxCylinders, direction) {
    let sequence = [head];
    let pending = [...queue];
    pending.sort((a, b) => a - b); // Sort ascending

    let left = pending.filter(x => x < head);
    let right = pending.filter(x => x >= head);

    if (direction === 'high') {
        sequence = sequence.concat(right);
        if (right.length > 0) sequence.push(maxCylinders); // Hit end
        sequence = sequence.concat(left.reverse()); // Go back down
    } else {
        sequence = sequence.concat(left.reverse());
        if (left.length > 0) sequence.push(0); // Hit 0
        sequence = sequence.concat(right); // Go up
    }

    return sequence;
}

function cscan(queue, head, maxCylinders, direction) {
    let sequence = [head];
    let pending = [...queue];
    pending.sort((a, b) => a - b); // Sort ascending

    let left = pending.filter(x => x < head);
    let right = pending.filter(x => x >= head);

    if (direction === 'high') {
        sequence = sequence.concat(right);
        sequence.push(maxCylinders); // Hit end
        sequence.push(0); // Jump to beginning (circular)
        sequence = sequence.concat(left);
    } else {
        sequence = sequence.concat(left.reverse());
        sequence.push(0); // Hit end
        sequence.push(maxCylinders); // Jump to high end
        sequence = sequence.concat(right.reverse());
    }

    return sequence;
}

function look(queue, head, direction) {
    let sequence = [head];
    let pending = [...queue];
    pending.sort((a, b) => a - b);

    let left = pending.filter(x => x < head);
    let right = pending.filter(x => x >= head);

    if (direction === 'high') {
        sequence = sequence.concat(right); // No hitting max end
        sequence = sequence.concat(left.reverse());
    } else {
        sequence = sequence.concat(left.reverse()); // No hitting 0
        sequence = sequence.concat(right);
    }

    return sequence;
}

function clook(queue, head, direction) {
    let sequence = [head];
    let pending = [...queue];
    pending.sort((a, b) => a - b);

    let left = pending.filter(x => x < head);
    let right = pending.filter(x => x >= head);

    if (direction === 'high') {
        sequence = sequence.concat(right);
        // Jump to lowest request, do NOT hit 0
        sequence = sequence.concat(left);
    } else {
        sequence = sequence.concat(left.reverse());
        // Jump to highest request, do NOT hit maxCylinders
        sequence = sequence.concat(right.reverse());
    }

    return sequence;
}

// ------ MAIN EXECUTION ------

function runSimulation() {
    const alg = document.getElementById('algorithm').value;
    const maxCylinders = parseInt(document.getElementById('max-cylinders').value, 10);
    const head = parseInt(document.getElementById('head').value, 10);
    const direction = document.getElementById('direction').value;
    const queueStr = document.getElementById('queue').value;

    const queue = parseQueue(queueStr, maxCylinders);

    let sequence = [];
    switch (alg) {
        case 'fcfs': sequence = fcfs(queue, head); break;
        case 'sstf': sequence = sstf(queue, head); break;
        case 'scan': sequence = scan(queue, head, maxCylinders, direction); break;
        case 'cscan': sequence = cscan(queue, head, maxCylinders, direction); break;
        case 'look': sequence = look(queue, head, direction); break;
        case 'clook': sequence = clook(queue, head, direction); break;
    }

    // Filter consecutive duplicates cleanly (like 0, 0 if queue hits edge exactly)
    sequence = sequence.filter((val, idx, arr) => idx === 0 || val !== arr[idx - 1]);

    const totalSeek = calculateSeekTime(sequence);
    const avgSeek = queue.length > 0 ? (totalSeek / queue.length).toFixed(2) : 0;

    // Update UI
    document.getElementById('total-seek').innerText = totalSeek;
    document.getElementById('avg-seek').innerText = avgSeek;
    document.getElementById('seek-sequence').innerText = sequence.join(" -> ");

    // Update Chart
    updateChart(sequence, maxCylinders);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    initChart();
    // Initialize CPU processes
    addProcessRow();
    addProcessRow();
    addProcessRow();

    // Initialize Banker's Grid
    if (document.getElementById('bankers-tables-container')) {
        generateBankersTables();
    }
});

// ==========================================
// BANKER'S ALGORITHM LOGIC
// ==========================================

function generateBankersTables() {
    const numP = parseInt(document.getElementById('num-processes').value, 10);
    const numR = parseInt(document.getElementById('num-resources').value, 10);

    const container = document.getElementById('bankers-tables-container');
    const totalResContainer = document.getElementById('total-resources-container');

    // Total Resources Input
    let totalHtml = '';
    for (let j = 0; j < numR; j++) {
        let resName = String.fromCharCode(65 + j); // A, B, C...
        totalHtml += `
            <div style="flex: 1; min-width: 60px;">
                <label style="font-size: 0.8rem;">${resName}</label>
                <input type="number" id="tot-res-${j}" class="process-input" style="width: 100%;" value="${Math.floor(Math.random() * 5) + 5}" min="0">
            </div>
        `;
    }
    totalResContainer.innerHTML = totalHtml;

    // Data matrices table
    let ht = `<table class="process-table">
                <thead>
                    <tr>
                        <th rowspan="2" style="vertical-align: middle;">Process</th>
                        <th colspan="${numR}" style="text-align: center; border-right: 1px solid rgba(255,255,255,0.1);">Allocation</th>
                        <th colspan="${numR}" style="text-align: center;">Max Need</th>
                    </tr>
                    <tr>`;
    for (let i = 0; i < 2; i++) {
        for (let j = 0; j < numR; j++) {
            let resName = String.fromCharCode(65 + j);
            ht += `<th style="text-align: center; ${j === numR - 1 && i === 0 ? 'border-right: 1px solid rgba(255,255,255,0.1);' : ''}">${resName}</th>`;
        }
    }
    ht += `</tr></thead><tbody>`;

    for (let i = 0; i < numP; i++) {
        ht += `<tr><td><strong>P${i}</strong></td>`;
        // Allocation
        for (let j = 0; j < numR; j++) {
            ht += `<td style="${j === numR - 1 ? 'border-right: 1px solid rgba(255,255,255,0.1);' : ''} text-align: center;">
                    <input type="number" id="alloc-${i}-${j}" class="process-input" style="width: 50px;" value="${Math.floor(Math.random() * 3)}" min="0">
                   </td>`;
        }
        // Max Need
        for (let j = 0; j < numR; j++) {
            ht += `<td style="text-align: center;">
                    <input type="number" id="max-${i}-${j}" class="process-input" style="width: 50px;" value="${Math.floor(Math.random() * 5) + 2}" min="0">
                   </td>`;
        }
        ht += `</tr>`;
    }
    ht += `</tbody></table>`;
    container.innerHTML = ht;
}

function runBankersSimulation() {
    const numP = parseInt(document.getElementById('num-processes').value, 10);
    const numR = parseInt(document.getElementById('num-resources').value, 10);

    let alloc = [];
    let max = [];
    let total = [];
    let need = [];

    // Get Total Resources
    for (let j = 0; j < numR; j++) {
        total.push(parseInt(document.getElementById(`tot-res-${j}`).value, 10));
    }

    // Get Matrices and calculate Need = Max - Alloc
    for (let i = 0; i < numP; i++) {
        alloc[i] = [];
        max[i] = [];
        need[i] = [];
        for (let j = 0; j < numR; j++) {
            alloc[i][j] = parseInt(document.getElementById(`alloc-${i}-${j}`).value, 10);
            max[i][j] = parseInt(document.getElementById(`max-${i}-${j}`).value, 10);
            need[i][j] = max[i][j] - alloc[i][j];

            if (need[i][j] < 0) {
                alert(`Error: Allocation for P${i} resource ${String.fromCharCode(65 + j)} exceeds Max.`);
                return;
            }
        }
    }

    // Calculate initial available: Available = Total - Sum(Alloc)
    let available = [...total];
    for (let j = 0; j < numR; j++) {
        let sumAlloc = 0;
        for (let i = 0; i < numP; i++) {
            sumAlloc += alloc[i][j];
        }
        available[j] -= sumAlloc;
        if (available[j] < 0) {
            alert(`Error: Total allocated resource ${String.fromCharCode(65 + j)} exceeds total instances in system.`);
            return;
        }
    }

    // Run Safety Algorithm
    let work = [...available];
    let finish = new Array(numP).fill(false);
    let safeSeq = [];
    let workTimeline = [];

    workTimeline.push([...work]); // Initial work

    let count = 0;
    while (count < numP) {
        let found = false;
        for (let p = 0; p < numP; p++) {
            if (finish[p] === false) {
                let canAllocate = true;
                for (let j = 0; j < numR; j++) {
                    if (need[p][j] > work[j]) {
                        canAllocate = false;
                        break;
                    }
                }

                if (canAllocate) {
                    // Execute Process
                    for (let j = 0; j < numR; j++) {
                        work[j] += alloc[p][j];
                    }
                    safeSeq.push(p);
                    workTimeline.push([...work]);
                    finish[p] = true;
                    found = true;
                    count++;
                }
            }
        }

        // If we loop through all and can't find a process to satisfy
        if (found === false) {
            break;
        }
    }

    // Output Results update
    const statusBox = document.getElementById('bankers-result-box');
    const statusText = document.getElementById('safety-status');
    const seqText = document.getElementById('safe-sequence');

    if (count < numP) {
        statusBox.style.borderColor = 'rgba(239, 68, 68, 0.5)';
        statusBox.style.background = 'rgba(239, 68, 68, 0.1)';
        statusText.style.color = '#ef4444';
        statusText.innerText = "System in Unsafe State (Deadlock Risk)";
        let unfinish = [];
        for (let i = 0; i < numP; i++) if (!finish[i]) unfinish.push(`P${i}`);
        seqText.innerText = `Processes unable to complete: ${unfinish.join(', ')}`;
    } else {
        statusBox.style.borderColor = 'rgba(39, 201, 63, 0.5)';
        statusBox.style.background = 'rgba(39, 201, 63, 0.1)';
        statusText.style.color = '#27c93f';
        statusText.innerText = "System is in a Safe State";
        seqText.innerText = `Safe Sequence: < ${safeSeq.map(p => 'P' + p).join(', ')} >`;
    }

    renderNeedMatrix(need, numP, numR);
    renderAvailableTimeline(workTimeline, safeSeq, numP, numR, count);
}

function renderNeedMatrix(need, numP, numR) {
    const container = document.getElementById('need-matrix-container');
    let ht = `<table class="process-table"><thead><tr><th>Process</th>`;
    for (let j = 0; j < numR; j++) ht += `<th style="text-align: center;">${String.fromCharCode(65 + j)}</th>`;
    ht += `</tr></thead><tbody>`;
    for (let i = 0; i < numP; i++) {
        ht += `<tr><td><strong>P${i}</strong></td>`;
        for (let j = 0; j < numR; j++) {
            ht += `<td style="text-align: center; color: var(--accent-pink);">${need[i][j]}</td>`;
        }
        ht += `</tr>`;
    }
    ht += `</tbody></table>`;
    container.innerHTML = ht;
}

function renderAvailableTimeline(timeline, safeSeq, numP, numR, count) {
    const container = document.getElementById('available-sequence-container');
    let ht = `<table class="process-table"><thead><tr><th>Step</th><th>Action</th>`;
    for (let j = 0; j < numR; j++) ht += `<th style="text-align: center;">${String.fromCharCode(65 + j)}</th>`;
    ht += `</tr></thead><tbody>`;

    // Initial state
    ht += `<tr><td>0</td><td style="color: var(--text-secondary);">Initial Available</td>`;
    for (let j = 0; j < numR; j++) ht += `<td style="text-align: center;">${timeline[0][j]}</td>`;
    ht += `</tr>`;

    // Timeline execution
    for (let i = 0; i < safeSeq.length; i++) {
        ht += `<tr><td>${i + 1}</td><td><span style="color: var(--accent-green);">P${safeSeq[i]} Completed</span> (Released Resources)</td>`;
        for (let j = 0; j < numR; j++) {
            ht += `<td style="text-align: center; color: var(--text-primary);">${timeline[i + 1][j]}</td>`;
        }
        ht += `</tr>`;
    }

    if (count < numP) {
        ht += `<tr><td colspan="${numR + 2}" style="text-align: center; color: #ef4444; padding: 1rem;">Process Execution Blocked - Deadlock Condition Met</td></tr>`;
    }

    ht += `</tbody></table>`;
    container.innerHTML = ht;
}

// ==========================================
// CPU SCHEDULING LOGIC
// ==========================================

let processCounter = 1;

function addProcessRow() {
    const tbody = document.getElementById('process-tbody');
    const tr = document.createElement('tr');
    tr.innerHTML = `
        <td>P${processCounter}</td>
        <td><input type="number" class="process-input arrival-time" value="0" min="0"></td>
        <td><input type="number" class="process-input burst-time" value="5" min="1"></td>
        <td><input type="number" class="process-input priority" value="1" min="1"></td>
        <td><button class="btn-remove" onclick="this.closest('tr').remove()"><i class="fas fa-trash"></i></button></td>
    `;
    // Store process ID in a data attribute
    tr.dataset.pid = `P${processCounter}`;
    tbody.appendChild(tr);
    processCounter++;
}

function toggleTimeQuantum() {
    const alg = document.getElementById('cpu-algorithm').value;
    document.getElementById('tq-group').style.display = (alg === 'rr') ? 'block' : 'none';
}

function getProcessesFromTable() {
    const rows = document.querySelectorAll('#process-tbody tr');
    const processes = [];
    rows.forEach(row => {
        processes.push({
            id: row.dataset.pid,
            at: parseInt(row.querySelector('.arrival-time').value, 10),
            bt: parseInt(row.querySelector('.burst-time').value, 10),
            rt: parseInt(row.querySelector('.burst-time').value, 10), // Remaining time
            pr: parseInt(row.querySelector('.priority').value, 10),
            ct: 0,
            tat: 0,
            wt: 0,
            st: -1 // Start time
        });
    });
    return processes;
}

// ------ CPU ALGORITHMS ------

// FCFS
function solveFCFS(processes) {
    let time = 0;
    let gantt = [];
    processes.sort((a, b) => a.at - b.at); // Sort by arrival

    for (let p of processes) {
        if (time < p.at) {
            gantt.push({ id: 'IDLE', start: time, end: p.at });
            time = p.at;
        }
        gantt.push({ id: p.id, start: time, end: time + p.bt });
        p.st = time;
        time += p.bt;
        p.ct = time;
    }
    return gantt;
}

// SJF (Non-Preemptive)
function solveSJF(processes) {
    let time = 0;
    let completed = 0;
    let n = processes.length;
    let gantt = [];
    let is_completed = new Array(n).fill(false);
    processes.sort((a, b) => a.at - b.at);

    while (completed !== n) {
        let idx = -1;
        let min_bt = Infinity;

        for (let i = 0; i < n; i++) {
            if (processes[i].at <= time && is_completed[i] === false) {
                if (processes[i].bt < min_bt) {
                    min_bt = processes[i].bt;
                    idx = i;
                }
                if (processes[i].bt === min_bt) {
                    if (processes[i].at < processes[idx].at) {
                        min_bt = processes[i].bt;
                        idx = i;
                    }
                }
            }
        }

        if (idx !== -1) {
            gantt.push({ id: processes[idx].id, start: time, end: time + processes[idx].bt });
            processes[idx].st = time;
            time += processes[idx].bt;
            processes[idx].ct = time;
            is_completed[idx] = true;
            completed++;
        } else {
            let next_arr = Infinity;
            for (let i = 0; i < n; i++) {
                if (!is_completed[i] && processes[i].at < next_arr) {
                    next_arr = processes[i].at;
                }
            }
            gantt.push({ id: 'IDLE', start: time, end: next_arr });
            time = next_arr;
        }
    }
    return gantt;
}

// SRTF (Preemptive SJF)
function solveSRTF(processes) {
    let time = 0;
    let completed = 0;
    let n = processes.length;
    let gantt = [];
    let is_completed = new Array(n).fill(false);

    let current_process = -1;
    let current_start = 0;

    processes.sort((a, b) => a.at - b.at); // Required for 'first come first serve' on arrival ties

    while (completed !== n) {
        let idx = -1;
        let min_rt = Infinity;

        // Find process with min remaining time
        for (let i = 0; i < n; i++) {
            if (processes[i].at <= time && !is_completed[i]) {
                if (processes[i].rt < min_rt) {
                    min_rt = processes[i].rt;
                    idx = i;
                }
                if (processes[i].rt === min_rt) {
                    if (processes[i].at < processes[idx].at) {
                        min_rt = processes[i].rt;
                        idx = i;
                    }
                }
            }
        }

        if (idx !== -1) {
            if (processes[idx].st === -1) processes[idx].st = time;

            if (current_process !== idx) {
                // Preemption or new process started
                if (current_process !== -1) {
                    gantt.push({ id: processes[current_process].id, start: current_start, end: time });
                } else if (time > 0 && current_start < time) {
                    gantt.push({ id: 'IDLE', start: current_start, end: time });
                }
                current_process = idx;
                current_start = time;
            }

            // Execute for 1 unit
            processes[idx].rt -= 1;
            time += 1;

            if (processes[idx].rt === 0) {
                processes[idx].ct = time;
                is_completed[idx] = true;
                completed++;
                gantt.push({ id: processes[idx].id, start: current_start, end: time });
                current_process = -1; // Reset for next iteration
                current_start = time;
            }
        } else {
            if (current_process !== -1) { // Close out current block if somehow hit
                gantt.push({ id: processes[current_process].id, start: current_start, end: time });
                current_process = -1;
            } else if (current_start === time) {
                // Do nothing, idle just started
            }
            time += 1;
        }
    }

    // Merge consecutive idles
    return combineGantt(gantt);
}

// Priority (Non-Preemptive)
function solvePriority(processes) {
    let time = 0;
    let completed = 0;
    let n = processes.length;
    let gantt = [];
    let is_completed = new Array(n).fill(false);
    processes.sort((a, b) => a.at - b.at);

    while (completed !== n) {
        let idx = -1;
        // Assume lower number = higher priority. e.g. 1 is highest
        let max_pr = Infinity;

        for (let i = 0; i < n; i++) {
            if (processes[i].at <= time && is_completed[i] === false) {
                if (processes[i].pr < max_pr) {
                    max_pr = processes[i].pr;
                    idx = i;
                }
                if (processes[i].pr === max_pr) {
                    if (processes[i].at < processes[idx].at) {
                        max_pr = processes[i].pr;
                        idx = i;
                    }
                }
            }
        }

        if (idx !== -1) {
            gantt.push({ id: processes[idx].id, start: time, end: time + processes[idx].bt });
            processes[idx].st = time;
            time += processes[idx].bt;
            processes[idx].ct = time;
            is_completed[idx] = true;
            completed++;
        } else {
            let next_arr = Infinity;
            for (let i = 0; i < n; i++) {
                if (!is_completed[i] && processes[i].at < next_arr) {
                    next_arr = processes[i].at;
                }
            }
            gantt.push({ id: 'IDLE', start: time, end: next_arr });
            time = next_arr;
        }
    }
    return gantt;
}

// Round Robin
function solveRR(processes, tq) {
    let time = 0;
    let n = processes.length;
    let gantt = [];
    let is_in_queue = new Array(n).fill(false);
    let queue = [];
    let completed = 0;

    // Ordered by ID for stable RR
    const originalProcs = [...processes];

    // Push first processes that arrived by time 0
    for (let i = 0; i < n; i++) {
        if (originalProcs[i].at === time) {
            queue.push(i);
            is_in_queue[i] = true;
        }
    }

    // Edge case if 0 isn't the first arrival
    if (queue.length === 0) {
        let next_arr = Infinity;
        for (let i = 0; i < n; i++) {
            if (processes[i].at < next_arr) next_arr = processes[i].at;
        }
        gantt.push({ id: 'IDLE', start: 0, end: next_arr });
        time = next_arr;
        for (let i = 0; i < n; i++) {
            if (originalProcs[i].at <= time) {
                queue.push(i);
                is_in_queue[i] = true;
            }
        }
    }

    while (completed !== n) {
        if (queue.length === 0) {
            let next_arr = Infinity;
            for (let i = 0; i < n; i++) {
                if (originalProcs[i].rt > 0 && originalProcs[i].at < next_arr) {
                    next_arr = originalProcs[i].at;
                }
            }

            if (next_arr !== Infinity) {
                gantt.push({ id: 'IDLE', start: time, end: next_arr });
                time = next_arr;
                for (let i = 0; i < n; i++) {
                    if (originalProcs[i].rt > 0 && originalProcs[i].at <= time && !is_in_queue[i]) {
                        queue.push(i);
                        is_in_queue[i] = true;
                    }
                }
            }
            continue;
        }

        let idx = queue.shift();

        if (originalProcs[idx].st === -1) {
            originalProcs[idx].st = time;
        }

        if (originalProcs[idx].rt > tq) {
            gantt.push({ id: originalProcs[idx].id, start: time, end: time + tq });
            originalProcs[idx].rt -= tq;
            time += tq;

            // Add processes that arrived while execution was happening
            for (let i = 0; i < n; i++) {
                if (originalProcs[i].rt > 0 && originalProcs[i].at <= time && !is_in_queue[i] && i !== idx) {
                    queue.push(i);
                    is_in_queue[i] = true;
                }
            }
            // Put current back in queue
            queue.push(idx);

        } else {
            // Process completes
            gantt.push({ id: originalProcs[idx].id, start: time, end: time + originalProcs[idx].rt });
            time += originalProcs[idx].rt;
            originalProcs[idx].rt = 0;
            originalProcs[idx].ct = time;
            completed++;

            for (let i = 0; i < n; i++) {
                if (originalProcs[i].rt > 0 && originalProcs[i].at <= time && !is_in_queue[i]) {
                    queue.push(i);
                    is_in_queue[i] = true;
                }
            }
        }
    }

    return combineGantt(gantt);
}

// Utility to combine consecutive same blocks
function combineGantt(gantt) {
    if (gantt.length === 0) return gantt;
    let res = [gantt[0]];
    for (let i = 1; i < gantt.length; i++) {
        let last = res[res.length - 1];
        if (last.id === gantt[i].id) {
            last.end = gantt[i].end;
        } else {
            res.push(gantt[i]);
        }
    }
    return res;
}

// ------ CPU RENDER EXECUTION ------

function runCPUSimulation() {
    let processes = getProcessesFromTable();
    if (processes.length === 0) {
        alert("Please add at least one process.");
        return;
    }

    const alg = document.getElementById('cpu-algorithm').value;
    const tq = parseInt(document.getElementById('time-quantum').value, 10);

    let gantt = [];

    // Deep clone array to maintain referential data before algorithms
    let procCopy = JSON.parse(JSON.stringify(processes));

    switch (alg) {
        case 'fcfs': gantt = solveFCFS(procCopy); break;
        case 'sjf': gantt = solveSJF(procCopy); break;
        case 'srtf': gantt = solveSRTF(procCopy); break;
        case 'priority': gantt = solvePriority(procCopy); break;
        case 'rr': gantt = solveRR(procCopy, tq); break;
    }

    // Calculate TAT and WT
    let totalWT = 0;
    let totalTAT = 0;

    procCopy.forEach(p => {
        p.tat = p.ct - p.at;
        p.wt = p.tat - p.bt;
        totalWT += p.wt;
        totalTAT += p.tat;
    });

    const avgWT = (totalWT / procCopy.length).toFixed(2);
    const avgTAT = (totalTAT / procCopy.length).toFixed(2);

    document.getElementById('avg-waiting').innerText = avgWT;
    document.getElementById('avg-turnaround').innerText = avgTAT;

    renderGanttChart(gantt);
    renderProcessTable(procCopy);
}

function renderGanttChart(gantt) {
    const container = document.getElementById('gantt-chart');
    container.innerHTML = '';

    if (gantt.length === 0) {
        container.innerHTML = '<div style="padding: 1rem; color: #64748b;">No schedule data generated.</div>';
        return;
    }

    let totalTime = gantt[gantt.length - 1].end;

    gantt.forEach(block => {
        const div = document.createElement('div');
        div.className = 'gantt-block';
        if (block.id === 'IDLE') div.classList.add('idle-block');

        // Flex basis roughly based on time passed
        const percent = ((block.end - block.start) / totalTime) * 100;
        
        // Use custom property for animation keyframes
        div.style.setProperty('--target-width', Math.max(percent, 5) + '%');
        div.classList.add('gantt-block-anim'); // Add animation class

        let bgStyle = '';
        if (block.id !== 'IDLE') {
            // Premium gradients
            const colors = [
                'linear-gradient(135deg, #0ea5e9, #6366f1)',
                'linear-gradient(135deg, #f43f5e, #fb923c)',
                'linear-gradient(135deg, #8b5cf6, #d946ef)',
                'linear-gradient(135deg, #10b981, #3b82f6)',
                'linear-gradient(135deg, #eab308, #ef4444)'
            ];
            const pnum = parseInt(block.id.replace('P', '')) || 1;
            bgStyle = `background: ${colors[(pnum - 1) % colors.length]};`;
        }

        div.innerHTML = `
            <div class="gantt-process" style="${bgStyle}">
                ${block.id}
            </div>
            <div class="gantt-time">
                <span>${block.start}</span>
                <span>${block.end}</span>
            </div>
        `;
        container.appendChild(div);
    });
}

function renderProcessTable(processes) {
    const tbody = document.getElementById('results-tbody');
    tbody.innerHTML = '';

    // Process display order based on Process ID numerically
    processes.sort((a, b) => parseInt(a.id.substring(1)) - parseInt(b.id.substring(1)));

    processes.forEach(p => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>${p.id}</strong></td>
            <td>${p.at}</td>
            <td>${p.bt}</td>
            <td style="color: var(--primary-accent);">${p.ct}</td>
            <td>${p.tat}</td>
            <td>${p.wt}</td>
        `;
        tbody.appendChild(tr);
    });
}

// -----------------------------------------------------------------------------
// MEMORY ALLOCATION SIMULATION
// -----------------------------------------------------------------------------

function runMemSimulation() {
    const algo = document.getElementById('mem-algorithm').value;
    const blocksInput = document.getElementById('mem-blocks').value;
    const processesInput = document.getElementById('mem-processes').value;

    let blocks = blocksInput.split(',').map(n => parseInt(n.trim())).filter(n => !isNaN(n));
    let processes = processesInput.split(',').map(n => parseInt(n.trim())).filter(n => !isNaN(n));

    if (blocks.length === 0 || processes.length === 0) {
        alert("Please enter valid comma-separated sizes for blocks and processes.");
        return;
    }

    // Allocation logic
    // allocation[i] contains block index where process i is placed
    let allocation = new Array(processes.length).fill(-1);

    // Create a copy of blocks to track remaining sizes
    let remBlocks = [...blocks];

    if (algo === 'first') {
        for (let i = 0; i < processes.length; i++) {
            for (let j = 0; j < remBlocks.length; j++) {
                if (remBlocks[j] >= processes[i]) {
                    allocation[i] = j;
                    remBlocks[j] -= processes[i];
                    break;
                }
            }
        }
    } else if (algo === 'best') {
        for (let i = 0; i < processes.length; i++) {
            let bestIdx = -1;
            for (let j = 0; j < remBlocks.length; j++) {
                if (remBlocks[j] >= processes[i]) {
                    if (bestIdx === -1 || remBlocks[j] < remBlocks[bestIdx]) {
                        bestIdx = j;
                    }
                }
            }
            if (bestIdx !== -1) {
                allocation[i] = bestIdx;
                remBlocks[bestIdx] -= processes[i];
            }
        }
    } else if (algo === 'worst') {
        for (let i = 0; i < processes.length; i++) {
            let worstIdx = -1;
            for (let j = 0; j < remBlocks.length; j++) {
                if (remBlocks[j] >= processes[i]) {
                    if (worstIdx === -1 || remBlocks[j] > remBlocks[worstIdx]) {
                        worstIdx = j;
                    }
                }
            }
            if (worstIdx !== -1) {
                allocation[i] = worstIdx;
                remBlocks[worstIdx] -= processes[i];
            }
        }
    }

    // Calculate Internal Fragmentation
    let totalIntFrag = 0;
    allocation.forEach((blockIdx, procIdx) => {
        if (blockIdx !== -1) {
            // Fragment generated in that specific block for that process
            // wait, remBlocks reflects the FINAL state of the blocks.
            // Internal fragmentation strictly is the sum of (original block - process) 
            // if we consider static partitions. If we consider dynamic partitions, 
            // internal fragmentation isn't quite the leftover. 
            // But let's define it as the total leftover space in blocks that have at least one process.
            // Actually, we can just sum up the remaining space of ALL used blocks.
        }
    });

    // Calculate total internal fragmentation: sum of remaining space in blocks that got USED
    let usedBlocks = new Set(allocation.filter(x => x !== -1));
    usedBlocks.forEach(idx => {
        totalIntFrag += remBlocks[idx];
    });

    document.getElementById('int-frag').innerText = `${totalIntFrag} KB`;

    renderMemResults(processes, allocation, blocks, remBlocks);
}

function renderMemResults(processes, allocation, originalBlocks, remBlocks) {
    // 1. Render logical Process Table
    const tbody = document.getElementById('mem-results-tbody');
    tbody.innerHTML = '';

    for (let i = 0; i < processes.length; i++) {
        let blockText = allocation[i] !== -1 ? `Block ${allocation[i] + 1}` : `<span style="color: #ef4444;">Not Allocated</span>`;
        tbody.innerHTML += `
            <tr>
                <td><strong>P${i + 1}</strong></td>
                <td>${processes[i]} KB</td>
                <td>${blockText}</td>
            </tr>
        `;
    }

    // 2. Render Physical Blocks
    const container = document.getElementById('memory-visualization-container');
    container.innerHTML = '';

    const colors = [
        'linear-gradient(135deg, #0ea5e9, #6366f1)',
        'linear-gradient(135deg, #f43f5e, #fb923c)',
        'linear-gradient(135deg, #8b5cf6, #d946ef)',
        'linear-gradient(135deg, #10b981, #3b82f6)',
        'linear-gradient(135deg, #eab308, #ef4444)'
    ];

    let maxBlockSize = Math.max(...originalBlocks);

    for (let j = 0; j < originalBlocks.length; j++) {
        // Find which processes are in this block
        let allocatedProcs = [];
        for (let i = 0; i < processes.length; i++) {
            if (allocation[i] === j) {
                allocatedProcs.push({ id: i + 1, size: processes[i] });
            }
        }

        // Calculate heights relative to the max block size for visualization (between 100px and 250px)
        let heightBase = Math.max(100, (originalBlocks[j] / maxBlockSize) * 250);

        let blockWrapper = document.createElement('div');
        blockWrapper.style.display = 'flex';
        blockWrapper.style.flexDirection = 'column';
        blockWrapper.style.alignItems = 'center';
        blockWrapper.style.gap = '0.5rem';
        blockWrapper.style.flex = '1';
        blockWrapper.style.minWidth = '120px';

        let innerHt = '';
        if (allocatedProcs.length === 0) {
            // Empty Box
            innerHt = `
                <div style="flex: 1; display:flex; align-items:center; justify-content:center; flex-direction: column; color: var(--text-secondary); opacity: 0.7;">
                    <div>Free</div>
                    <div style="font-size: 0.8rem;">${originalBlocks[j]} KB</div>
                </div>
            `;
        } else {
            // Stacked processes
            allocatedProcs.forEach(proc => {
                let procPercent = (proc.size / originalBlocks[j]) * 100;
                let bg = colors[(proc.id - 1) % colors.length];
                innerHt += `
                    <div style="height: ${procPercent}%; width: 100%; background: ${bg}; display:flex; align-items:center; justify-content:center; flex-direction: column; border-bottom: 1px solid rgba(0,0,0,0.05);">
                        <div style="font-weight: 700; text-shadow: 0 1px 3px rgba(0,0,0,0.1); color: #fff;">P${proc.id}</div>
                        <div style="font-size: 0.8rem; color: rgba(255,255,255,0.9);">${proc.size} KB</div>
                    </div>
                `;
            });

            // Add remaining free space if > 0
            let freePercent = (remBlocks[j] / originalBlocks[j]) * 100;
            if (freePercent > 0) {
                innerHt += `
                    <div style="height: ${freePercent}%; width: 100%; display:flex; align-items:center; justify-content:center; flex-direction: column; color: var(--text-secondary); opacity: 0.7; border-top: 1px dashed rgba(0,0,0,0.1);">
                        <div style="font-size: 0.8rem;">Free ${remBlocks[j]} KB</div>
                    </div>
                `;
            }
        }

        let physicalBlock = `
            <div style="width: 100%; height: ${heightBase}px; background: rgba(255,255,255,0.4); border: 2px solid var(--glass-border); border-radius: 8px; margin-bottom: 0.5rem; overflow: hidden; display: flex; flex-direction: column; box-shadow: inset 0 0 20px rgba(0,0,0,0.05);">
                ${innerHt}
            </div>
            <div style="font-weight: 600; font-size: 0.9rem;">Block ${j + 1}</div>
            <div style="font-size: 0.8rem; color: var(--text-secondary);">${originalBlocks[j]} KB Total</div>
        `;
        blockWrapper.innerHTML = physicalBlock;
        blockWrapper.classList.add('mem-block-anim'); // Add staggering class
        blockWrapper.style.animationDelay = `${j * 0.15}s`; // Sequential stagger
        container.appendChild(blockWrapper);
    }
}

// -----------------------------------------------------------------------------
// PROCESS SYNCHRONIZATION SIMULATION
// -----------------------------------------------------------------------------

function runSyncSimulation() {
    const problem = document.getElementById('sync-problem').value;
    const numEntities = parseInt(document.getElementById('sync-entities').value);

    const terminal = document.getElementById('sync-terminal');
    const visualizer = document.getElementById('sync-visualizer');
    const statusBox = document.getElementById('sync-status');

    terminal.innerHTML = `<span style="color: #6366f1;">admin@talensync</span>:<span style="color: #10b981;">~/sync</span>$ ./start_sim --type ${problem} --entities ${numEntities}<br><br>`;
    visualizer.innerHTML = '';
    
    // Start pulsing animation
    visualizer.classList.add('sync-pulse');
    statusBox.innerText = "Running...";
    statusBox.style.color = "var(--accent-pink)";

    let logs = [];
    let stateHtml = '';

    // Simple simulated traces for visualization
    if (problem === 'producer_consumer') {
        let bufferSize = 5;
        let pCount = Math.floor(numEntities / 2) || 1;
        let cCount = numEntities - pCount;

        logs.push(`Initializing Bounded Buffer (Size: ${bufferSize})`);
        logs.push(`Starting ${pCount} Producers and ${cCount} Consumers...`);
        logs.push(`[System] Mutex initialized to 1.`);
        logs.push(`[System] Semaphores 'empty'=${bufferSize}, 'full'=0.`);

        for (let i = 0; i < 6; i++) {
            let isProd = Math.random() > 0.5;
            if (isProd) {
                logs.push(`[Producer ${Math.floor(Math.random() * pCount) + 1}] wait(empty) -> wait(mutex) -> Producing item -> signal(mutex) -> signal(full)`);
            } else {
                logs.push(`[Consumer ${Math.floor(Math.random() * cCount) + 1}] wait(full) -> wait(mutex) -> Consuming item -> signal(mutex) -> signal(empty)`);
            }
        }

        logs.push(`Simulation completed.`);

        // Build visualizer
        for (let j = 0; j < bufferSize; j++) {
            let filled = Math.random() > 0.5;
            let bg = filled ? 'var(--accent-purple)' : 'rgba(0,0,0,0.05)';
            stateHtml += `<div style="width: 50px; height: 50px; border-radius: 8px; border: 2px solid var(--glass-border); background: ${bg}; display: flex; align-items: center; justify-content: center; font-weight: bold;">${filled ? 'Data' : ''}</div>`;
        }

    } else if (problem === 'readers_writers') {
        let rCount = Math.floor(numEntities * 0.7) || 1;
        let wCount = numEntities - rCount;

        logs.push(`Initializing Shared Data Resource.`);
        logs.push(`Starting ${rCount} Readers and ${wCount} Writers...`);
        logs.push(`[System] rw_mutex initialized to 1, mutex initialized to 1.`);

        for (let i = 0; i < 6; i++) {
            let isRead = Math.random() > 0.3;
            if (isRead) {
                logs.push(`[Reader ${Math.floor(Math.random() * rCount) + 1}] Entering... read_count++ ... reading shared data ... read_count-- ... Leaved.`);
            } else {
                logs.push(`[Writer ${Math.floor(Math.random() * wCount) + 1}] wait(rw_mutex) -> Writing to shared data -> signal(rw_mutex)`);
            }
        }

        logs.push(`Simulation completed.`);

        stateHtml = `<div style="text-align:center; padding: 2rem; border: 2px dashed var(--accent-blue); border-radius: 12px; width: 100%;">Shared Resource<br><span style="color: var(--text-secondary); font-size: 0.8rem;">Current State: Stable</span></div>`;

    } else if (problem === 'dining_philosophers') {
        logs.push(`Initializing table with ${numEntities} Philosophers and ${numEntities} Chopsticks.`);

        for (let i = 0; i < 6; i++) {
            let phil = Math.floor(Math.random() * numEntities);
            let left = phil;
            let right = (phil + 1) % numEntities;
            logs.push(`[Philosopher ${phil}] Thinking...`);
            logs.push(`[Philosopher ${phil}] Hungry. Waiting for chopstick ${left} and ${right}...`);
            logs.push(`[Philosopher ${phil}] Eating...`);
            logs.push(`[Philosopher ${phil}] Put down chopsticks. Back to Thinking.`);
        }

        logs.push(`Simulation completed.`);

        for (let j = 0; j < numEntities; j++) {
            let state = Math.random() > 0.5 ? 'Eating' : 'Thinking';
            let color = state === 'Eating' ? 'var(--accent-green)' : 'var(--text-secondary)';
            stateHtml += `
                <div style="display:flex; flex-direction:column; align-items:center; background: rgba(255,255,255,0.6); padding: 1rem; border-radius: 12px; border: 1px solid var(--glass-border);">
                    <i class="fas fa-user-tie" style="font-size: 2rem; color: ${color}; margin-bottom: 0.5rem;"></i>
                    <div style="font-weight:bold;">Phil ${j}</div>
                    <div style="font-size:0.8rem; color:${color};">${state}</div>
                </div>
            `;
        }
    }

    // Simulate typing effect in terminal
    let delay = 0;
    logs.forEach(log => {
        setTimeout(() => {
            terminal.innerHTML += `> ${log}<br>`;
            terminal.scrollTop = terminal.scrollHeight;
        }, delay);
        delay += 500;
    });

    setTimeout(() => {
        statusBox.innerText = "Completed";
        statusBox.style.color = "var(--accent-green)";
        visualizer.innerHTML = stateHtml;
        // Stop pulsing animation when complete
        visualizer.classList.remove('sync-pulse');
    }, delay + 200);
}

// -----------------------------------------------------------------------------
// FILE SYSTEM ALLOCATION SIMULATION
// -----------------------------------------------------------------------------

function runFSSimulation() {
    const method = document.getElementById('fs-algorithm').value;
    const totalBlocks = parseInt(document.getElementById('fs-disk-size').value);
    const filesInput = document.getElementById('fs-files').value;

    if (isNaN(totalBlocks) || totalBlocks <= 0) {
        alert("Invalid total blocks.");
        return;
    }

    let fileEntries = filesInput.split(',').map(f => f.trim());
    let files = [];

    fileEntries.forEach(entry => {
        let parts = entry.split(':');
        if (parts.length === 2) {
            files.push({ name: parts[0].trim(), size: parseInt(parts[1].trim()) });
        }
    });

    if (files.length === 0) {
        alert("Please enter valid files.");
        return;
    }

    // Disk Map: -1 means free, otherwise stores the file name/id
    let disk = new Array(totalBlocks).fill(-1);
    let fat = []; // Stores {name: string, startBlock: any, blocks: []}

    let freeBlocksCount = totalBlocks;

    if (method === 'contiguous') {
        let currentBlock = 0;
        files.forEach(f => {
            if (f.size > 0 && currentBlock + f.size <= totalBlocks) {
                let allocated = [];
                for (let i = 0; i < f.size; i++) {
                    disk[currentBlock + i] = f.name;
                    allocated.push(currentBlock + i);
                }
                fat.push({ name: f.name, start: currentBlock, blocks: allocated });
                currentBlock += f.size;
                freeBlocksCount -= f.size;
            } else {
                fat.push({ name: f.name, start: 'Failed (No Contiguous Space)', blocks: [] });
            }
            // Add a gap to simulate external fragmentation
            currentBlock += Math.floor(Math.random() * 3);
        });

    } else if (method === 'linked') {
        files.forEach(f => {
            let allocated = [];
            for (let i = 0; i < totalBlocks && allocated.length < f.size; i++) {
                if (disk[i] === -1) {
                    disk[i] = f.name;
                    allocated.push(i);
                }
            }
            if (allocated.length === f.size) {
                fat.push({ name: f.name, start: allocated[0], blocks: allocated });
                freeBlocksCount -= f.size;
            } else {
                // Rollback if failed
                allocated.forEach(b => disk[b] = -1);
                fat.push({ name: f.name, start: 'Failed (Not Enough Space)', blocks: [] });
            }
        });

    } else if (method === 'indexed') {
        files.forEach(f => {
            // Find an index block
            let indexBlock = -1;
            for (let i = 0; i < totalBlocks; i++) {
                if (disk[i] === -1) {
                    indexBlock = i;
                    disk[i] = `IDX(${f.name})`;
                    break;
                }
            }

            if (indexBlock !== -1) {
                let allocated = [];
                for (let i = 0; i < totalBlocks && allocated.length < f.size; i++) {
                    if (disk[i] === -1) {
                        disk[i] = f.name;
                        allocated.push(i);
                    }
                }

                if (allocated.length === f.size) {
                    fat.push({ name: f.name, start: `Index Block: ${indexBlock}`, blocks: [indexBlock, ...allocated] });
                    freeBlocksCount -= (f.size + 1); // +1 for index block
                } else {
                    // Rollback
                    disk[indexBlock] = -1;
                    allocated.forEach(b => disk[b] = -1);
                    fat.push({ name: f.name, start: 'Failed (Not Enough Space)', blocks: [] });
                }
            } else {
                fat.push({ name: f.name, start: 'Failed (No Index Block)', blocks: [] });
            }
        });
    }

    document.getElementById('fs-free-blocks').innerText = freeBlocksCount;

    renderFSMaps(disk, fat);
}

function renderFSMaps(disk, fat) {
    // Render Grid
    const grid = document.getElementById('fs-disk-grid');
    grid.innerHTML = '';

    // Create a color map for files
    let colorMap = {};
    const colors = [
        '#0ea5e9', '#f43f5e', '#8b5cf6', '#10b981', '#fb923c', '#d946ef', '#eab308'
    ];
    let cIdx = 0;

    fat.forEach(f => {
        if (!colorMap[f.name]) {
            colorMap[f.name] = colors[cIdx % colors.length];
            // Fix index block identifiers
            colorMap[`IDX(${f.name})`] = colors[cIdx % colors.length];
            cIdx++;
        }
    });

    disk.forEach((val, idx) => {
        let div = document.createElement('div');
        div.style.aspectRatio = '1';
        div.style.display = 'flex';
        div.style.alignItems = 'center';
        div.style.justifyContent = 'center';
        div.style.fontSize = '0.7rem';
        div.style.borderRadius = '4px';
        div.style.fontWeight = 'bold';
        div.title = `Block ${idx}: ${val === -1 ? 'Free' : val}`;
        
        // Add sweep animation class and stagger delay based on index
        div.classList.add('fs-block-anim');
        div.style.animationDelay = `${idx * 0.05}s`;

        if (val === -1) {
            div.style.background = 'rgba(0,0,0,0.05)';
            div.style.border = '1px solid rgba(0,0,0,0.1)';
        } else {
            // Is it an index block?
            if (typeof val === 'string' && val.startsWith('IDX')) {
                div.style.background = colorMap[val];
                div.style.border = '2px solid #fff';
                div.innerText = 'I';
            } else {
                div.style.background = colorMap[val];
                // just text of the file name initial
                div.innerText = val.charAt(0).toUpperCase();
            }
        }
        grid.appendChild(div);
    });

    // Render FAT Table
    const tbody = document.getElementById('fs-fat-tbody');
    tbody.innerHTML = '';

    fat.forEach(f => {
        let blocksStr = f.blocks.length > 0 ? f.blocks.join(', ') : '-';
        let color = colorMap[f.name] || 'inherit';

        tbody.innerHTML += `
            <tr>
                <td style="color: ${color}; font-weight: bold;">${f.name}</td>
                <td>${f.start}</td>
                <td style="font-family: 'Space Mono', monospace; font-size: 0.9rem;">[${blocksStr}]</td>
            </tr>
        `;
    });
}
