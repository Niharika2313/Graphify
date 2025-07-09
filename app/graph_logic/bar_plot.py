import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

def create_bar_plot():
    # Clear previous plots to avoid overlapping
    plt.clf()
    
    # Create a sample DataFrame
    df = pd.DataFrame({'fruits': ['Apple', 'Banana', 'Mango'], 'count': [5, 7, 3]})
    
    # Make the plot
    plt.figure(figsize=(6, 4))
    sns.barplot(data=df, x='fruits', y='count')
    
    # Save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf
