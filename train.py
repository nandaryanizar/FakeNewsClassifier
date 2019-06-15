from classifier.machine_learning import classifier
from classifier.models import Classifier

clssfr = Classifier.objects.get(pk=1)
model = classifier.Classifier(clssfr.model,clssfr.model + "_model",clssfr.model + "_tfidf")

model.train()  