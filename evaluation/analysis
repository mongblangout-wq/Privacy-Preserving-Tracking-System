import pandas as pd
import matplotlib.pyplot as plt

csv_file = 'auto_evaluation_sum.csv'
df = pd.read_csv(csv_file)

mosaic_data = df[df['method'] == 'mosaic']
if not mosaic_data.empty:
    pivot_recall = mosaic_data.pivot_table(
        index='intensity', 
        columns='model', 
        values='recall', 
        aggfunc='mean'
    )
    
    pivot_recall.plot(kind='bar', figsize=(8, 5))
    plt.title('Recall by Mosaic Intensity (YOLOv8n vs YOLOv8s)')
    plt.xlabel('Intensity')
    plt.ylabel('Recall')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('model_recall_comparison.png')
    plt.show()

target_data = df[df['method'].isin(['mosaic', 'blur'])]
if not target_data.empty:
    pivot_mota = target_data.pivot_table(
        index='intensity', 
        columns='target', 
        values='mota', 
        aggfunc='mean'
    )
    
    pivot_mota.plot(marker='o', figsize=(8, 5))
    plt.title('MOTA Degradation: Face vs Person')
    plt.xlabel('Intensity')
    plt.ylabel('MOTA')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig('target_mota_comparison.png')
    plt.show()