import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

def create_line_plot():
    # Clear any old figure
    plt.clf()

    # Create sample data
    df = pd.DataFrame({
        'x': [1, 2, 3, 4],
        'y': [10, 20, 25, 30]
    })

    # Create plot
    plt.figure(figsize=(6, 4))
    sns.lineplot(data=df, x='x', y='y')
    
    # Save to in-memory buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return buf
