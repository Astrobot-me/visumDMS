analysisDict = {
                "emotiondict": 1,
                "dominantemotion": 1,
                "face_confidence": 2,
                "age": 3,
                "dominant_gender": 5,
                "leye_region": 5,
                "reye_region": 6
            }

print(analysisDict['dominantemotion'])


li = ['a','b']

if 'a' not in li :
    print("Hellow world")
else: 
    print("Relax world")

size = 2
array = ["hello","feloo"]
if(size>1):
    for i in range(size-1,-1,-1):
        print(array[i])