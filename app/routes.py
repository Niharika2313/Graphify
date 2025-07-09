from flask import Blueprint, render_template, request, send_file, redirect
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import io

main = Blueprint('main', __name__)
temp_df = {}  # In-memory store for uploaded data

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/upload', methods=['GET'])
def upload():
    return render_template('upload.html')

@main.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file:
        filename = file.filename
        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(file)
            elif filename.endswith('.xlsx'):
                df = pd.read_excel(file)
            else:
                return "Unsupported file type", 400

            temp_df['data'] = df
            columns = df.columns.tolist()
            return render_template('graph_gallery.html', columns=columns)

        except Exception as e:
            return f"Error processing file: {str(e)}", 500

    return redirect('/')

@main.route('/plot', methods=['POST'])
def plot_graph():
    df = temp_df.get('data')
    if df is None:
        return "No dataset found. Please upload again.", 400

    graph_type = request.form.get('graph_type')
    x = request.form.get('x_column')
    y = request.form.get('y_column')

    if not (x and y and graph_type):
        return "Missing input data", 400

    plt.clf()

    plt.figure(figsize=(6, 4))

    try:
        if graph_type.lower() == 'line plot':
            sns.lineplot(data=df, x=x, y=y)
        elif graph_type.lower() == 'bar plot':
            sns.barplot(data=df, x=x, y=y)
        elif graph_type.lower() == 'histogram':
            sns.histplot(data=df, x=x)
        elif graph_type.lower() == 'scatter plot':
            sns.scatterplot(data=df, x=x, y=y)
        elif graph_type.lower() == 'count plot':
            sns.countplot(data=df, x=x)
        elif graph_type.lower() == 'box plot':
            sns.boxplot(data=df, x=x, y=y)
        elif graph_type.lower() == 'violin plot':
            sns.violinplot(data=df, x=x, y=y)
        elif graph_type.lower() == 'heatmap':
            corr = df.corr(numeric_only=True)
            sns.heatmap(corr, annot=True, cmap='Blues')
        else:
            return "Unsupported chart type", 400
    except Exception as e:
        return f"Error while plotting: {str(e)}", 500

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return send_file(buf, mimetype='image/png')
