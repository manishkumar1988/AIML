# Glossary

Plain-language definitions. The number in brackets is the challenge where the term first matters.

## Data and evaluation

| Term | Meaning |
| --- | --- |
| **Feature** | An input column the model uses (age, price, pixel value). |
| **Label / target** | The answer you want the model to predict. |
| **Training set** [02] | Data the model learns from. |
| **Validation (dev) set** [02] | Data you use to make choices: which model, which settings. |
| **Test set** [02] | Data you look at **once**, at the end, to report the final score. If you make choices using it, the score lies. |
| **Baseline** [02] | The simplest possible "model" (predict the average, the most common class, "same as last week"). Your model must beat it to be useful. |
| **Overfitting** [02] | The model memorizes training data and does worse on new data. Training score high, validation score low. |
| **Underfitting** | The model is too simple to learn the pattern. Both scores are low. |
| **Data leakage** [06] | Information from the answer, or from the future, sneaks into the inputs. Scores look amazing and then fail in real use. |
| **Cross-validation** [07] | Split training data into k parts; train k times, each time validating on a different part. Gives a more stable estimate. |
| **Hyperparameter** [07] | A setting you choose (tree depth, learning rate), as opposed to a parameter the model learns. |
| **Pipeline** [03] | Preprocessing + model bundled together, so the same steps run on training and new data, and preprocessing only learns from training data. |

## Metrics

| Term | Meaning |
| --- | --- |
| **MAE** [02] | Mean absolute error. Average size of the mistake, in the target's units. Easy to explain. |
| **RMSE** [02] | Root mean squared error. Like MAE but punishes big mistakes more. |
| **Accuracy** [03] | Fraction of predictions that are correct. Misleading when classes are imbalanced. |
| **Precision** [03] | Of the items the model flagged, how many were really positive? "When it says yes, is it right?" |
| **Recall** [03] | Of the real positives, how many did the model find? "Does it miss things?" |
| **F1** [03] | One number combining precision and recall (their harmonic mean). |
| **Confusion matrix** [03] | A table of predicted vs actual classes. Shows exactly which mistakes happen. |
| **Threshold** [04] | The score above which you say "yes." Moving it trades precision for recall. |
| **ROC-AUC** [03] | How well the model ranks positives above negatives. Can look good even when the rare class is badly handled. |
| **PR-AUC / average precision** [04] | Area under the precision-recall curve. Better than ROC-AUC for rare classes. |
| **Macro-F1** [15] | Average F1 across classes, each class counted equally. Good when small classes matter. |
| **IoU** [13] | Intersection over union. How much a predicted box or mask overlaps the true one (0 to 1). |
| **mAP** [13] | Mean average precision. The standard object-detection score. |
| **Perplexity** [24] | How "surprised" a language model is by held-out text. Lower is better. Only comparable between models with the same tokenizer. |
| **Recall@k** [30] | In retrieval: did the right document appear in the top k results? |
| **MRR** [30] | Mean reciprocal rank. Rewards putting the right document near the top. |
| **Faithfulness** [31] | Does the generated answer only say things supported by the retrieved sources? |

## Deep learning

| Term | Meaning |
| --- | --- |
| **Neuron / layer** [09] | A weighted sum followed by a nonlinearity. Layers are stacks of them. |
| **Activation function** [09] | The nonlinearity (ReLU, sigmoid). Without it, a deep network collapses into a linear model. |
| **Loss** [09] | A number measuring how wrong the model is. Training tries to make it smaller. |
| **Gradient** [09] | The direction that increases the loss fastest. You step the other way. |
| **Backpropagation** [09] | The chain rule, applied layer by layer, to compute gradients. |
| **Learning rate** [09] | Step size. Too big: loss explodes. Too small: nothing happens. |
| **Epoch** [10] | One full pass over the training data. |
| **Batch** [10] | A small group of examples processed together. |
| **Optimizer** [10] | The rule for updating weights (SGD, Adam, AdamW). |
| **CNN** [10] | Convolutional neural network. Learns local patterns in images. |
| **Regularization** [11] | Anything that reduces overfitting: dropout, weight decay, augmentation, early stopping. |
| **Data augmentation** [11] | Randomly altering training images (flip, crop, color) so the model generalizes. |
| **Transfer learning** [12] | Start from a model pretrained on a big dataset, adapt it to yours. |
| **Backbone** [12] | The pretrained feature-extracting part of a vision model. |
| **Embedding** [15] | A learned vector that represents a word, sentence, or item, where similar things are close together. |
| **RNN / LSTM** [15] | Networks that read sequences one step at a time, carrying a memory. |
| **Attention** [16] | A way for each token to look at every other token and decide which ones matter. |
| **Transformer** [16] | Architecture built from attention + feed-forward layers. Basis of modern LLMs. |
| **Autoencoder** [17] | Network that compresses input to a small code and reconstructs it. |
| **VAE** [17] | Variational autoencoder. An autoencoder whose code space you can sample new data from. |
| **Diffusion model** [18] | Generates data by learning to remove noise, step by step. |

