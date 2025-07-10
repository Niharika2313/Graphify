from flask import Blueprint, render_template, request, send_file, redirect
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import io

main = Blueprint('main', __name__)
temp_df = {}

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
    hue = request.form.get('hue_column')
    color = request.form.get('color', '#1f77b4')
    show_legend = request.form.get('show_legend') == 'on'

    if not graph_type or not x:
        return "Missing graph type or x-axis", 400
    if graph_type.lower() not in ['heatmap', 'pie chart'] and not y:
        return "Missing y-axis for this graph type", 400

    plt.clf()

    # Adjust figure size based on number of unique x-tick labels
    num_labels = df[x].nunique()
    width = max(6, min(20, num_labels * 0.4))
    plt.figure(figsize=(width, 5))

    try:
        kwargs = {}
        if hue:
            kwargs['hue'] = hue
            kwargs['palette'] = 'Set2'
        else:
            kwargs['color'] = color

        gtype = graph_type.lower()
        if gtype == 'line plot':
            sns.lineplot(data=df, x=x, y=y, **kwargs)
        elif gtype == 'bar plot':
            sns.barplot(data=df, x=x, y=y, **kwargs)
        elif gtype == 'histogram':
            sns.histplot(data=df, x=x, **kwargs)
        elif gtype == 'scatter plot':
            sns.scatterplot(data=df, x=x, y=y, **kwargs)
        elif gtype == 'count plot':
            sns.countplot(data=df, x=x, **kwargs)
        elif gtype == 'box plot':
            sns.boxplot(data=df, x=x, y=y, **kwargs)
        elif gtype == 'violin plot':
            sns.violinplot(data=df, x=x, y=y, **kwargs)
        elif gtype == 'heatmap':
            corr = df.corr(numeric_only=True)
            sns.heatmap(corr, annot=True, cmap='Blues')
        elif gtype == 'pie chart':
            pie_data = df[x].value_counts()
            plt.pie(pie_data, labels=pie_data.index, colors=[color]*len(pie_data), autopct='%1.1f%%')
        else:
            return "Unsupported chart type", 400

        if show_legend and hue and gtype not in ['heatmap', 'pie chart']:
            plt.legend(title=hue)
        else:
            plt.legend([], [], frameon=False)

        plt.xticks(rotation=30)
        plt.tight_layout()

    except Exception as e:
        return f"Error while plotting: {str(e)}", 500

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return send_file(buf, mimetype='image/png')
