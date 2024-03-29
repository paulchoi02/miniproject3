import util
import classificationMethod
import math

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
  """
  See the project description for the specifications of the Naive Bayes classifier.
  
  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__(self, legalLabels):
    self.legalLabels = legalLabels
    self.type = "naivebayes"
    self.k = 1 # this is the smoothing parameter, ** use it in your train method **
    self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **
    
  def setSmoothing(self, k):
    """
    This is used by the main method to change the smoothing parameter before training.
    Do not modify this method.
    """
    self.k = k

  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method. Do not modify this method.
    """  
      
    self.features = trainingData[0].keys() # this could be useful for your code later...
    
    if (self.automaticTuning):
        kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
    else:
        kgrid = [self.k]
        
    self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)
      
  def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
    """
    Trains the classifier by collecting counts over the training data, and
    stores the Laplace smoothed estimates so that they can be used to classify.
    Evaluate each value of k in kgrid to choose the smoothing parameter 
    that gives the best accuracy on the held-out validationData.
    
    trainingData and validationData are lists of feature Counters.  The corresponding
    label lists contain the correct label for each datum.
    
    To get the list of all possible features or labels, use self.features and 
    self.legalLabels.
    """

    acc = -1
    trainCount = util.Counter(); #number of times seeing label l
    trainCondProb = util.Counter(); #p(feature = 1 | label)
    trainPrior = util.Counter(); #p(label)
    lengthT = len(trainingData)

    #loop through the training data
    for x in range lengthT:
      label = trainingLabels[x] #label
      datum = trainingData[x] #data #
      trainPrior[label] = trainPrior[label] + 1 #increment the prior 
      for feature, val in datum.items(): #iterate through datum objects
        trainCount[(feature, label)] = trainCount[(feature,label)] + 1
        if val > 0: #assume binary value
          trainCondProb[(feature, label)]

      #set k value for tuning
      #must smooth the data using K from kgrid
      #normalize the data 
      #can get auto tuning for k value use:
      # python dataClassifiers.py -c naiveBayes --autotune
      # should run with accuracy of 65% + 
    

    util.raiseNotDefined()
        
  def classify(self, testData):
    """
    Classify the data based on the posterior distribution over labels.
    
    You shouldn't modify this method.
    """
    guesses = []
    self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
    for datum in testData:
      posterior = self.calculateLogJointProbabilities(datum)
      guesses.append(posterior.argMax())
      self.posteriors.append(posterior)
    return guesses
      
  def calculateLogJointProbabilities(self, datum):
    """
    Returns the log-joint distribution over legal labels and the datum.
    Each log-probability should be stored in the log-joint counter, e.g.    
    logJoint[3] = <Estimate of log( P(Label = 3, datum) )>
    """
    logJoint = util.Counter()
    
    for l in self.legalLabels:
        logJoint[l] = math.log(self.prior[l])
        #find the most probable label given the feature values for each pixel:
        for feature, val in datum.items():
          #multiplying many probabilties often result in underflow, instead
          #compute log probabilities which have the same argmax:
          if(val < 0):#1 - self
            logJoint[l] += math.log(1-self.conditionalProb[feature, l])
          elif(value == 0):
            logJoint[l] += math.log(1-self.conditionalProb[feature, l])
          else: #self 
            logJoint[l] += math.log(self.conditionalProb[feature, l])
    util.raiseNotDefined()
    
    return logJoint
  
  def findHighOddsFeatures(self, label1, label2):
    """
    Returns the 100 best features for the odds ratio:
            P(feature=1 | label1)/P(feature=1 | label2) 
    """
    featuresOdds = []
    #self.features is the list of all possible features.
    #We want the best 100 features for each odds ratio so loop through all possible fatures
    for features in self.feature:
      featureOdds.append((self.conditionalProb[feature, label1]/self.conditionalProb[feature, label2], feature))
    
    #sort the odds from least to greatest
    featureOdds.sort()
    #print(featureOdds)
    #for each value in feature 
    #feature value = features in featureodds from -100:list
    featureOdds = [feature for val, feature in featuresOdds[-100:]]
    util.raiseNotDefined()

    return featuresOdds