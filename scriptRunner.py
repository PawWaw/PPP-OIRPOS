from InceptionResnetV2 import runInceptionResnetV2
from InceptionV3 import runInceptionV3
from MobileNet import runMobileNet
from MobileNet_V2 import runMobileNetV2
from ResNet import runResNet50
from VGG16 import runVGG16
from VGG19 import runVGG19

def runScripts(path):
    tab = []
    tab.append((runInceptionResnetV2(path), "InceptionResnetV2"))
    tab.append((runInceptionV3(path), "InceptionV3"))
    tab.append((runMobileNet(path), "MobileNet"))
    tab.append((runMobileNetV2(path), "MobileNetV2"))
    tab.append((runResNet50(path), "ResNet50"))
    tab.append((runVGG16(path), "VGG16"))
    tab.append((runVGG19(path), "VGG19"))

    return tab

values = []
values = runScripts('C:/Users/pawel/Desktop/border.jpg')

for x in values:
    print(x[0])
    print(x[1])