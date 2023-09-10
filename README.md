# LeadSquared-assignment
Extract insights about customer satisfaction and review subjects from textual reviews

For inference:
 Kindly use the inference.py file to get outputs on a dataset.
 Set the filename to the data file and put in the input text column name before running the script.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ABOUT THE WORK


Assumptions:
 - Assuming the business team needs more context of the product's impression on the customers for product development, they will be more concerned to get the subject information and the supporting phrase to determine customer satisfaction for the subject


Approach:
 - Since the data is not annotated, an unsupervised or semi-supervised approach will be the way to go.
 - We first get the possible subjects from the reviews using spacy for all sentences of a review.
 - We now have all the possible subjects for a review
 - the plan was to then decide the most sentimental subject for the review using an LLM and then  run clustering on dimensinally reduced embeddings of each os those sentimental subjects to get similar subjects grouped together, and we can substitute those subjects by a single cluster subject. THis way the business team will see a small number of subjects, and they can opt to see more details about the review and its sentimental subject if they are interested in the cluster (based on business use-case)

Problems faced:
 - Assumed the Roberta LLM to have a poor but usable performance for sentiment classification on the subjects. The model however was predicting almost equal values for any sentimental phrase, so without training for the downstream task, the model isn't ready for a classification problem.

Alternate approach:
 - Performed a clustering on dimensionally reduced ebeddings of all individual subjects derived from sentences in the reviews, for smaller groups (upto 8) the groups were not insightful for a business with noisy data points. The subject was largely generalised (for ex: subjects talking about dress style clustered together, subjects talking about the dimensions of dress clustered together, some complaining subjects clustered together). The business team will not benefit from summarized insights of subjects without data on the customer satisfaction in the summary. The dimensionality reduction probably resulted in a lot of data loss for the KMeans model to differentiate between subjects at the ground level.
