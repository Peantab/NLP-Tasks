1. Which measure works better for the problem?

    LLR works better, by choosing bigrams that are more semantically associated.

2. What would be needed, besides good measure, to build a dictionary of multiword expressions?
    * elimination of splitting words into two lines (resulting pieces are meaningless and they only exist together, so for LLR and PMI they are perfect bigrams),
    * bigger corpus which is not homogeneous in style and topic,
    * good definition of a multiword expression (is *w ustawie* a multiword expression?),
    * removing bigrams containing stopwords (if answer for the previous question is *no*), 
    * providing extensions for abbreviations,
    * performing probability calculations on lemmatized text (but results may be more accurately presented not lemmatized, with respect to inflection - *w droga rozporządzenie* make little sense).
    
3. Can you identify a certain threshold which clearly divides the *good* expressions from the *bad*?
    * PMI - very big amount of top bigrams got the same value of PMI and they are of mixed quality - no threshold;
    * LLR - the very first bigram is not very good, so there is no such absolute threshold, though quality decreases around 3e-6.