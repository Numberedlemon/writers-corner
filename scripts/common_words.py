import os
import csv
from collections import defaultdict
import matplotlib.pyplot as plt

def read_csv_files(folder_path):
    word_counts = defaultdict(int)
    
    # Loop through all CSV files in the given folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 2:
                        word, count = row
                        try:
                            count = int(count)
                            word_counts[word] += count
                        except ValueError:
                            print(f"Skipping invalid count for word '{word}' in file {filename}")
    
    return word_counts

def rank_words(word_counts):
    # Sort words by count in descending order
    ranked_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    return ranked_words

def display_ranking(ranked_words, top_n=20):
    print(f"{'Rank':<5}{'Word':<15}{'Count':<10}")
    print('-' * 30)
    
    for rank, (word, count) in enumerate(ranked_words[:top_n], 1):
        print(f"{rank:<5}{word:<15}{count:<10}")

def plot_word_counts(ranked_words, top_n=20):
    # Get the top n words and their counts
    words = [word for word, count in ranked_words[:top_n]]
    counts = [count for word, count in ranked_words[:top_n]]

    # Create the bar plot
    plt.figure(figsize=(12, 8))
    plt.bar(words, counts, color='skyblue')
    
    # Add labels and title
    plt.xlabel('Words')
    plt.ylabel('Counts')
    plt.title('Top Words by Occurrence')
    plt.xticks(rotation=45, ha='right')
    
    # Add count labels on top of the bars
    for i in range(len(words)):
        plt.text(i, counts[i], str(counts[i]), ha='center', va='bottom')
    
    # Show the plot
    plt.tight_layout()
    plt.show()

# Main function to execute the steps
def main(folder_path, top_n=20):
    word_counts = read_csv_files(folder_path)
    ranked_words = rank_words(word_counts)
    display_ranking(ranked_words, top_n)
    plot_word_counts(ranked_words, top_n)

main("words/firefly", top_n=100)