import json, urllib.request, concurrent.futures as cf, subprocess
KEY=open('/home/claude/fal/.key').read().strip()
H={"Authorization":"Key "+KEY,"Content-Type":"application/json"}
SEG=[
("a","You're in a car, and the speedometer says sixty miles per hour. But what does that actually mean? Sixty miles per hour is a distance divided by a time. Yet the speedometer gives you a number at a single instant, when no time passes and no distance is covered. So how can you have a speed at one instant? That puzzle is exactly what the derivative solves."),
("b","Let's draw the trip. Time goes across, and distance goes up. This curve shows how far the car has gone at each moment. Where the curve is flatter, the car is slow. Where the curve is steep, the car is covering a lot of distance quickly, so it's fast. Speed is hiding in the steepness of the curve."),
("c","Measuring steepness between two moments is easy. Pick two points on the curve and connect them with a straight line. The slope of that line, rise over run, is the average speed between those two moments. From one second to three seconds, the car goes from one meter to nine meters. That's eight meters in two seconds: an average of four meters per second."),
("d","But we want the speed at exactly one second. So slide the second point closer. Three seconds. Two seconds. One and a half. The line keeps tilting, and its slope keeps changing. Four. Three. Two and a half. As the gap shrinks toward nothing, the slope doesn't go wild. It settles down toward one particular number: two."),
("e","The line it settles into just touches the curve at that one point. It's called the tangent line. Its slope, two meters per second, is the car's speed at exactly one second. That number is the derivative at that point."),
("f","And we can do this at every point. Slide along the curve. Where it's flat, the derivative is small. Where it's steep, the derivative is large. Collect all those slopes, and you get a brand new function, the derivative, that tells you how fast things are changing at every moment."),
("g","So here is the whole idea in one sentence. The derivative is the slope of a curve at a single point: how fast something is changing right now. Speed is the derivative of distance. And the same idea measures how fast a population grows, how quickly a price changes, or how fast a rocket climbs. In level two, we'll turn this picture into a formula, and learn to calculate it."),
]
def run(x):
    n,t=x
    req=urllib.request.Request("https://fal.run/fal-ai/elevenlabs/tts/eleven-v3",data=json.dumps({"text":t,"voice":"Brian","stability":0.5,"timestamps":True}).encode(),headers=H)
    try: r=json.load(urllib.request.urlopen(req,timeout=240))
    except urllib.error.HTTPError as e: return n,"ERR "+e.read().decode()[:300]
    urllib.request.urlretrieve(r["audio"]["url"],f"vo/{n}.mp3")
    json.dump(r,open(f"vo/{n}.json","w"))
    d=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"vo/{n}.mp3"],capture_output=True,text=True).stdout.strip()
    return n,d
with cf.ThreadPoolExecutor(7) as ex:
    for n,d in ex.map(run,SEG): print(n,d)
