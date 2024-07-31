import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

# Example data
chapters = ['Prologue', 'Chapter 1', 'Chapter 2', "Chapter 3", "Chapter 4"]
scenes_word_counts = [
    [2627],  # Prologue
    [1951, 1968, 1695],  # Chapter 1
    [1472, 2503],  # Chapter 2
    [2003, 2138, 1558, 1975], # Chapter 3
    [1] # Chapter 4
]

plt.style.use('dark_background')

# Determine the number of chapters and maximum number of scenes per chapter
num_chapters = len(chapters)
max_scenes = max(len(scene) for scene in scenes_word_counts)

# Initialize the bottom of the bars for the stacked bar chart
bottom = np.zeros(num_chapters)

cmap = mpl.colormaps["Dark2"]

# Create subplots
fig, axs = plt.subplots(2, 2, figsize=(15, 10))

# Plot 1: Stacked Bar Chart of Word Counts per Scene in Each Chapter
ax1 = axs[0, 0]
for i in range(max_scenes):
    scene_word_counts = []
    for j in range(num_chapters):
        if i < len(scenes_word_counts[j]):
            scene_word_counts.append(scenes_word_counts[j][i])
        else:
            scene_word_counts.append(0)
    bars = ax1.bar(chapters, scene_word_counts, bottom=bottom, label=f'Scene {i+1}', color=cmap(i))
    for bar, wc in zip(bars, scene_word_counts):
        if wc > 0:
            ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2,
                     f'{wc}', ha='center', va='center', color='white', fontsize=8, fontweight='bold')
    bottom += scene_word_counts
ax1.set_xlabel('Chapters')
ax1.set_ylabel('Word Count')
ax1.set_title('Word Count per Scene in Each Chapter')
ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# Calculate total and average word counts
total_word_counts = [sum(scenes) for scenes in scenes_word_counts]
total_word_count = sum(total_word_counts)
total_scenes = sum(len(scenes) for scenes in scenes_word_counts)
avg_word_count_per_scene = total_word_count / total_scenes
avg_word_count_per_chapter = [sum(scenes) / len(scenes) for scenes in scenes_word_counts]
overall_avg_word_count_per_chapter = total_word_count / num_chapters
median_word_count_per_chapter = [np.median(scenes) for scenes in scenes_word_counts]
std_dev_word_count_per_chapter = [np.std(scenes) for scenes in scenes_word_counts]

# Cumulative word count
cumulative_word_count = np.cumsum([wc for chapter in scenes_word_counts for wc in chapter])
cumulative_word_count = np.insert(cumulative_word_count, 0, 0)  # Insert zero at the start

# Plot 2: Cumulative Word Count Plot
ax2 = axs[0, 1]
ax2.plot(range(len(cumulative_word_count)), cumulative_word_count, marker='o')
ax2.set_xlabel('Scene Index')
ax2.set_ylabel('Cumulative Word Count')
ax2.set_title('Cumulative Word Count Across Scenes')

# Plot 3: Histogram of Scene Lengths
scene_lengths = [wc for chapter in scenes_word_counts for wc in chapter]
ax3 = axs[1, 0]
ax3.hist(scene_lengths, bins=10, edgecolor='black')
ax3.set_xlabel('Word Count')
ax3.set_ylabel('Frequency')
ax3.set_title('Distribution of Scene Lengths')

# Plot 4: Bar Chart of Number of Scenes per Chapter
num_scenes_per_chapter = [len(scenes) for scenes in scenes_word_counts]
ax4 = axs[1, 1]
ax4.bar(chapters, num_scenes_per_chapter, color='skyblue')
for i, num_scenes in enumerate(num_scenes_per_chapter):
    ax4.text(i, num_scenes + 0.1, str(num_scenes), ha='center', va='bottom')
ax4.set_xlabel('Chapters')
ax4.set_ylabel('Number of Scenes')
ax4.set_title('Number of Scenes per Chapter')

# Milestone scenes for forecasting
milestone_scenes = np.arange(10, 35, 5)

# Forecasting word counts
forecasted_word_counts = []
for milestone in milestone_scenes:
    # Project based on average scene word count
    avg_scene_word_count = np.mean(scene_lengths)
    projected_wc_avg = avg_scene_word_count * milestone
    
    # Project based on average chapter word count and std deviation
    avg_chapter_word_count = np.mean(total_word_counts)
    std_dev_chapter_word_count = np.mean(std_dev_word_count_per_chapter)
    projected_wc_chapter = avg_chapter_word_count * (milestone / (total_scenes / num_chapters))
    projected_wc_chapter_with_std_dev = projected_wc_chapter + std_dev_chapter_word_count
    
    forecasted_word_counts.append({
        'milestone': milestone,
        'projected_wc_avg': projected_wc_avg,
        'projected_wc_chapter': projected_wc_chapter,
        'projected_wc_chapter_with_std_dev': projected_wc_chapter_with_std_dev
    })

# Add forecasts to the cumulative plot
ax2.scatter([m for m in milestone_scenes], 
            [forecast['projected_wc_chapter'] for forecast in forecasted_word_counts], 
            color='red', marker='x', label='Forecasted (Chapter Avg)')
ax2.scatter([m for m in milestone_scenes], 
            [forecast['projected_wc_avg'] for forecast in forecasted_word_counts], 
            color='blue', marker='o', label='Forecasted (Scene Avg)')

# Add the legend for forecasted points
ax2.legend(loc='best')

# Adjust layout to make room for the legend in the first plot
plt.tight_layout()

# Show all plots
plt.show()

# Print statistics
print(f"Total word count: {total_word_count}")
print(f"Overall average word count per chapter: {overall_avg_word_count_per_chapter:.2f}")
print(f"Average word count per scene: {avg_word_count_per_scene:.2f}")
for i, (avg, median, std_dev) in enumerate(zip(avg_word_count_per_chapter, median_word_count_per_chapter, std_dev_word_count_per_chapter)):
    print(f"Chapter {i+1}:")
    print(f"  Average word count: {avg:.2f}")
    print(f"  Median word count: {median:.2f}")
    print(f"  Standard deviation: {std_dev:.2f}")

print(f"Cumulative word count: {max(cumulative_word_count)}")