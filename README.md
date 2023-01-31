# Word-Sense-Disambiguation
### Aim of this project to identify the sense of particular word for given context. 
In this project, I have used only to identify the sense of 6 different words. Such as plant, bass, crane, motion, palm, and tank.
####Methodology:
1. Create the bag of words for each sense
2. Applied Naive Bayes algorithm to identify the most probable sense of word in given context
3. Add one smoothing is done to avoid the zero probability case.
4. Used 5 fold cross validation technique, to identify the correct sense of given word.

### Result 
Average accuray for each word for sense identification:

Accuracy for the plant.wsd dataset:74.12 %

Accuracy for the bass.wsd dataset: 90.48 %

Accuracy for the crane.wsd dataset:76.84 %

Accuracy for the motion.wsd dataset: 82.0 %

Accuracy for the palm.wsd dataset:75.5 %

Accuracy for the tank.wsd dataset: 69.5 %
