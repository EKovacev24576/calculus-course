import json, urllib.request, concurrent.futures as cf, subprocess
KEY=open('/home/claude/fal/.key').read().strip()
H={"Authorization":"Key "+KEY,"Content-Type":"application/json"}
SEG=[
("s11a","Press B4 on a vending machine, and you get pretzels. Every time. You never press B4 and get two different snacks. A vending machine is a function: one input, exactly one output. That simple rule is the foundation of all of calculus."),
("s11b","Think of a function as a machine. A number goes in, the machine follows its rule, and a number comes out. This machine's rule is: square the input, then add one. Put in two. Two squared is four, plus one is five. Put in three, and you get ten. Put in negative one, and you get two."),
("s11c","We write that rule like this: f of x equals x squared plus one. Here, f is the machine's name. x is whatever goes in. And f of x is what comes out. So f of two equals five."),
("s11d","Now list some inputs and outputs in a table. Each pair is a point. The input tells you how far across, and the output tells you how far up. Plot them all, fill in every input in between, and you get the graph of the function: a picture of everything the machine can do."),
("s11e","Remember the one rule: each input gets exactly one output. On a graph, that means any vertical line crosses the curve at most once. This curve passes. But a circle fails. One input, two outputs. So a circle is not a function."),
("s11f","Two last words. The domain is every input the machine accepts. The range is every output it can produce. For our machine, any number can go in, so the domain is all real numbers. But the output is never less than one, so the range is one and up."),
("s11g","So, a function is a rule that gives each input exactly one output. You can show it as a machine, a formula, a table, or a graph. Calculus is the study of how functions change, which is why we start here. In level two, we'll find domains and ranges, combine functions, and spot symmetry."),
]
def run(x):
    n,t=x
    req=urllib.request.Request("https://fal.run/fal-ai/elevenlabs/tts/eleven-v3",data=json.dumps({"text":t,"voice":"Brian","stability":0.5,"timestamps":True}).encode(),headers=H)
    try: r=json.load(urllib.request.urlopen(req,timeout=240))
    except urllib.error.HTTPError as e: return n,"ERR "+str(e.code)+" "+e.read().decode()[:300]
    urllib.request.urlretrieve(r["audio"]["url"],f"vo/{n}.mp3"); json.dump(r,open(f"vo/{n}.json","w"))
    return n,subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"vo/{n}.mp3"],capture_output=True,text=True).stdout.strip()
with cf.ThreadPoolExecutor(7) as ex:
    for n,d in ex.map(run,SEG): print(n,d)
