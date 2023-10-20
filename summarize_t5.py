from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

def chunk_text(text, chunk_size=512):
    """Split the text into chunks of size `chunk_size`."""
    words = text.split(' ')
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

def remove_duplicates(text):
    # Split the text into sentences
    sentences = re.split('(?<=[.!?]) +', text)
    
    # Compute TF-IDF vectors for each sentence
    vectorizer = TfidfVectorizer().fit_transform(sentences)
    
    # Compute pairwise cosine similarity between the sentences
    similarity_matrix = cosine_similarity(vectorizer)
    
    # Find pairs of sentences where the similarity score is above the threshold
    similar_pairs = np.argwhere(similarity_matrix > 0.8)
    
    # Get the indices of sentences to remove
    indices_to_remove = [pair[1] for pair in similar_pairs if pair[0] != pair[1]]
    
    # Remove similar sentences
    unique_sentences = [sentence for i, sentence in enumerate(sentences) if i not in indices_to_remove]
    
    return ' '.join(unique_sentences)
    
class TextSummarization:
    tokenizer = AutoTokenizer.from_pretrained('t5-base', model_max_length=512)
    model = AutoModelForSeq2SeqLM.from_pretrained('t5-base', return_dict=True)

    def summarize_text_t5(self, text : str):
        chunks = chunk_text(text)
        summaries = []

        for chunk in chunks:
            inputs = self.tokenizer.encode("summarize: " + chunk,
                                    return_tensors='pt',
                                    max_length=512,
                                    truncation=True)

            summary_ids = self.model.generate(inputs, max_length=512, min_length=80, length_penalty=5., num_beams=2)
            summary = self.tokenizer.decode(summary_ids[0])

            # Remove the special tokens
            summary = summary.replace('<pad>', '').replace('</s>', '').strip()

            summaries.append(summary)

        summaries_nodup = remove_duplicates(' '.join(summaries))

        # Check if the last sentence ends with . ! or ?
        sentences = re.split('(?<=[.!?]) +', summaries_nodup)

        # capitalize sentences
        sentences = [sentence.capitalize() for sentence in sentences]

        if sentences[-1][-1] not in ['.', '!', '?']:
            final_summary = ' '.join(sentences[:-1])
        else:
            final_summary = ' '.join(sentences)

        return final_summary
    
if __name__ == "__main__":
    import argparse

    # Create the parser
    parser = argparse.ArgumentParser(description='Summarize a text.')

    # Add the arguments
    parser.add_argument('text', type=str, help='Text to summarize.')

    # Parse the arguments
    args = parser.parse_args()

    # handle arguments
    if len(args.text) < 80:
        raise Exception("Text's length must be longer or equal to 80 characters.")

    summarizer = TextSummarization()

    print(summarizer.summarize_text_t5(args.text))