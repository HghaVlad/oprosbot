from matplotlib import rcParams
import matplotlib.pyplot as plt
def analyse(answers):
    print(answers[0])
    data = {}
    for _ in range(len(answers[0])):
        data.update({_: {}})
    i = 0
    for answer in answers:
        i = 0
        for an in answer:
            an = an.title()
            if an in data[i].keys():
                data[i][an] = data[i][an] + data[i][an]
            else:
                data[i][an] = 1
            i = i + 1
    return data
def getimg(name,data,quests):
    pathes = []
    for i in data:
        labels = list(data[i].keys())
        if len(labels) >= 5:
            values = list(data[i].values())
            x = zip(values, labels)
            xs = sorted(x, key=lambda tup: tup[0])
            values = [x[0] for x in xs]
            labels = [x[1] for x in xs]
            othe = 0
            for x in values[:-4]:
                othe = othe + x
            values = values[-4::]
            labels = labels[-4::]
            labels.append("Другое")
            values.append(othe)
            plt.close()
            plt.figure(figsize=(8,6))
            plt.pie(labels= labels, x=values,autopct='%1.1f%%')
            plt.title(quests[i].split("/;")[0])
            newname = name +str(i)+'.png'
            plt.savefig(newname)
            pathes.append(newname)
        else:
            values = list(data[i].values())
            plt.close()
            plt.pie(labels= labels, x=values,autopct='%1.1f%%')
            plt.title(quests[i].split("/;")[0])
            newname = name +str(i)+'.png'
            plt.savefig(newname)
            pathes.append(newname)  
    print(pathes)
    return pathes


