from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

def chunk_text(text, chunk_size=512):
    """Split the text into chunks of size `chunk_size`."""
    words = text.split(' ')
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks
    
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

            summary_ids = self.model.generate(inputs, max_length=150, min_length=80, length_penalty=5., num_beams=2)
            summary = self.tokenizer.decode(summary_ids[0])

            # Remove the special tokens
            summary = summary.replace('<pad>', '').replace('</s>', '').strip()

            summaries.append(summary)

        final_summary = ' '.join(summaries)
        
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