## Language models

| Term | Meaning |
| --- | --- |
| **Token** [19] | A chunk of text the model reads: a word, part of a word, or a character. |
| **Tokenizer** [22] | Splits text into tokens and maps them to ids. |
| **BPE** [22] | Byte-pair encoding. Builds a vocabulary by repeatedly merging frequent character pairs. |
| **Fertility** [22] | Average number of tokens per word. Lower usually means a better-fitting tokenizer. |
| **Context window** [23] | The maximum number of tokens a model can see at once. |
| **Causal mask** [23] | Stops a token from looking at future tokens during training. |
| **Pretraining** [24] | Training on lots of raw text to predict the next token. |
| **Fine-tuning** [20] | Further training a pretrained model on a specific task. |
| **Instruction tuning / SFT** [25] | Fine-tuning on (instruction, response) pairs so the model follows requests. |
| **Temperature** [24] | Sampling randomness. 0 = always the most likely token; higher = more varied. |
| **Top-k / top-p** [24] | Only sample from the k most likely tokens, or from the smallest set covering probability p. |
| **SLM** [24] | Small language model, roughly under a few billion parameters. |
| **Quantization** [26] | Storing weights with fewer bits (8-bit, 4-bit) to save memory. Slight quality loss. |
| **Prompt engineering** [26] | Designing the input text to get better outputs. |
| **Few-shot** [26] | Putting a few examples in the prompt. |
| **Structured output** [27] | Making the model return data in a fixed format, such as JSON matching a schema. |
| **Hallucination** [27] | The model states something false or unsupported, confidently. |
| **LLM-as-judge** [28] | Using an LLM to grade outputs. Must be checked against human labels before you trust it. |
| **LoRA** [32] | Low-rank adaptation. Fine-tunes a few small added matrices instead of all weights. |
| **QLoRA** [32] | LoRA on a model loaded in 4-bit, to save even more memory. |

## RAG and agents

| Term | Meaning |
| --- | --- |
| **RAG** [29] | Retrieval-augmented generation. Find relevant documents, then have the LLM answer using them. |
| **Chunk** [29] | A piece of a document, small enough to embed and retrieve. |
| **Vector database** [29] | Stores embeddings and finds the nearest ones quickly. |
| **BM25** [30] | Classic keyword search scoring. A strong, cheap baseline. |
| **Hybrid search** [30] | Combining keyword and embedding search. |
| **Reranker** [30] | A slower, more accurate model that re-orders the top retrieved results. |
| **Grounding** [31] | Tying every claim in an answer to a source. |
| **Agent** [34] | An LLM in a loop that decides which tool to call next, sees the result, and continues until done. |
| **Tool / function calling** [34] | The LLM outputs a structured request to run a function, and your code runs it. |
| **ReAct** [35] | An agent pattern: reason, act (call a tool), observe, repeat. |
| **MCP** [37] | Model Context Protocol. A standard way to expose tools and data to LLM applications. |
| **Guardrail** [35] | A limit or check around an agent: max steps, allowed tools, output validation. |

## Deployment

| Term | Meaning |
| --- | --- |
| **API endpoint** [38] | A URL that accepts input and returns a prediction. |
| **Latency** [38] | How long one request takes. Usually reported as p50 / p95. |
| **Throughput** [38] | How many requests per second you can serve. |
| **Docker** [38] | Packages your app and its environment so it runs the same everywhere. |
| **Drift** [39] | Live data starts to look different from training data, so the model gets worse. |
