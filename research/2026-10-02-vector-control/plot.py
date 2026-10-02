"""Render the analytical study. Values come directly from results.json."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

ROOT = Path(__file__).resolve().parent
R = json.loads((ROOT / 'results.json').read_text())
plt.rcParams.update({'font.size': 11, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.titleweight': 'bold', 'figure.facecolor': 'white'})
COLORS = ['#666b73', '#188278', '#316cc1', '#c05b29']
MODES = ['fixed', 'microcode', 'riscv-vector', 'riscv-strip']
LABELS = ['Fixed reference', 'Microcode', 'RISC-V whole row', 'RISC-V short SIMD']

def series(parameter, op, mode='riscv-vector'):
    a = [x for x in R['sensitivities'] if x['parameter']==parameter and x['op']==op and x['controller']==mode]
    return [x['value'] for x in a], [x['us'] for x in a]

def point(op, mode):
    a=[x for x in R['sensitivities'] if x['parameter']=='controllers' and x['value']==1 and x['op']==op and x['controller']==mode]
    assert len(a)==1
    return a[0]['us']

fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.subplots_adjust(top=.85, bottom=.18, left=.08, right=.97, hspace=.49, wspace=.28)
fig.suptitle('Programmability depends on command granularity', x=.08, y=.98, ha='left', fontsize=22, weight='bold')
fig.text(.08,.932,'Analytical estimates • Qwen3.5-2B kernel shapes • same arithmetic and memory for each controller',fontsize=12,color='#444')
ax=axs[0,0]
ops=['SOFT_MAX','RMS_NORM','SWIGLU']
x=np.arange(3)
for i, mode in enumerate(MODES):
    ys=[point(op,mode)/point(op,'fixed') for op in ops]
    bars=ax.bar(x+(i-1.5)*.2,ys,.19,label=LABELS[i],color=COLORS[i])
    ax.bar_label(bars,labels=[f'{y:.2f}×' for y in ys],padding=3,fontsize=8)
ax.set_xticks(x,['Softmax\n8 × 20,736','RMSNorm\n16 × 128','SwiGLU\n8 × 6,144'])
ax.set_ylim(0,6.5);ax.set_ylabel('Latency / fixed reference');ax.set_title('Short commands can starve the datapath',loc='left',fontsize=13)
ax.legend(ncol=2,loc='upper left',bbox_to_anchor=(0,1.01),fontsize=8,frameon=False)
ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)

ax=axs[0,1]
for parameter,label,color in [('sramBpc','Shared SRAM (aggregate)',COLORS[2]),('localBpcPerEngine','Local scratch (per engine)',COLORS[1])]:
    xx,yy=series(parameter,'SWIGLU');ax.plot(xx,yy,'o-',label=label,color=color)
ax.set_xscale('log',base=2);ax.set_xticks([16,32,64,128,256,512],[16,32,64,128,256,512])
ax.set_xlabel('Effective bytes per accelerator cycle');ax.set_ylabel('SwiGLU latency (µs)');ax.set_title('More memory bandwidth can help',loc='left',fontsize=13)
ax.legend(fontsize=9,frameon=False);ax.grid(alpha=.18)
ax.text(0,-.29,'Each curve varies one bandwidth; all other settings stay fixed.',transform=ax.transAxes,fontsize=9,color='#555')

ax=axs[1,0]
xx,yy=series('specialPorts','SWIGLU');ax.plot(xx,yy,'o-',color=COLORS[2],label='Whole-row RISC-V')
ax.set_xscale('log',base=2);ax.set_xticks(xx,xx);ax.set_xlabel('Special-function elements/cycle/engine');ax.set_ylabel('SwiGLU latency (µs)');ax.set_title('Exp/reciprocal throughput beats wider SIMD here',loc='left',fontsize=12)
ax.grid(alpha=.18)
ax.annotate(f'{yy[0]:.1f} µs',xy=(xx[0],yy[0]),xytext=(1.3,yy[0]-2),fontsize=10)
ax.annotate(f'{yy[3]:.1f} µs',xy=(xx[3],yy[3]),xytext=(7,yy[3]+7),fontsize=10,arrowprops={'arrowstyle':'->','color':'#666'})
ax.text(0,-.29,'16 → 128 lanes alone leaves this workload at ≈32.3 µs.',transform=ax.transAxes,fontsize=9,color='#555')

ax=axs[1,1]
xx,yy=series('enginesPerCommand','RMS_NORM');ax.plot(xx,yy,'o-',color=COLORS[2],label='One core, batched dispatch')
ax.axhline(point('RMS_NORM','fixed'),color=COLORS[0],linestyle='--',label='Fixed reference')
ax.set_xticks(xx);ax.set_ylim(.65,1.95);ax.set_xlabel('Row engines started per command');ax.set_ylabel('16 × 128 RMSNorm latency (µs)');ax.set_title('Batch small rows before replicating cores',loc='left',fontsize=13)
for a,b in zip(xx,yy): ax.annotate(f'{b:.2f}',(a,b),xytext=(0,9),textcoords='offset points',ha='center',fontsize=10)
ax.legend(fontsize=9,frameon=False);ax.grid(alpha=.18)
ax.text(0,-.29,'Batching requires address generators and completion tracking.',transform=ax.transAxes,fontsize=9,color='#555')
fig.text(.08,.03,'Reference: 8 engines × 32 lanes, 300 MHz, 64 KiB scratch/engine, 4-cycle RISC-V issue.\nNo RTL, area, power, instruction traces, or numerical validation. Resource sweeps do not hold area constant.',fontsize=10,color='#555')
fig.savefig(ROOT/'overview.png',dpi=180)

fig2, ax = plt.subplots(figsize=(11,6))
fig2.subplots_adjust(top=.77,bottom=.23,left=.10,right=.96)
fig2.suptitle('Most whole-model time is outside controller dispatch',x=.10,y=.96,ha='left',fontsize=20,weight='bold')
fig2.text(.10,.89,'Exploratory projection into the captured Qwen3.5-2B graph',fontsize=13,color='#444')
xx=np.arange(2)
for i,mode in enumerate(MODES[1:]):
    yy=[]
    for phase in ['prefill','decode']:
        rows=[x for x in R['projections'] if x['prompt']==8192 and x['phase']==phase and x['localKiB']==64]
        t=next(x['seconds'] for x in rows if x['controller']==mode)
        base=next(x['seconds'] for x in rows if x['controller']=='fixed')
        yy.append((t/base-1)*100)
    bars=ax.bar(xx+(i-1)*.22,yy,.21,color=COLORS[i+1],label=LABELS[i+1])
    ax.bar_label(bars,labels=[f'+{y:.2f}%' for y in yy],padding=5,fontsize=11)
ax.set_xticks(xx,['8,192-token prefill','Decode: 20,480 prior tokens'])
ax.set_ylabel('Increase in phase time vs fixed controller (%)');ax.set_ylim(0,80)
ax.legend(frameon=False,fontsize=10);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
fig2.text(.10,.065,'Identical compute and memory within each controller comparison. Unsupported nodes retain inherited timings.\nFP32 vector temporaries; inherited W4/A8 matrix model. Conversion, bank conflicts, and new HBM allocation omitted.\nModel-to-model sensitivity, not measured inference performance.',fontsize=10,color='#555')
fig2.savefig(ROOT/'projection.png',dpi=180)
with PdfPages(ROOT/'charts.pdf') as pdf:
    pdf.savefig(fig);pdf.savefig(fig2)
plt.close('all')
print('Rendered overview.png, projection.png, charts.pdf')
