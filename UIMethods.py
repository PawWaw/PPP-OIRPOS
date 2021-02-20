import math

# def mockup():
#     return (("InceptionResnetV2", "InceptionV3", "MobileNet", "MobileNetV2", "ResNet50", "VGG16","VGG19"),(0.943524,0.143534,0.856757,0.3454367,0.756547,0.785757657,0.78678567))

def getDataForGraph(tab):
    tabNetworks = []
    tabPerformances = []
    tabItems = []
    for x in tab:
        temp = x[0] 
        tabPerformances.append(temp[2])
        tabNetworks.append(x[1])  
        tabItems.append(temp[1])
    return (tabNetworks,tabPerformances)

def getDataForText(tab):
    tabNetworks = []
    tabPerformances = []
    tabItems = []
    tabItemsNumber = []
    for x in tab:
        temp = x[0] 
        if tabPerformances.count == 0:
            tabNetworks.append(x[1])
            tabPerformances.append(temp[2])
            tabItems.append(temp[1])
            tabItemsNumber.append(1)
        else:
            if temp[1] in tabItems:
                index = tabItems.index(temp[1])
                tabItemsNumber[index] = tabItemsNumber[index] + 1
                tabPerformances[index] = tabPerformances[index] + temp[2]
                tabNetworks[index] = tabNetworks[index] + ", " + x[1]
            else:
                tabNetworks.append(x[1])
                tabPerformances.append(temp[2])
                tabItems.append(temp[1])
                tabItemsNumber.append(1)
    tempString = "Srednia trafnosc rozpoznawania:"
    for x in tabItems:
        index = tabItems.index(x)
        average = tabPerformances[index]/tabItemsNumber[index]
        average = math.trunc(average * 100)
        tempString = tempString + " " + x + " " + str(average) + "% przez sieci: " + tabNetworks[index] + "; "
    return tempString