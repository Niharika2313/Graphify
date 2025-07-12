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
    palette = request.form.get('palette')
    label_column = request.form.get('label_column')
    show_legend = request.form.get('show_legend') == 'on'

    if not graph_type:
        return "Missing graph type", 400

    plt.clf()
    plt.figure(figsize=(10, 6))

    try:
        gtype = graph_type.lower()
        kwargs = {}

        if hue:
            kwargs['hue'] = hue
            kwargs['palette'] = palette if palette else 'Set2'
        else:
            if gtype != 'pie chart':  # pie handles color differently
                kwargs['color'] = color

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
            numeric_df = df.select_dtypes(include='number')
            if 'SR No' in numeric_df.columns:
                numeric_df = numeric_df.drop(columns=['SR No'])
            corr = numeric_df.corr()
            sns.heatmap(corr, annot=True, cmap='Blues')
        elif gtype == 'pie chart':
            if not label_column:
                return "Label column is required for pie chart", 400

            pie_data = df[label_column].value_counts()
            colors = sns.color_palette(palette if palette else 'Set2', len(pie_data))
            wedges, texts, autotexts = plt.pie(
                pie_data,
                labels=pie_data.index,
                autopct='%1.1f%%',
                startangle=90,
                colors=colors
            )
            if show_legend:
                plt.legend(wedges, pie_data.index, title=label_column, bbox_to_anchor=(1, 0.5))
            plt.axis('equal')  # makes the pie chart a circle
        else:
            return "Unsupported chart type", 400

        if gtype not in ['heatmap', 'pie chart'] and show_legend and hue:
            plt.legend(title=hue)
        elif gtype not in ['heatmap', 'pie chart']:
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
