A real project for an Internet provider. 

There is a support service in which different groups of employees are responsible for different issues. There is a chat bot. It is necessary, according to the first phrase of the customer (first phrase is customer's question), to determine the class of conversation, for the further transfer to the appropriate group of operators. The labeling of the training set took place in a semi-automatic mode. When the support staff finishes a conversation with a customer, they indicate the topic of the conversation. Based on these themes, a dataset was formed.

Solution:
1. Select the first phrase of the customer
2. Preprocessing
3. Tokenization
4. Building word embeddings (word2vec)
5. Solution 1. We get the embedding of the sentence (the arithmetic mean of the word embeddings included in sentence). Using SVM for classification
6. Solution 2. We use NN (Input->LSTM->Dropout->Dense(softmax)->Output) based on existing word embeddings. Input is the sequence of words embedding included in the sentence. Sequence length is fixed.  