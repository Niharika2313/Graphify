from flask import Blueprint, render_template, request, send_file, redirect, flash, url_for
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import io

main = Blueprint('main', __name__)
temp_df = {}

AVAILABLE_PALETTES = sorted([
    "deep", "muted", "pastel", "dark", "colorblind", "bright",
    "Set1", "Set2", "Set3", "Paired", "Pastel1", "Pastel2", "Dark2", "Accent",
    "tab10", "tab20", "tab20b", "tab20c", "hls", "husl", "cubehelix",
    "rocket", "mako", "flare", "crest", "viridis", "plasma", "inferno", "magma", "cividis"
])

# NEW: Add a list of available colormaps for heatmaps
AVAILABLE_CMAPS = [
    'viridis', 'plasma', 'inferno', 'magma', 'cividis', 'Greys', 'Purples',
    'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd',
    'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn',
    'YlGn', 'coolwarm', 'bwr', 'seismic', 'rocket', 'mako'
]

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/upload', methods=['GET'])
def upload():
    return render_template('upload.html')

@main.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file and file.filename:
        filename = file.filename
        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(file)
            elif filename.endswith('.xlsx'):
                df = pd.read_excel(file)
            else:
                flash("Unsupported file type.", "error")
                return redirect(url_for('main.upload'))

            temp_df['data'] = df
            columns = df.columns.tolist()
            numeric_columns = df.select_dtypes(include='number').columns.tolist()
            flash("File uploaded successfully!", "success")
            
            # MODIFIED: Pass the new cmaps list to the template
            return render_template('graph_gallery.html',
                                   columns=columns,
                                   numeric_columns=numeric_columns,
                                   palettes=AVAILABLE_PALETTES,
                                   cmaps=AVAILABLE_CMAPS)

        except Exception as e:
            flash(f"Error processing file: {str(e)}", "error")
            return redirect(url_for('main.upload'))

    flash("No file was uploaded.", "error")
    return redirect(url_for('main.upload'))


@main.route('/plot', methods=['POST'])
def plot_graph():
    df = temp_df.get('data')
    if df is None:
        flash("No dataset found. Please upload again.", "error")
        return redirect(url_for('main.upload'))

    graph_type = request.form.get('graph_type')
    x = request.form.get('x_column')
    y = request.form.get('y_column')
    hue = request.form.get('hue_column')
    label_column = request.form.get('label_column')
    palette = request.form.get('palette') or 'Set2'
    show_legend = request.form.get('show_legend') == 'on'
    color_selection = request.form.get('color_picker')
    # NEW: Get the selected colormap from the form
    cmap_selection = request.form.get('cmap_selection')

    if not graph_type:
        flash("Graph type is required", "error")
        return redirect(url_for('main.upload'))

    gtype = graph_type.lower()

    if gtype == 'pie chart':
        if not label_column:
            flash("Label column is required for Pie Chart", "error")
            return redirect(url_for('main.upload'))
        pie_data = df[label_column].value_counts()
    elif gtype != 'heatmap' and (not x or (gtype not in ['histogram', 'count plot'] and not y)):
        flash("Missing required fields (X or Y axis)", "error")
        return redirect(url_for('main.upload'))

    plt.clf()

    try:
        if gtype == 'heatmap':
            selected_columns = request.form.getlist('heatmap_columns')
            if not selected_columns or len(selected_columns) < 2:
                flash("Please select at least two numeric columns for the heatmap.", "error")
                return redirect(url_for('main.upload'))
            corr = df[selected_columns].corr()
            plt.figure(figsize=(10, 8))
            # MODIFIED: Use the selected cmap, with 'viridis' as a fallback
            sns.heatmap(corr, annot=True, cmap=cmap_selection or 'viridis')

        elif gtype == 'pie chart':
            colors = sns.color_palette(palette, len(pie_data))
            plt.figure(figsize=(7, 7))
            plt.pie(pie_data, labels=pie_data.index, colors=colors, autopct='%1.1f%%')
            if show_legend:
                plt.legend(pie_data.index, title=label_column, loc='best')

        else: 
            width = max(6, min(20, df[x].nunique() * 0.4))
            plt.figure(figsize=(width, 5))
            kwargs = {}
            if hue:
                kwargs['hue'] = hue
                kwargs['palette'] = palette
            elif color_selection:
                kwargs['color'] = color_selection
            
            if gtype == 'line plot':
                sns.lineplot(data=df, x=x, y=y, **kwargs)
            elif gtype == 'bar plot':
                sns.barplot(data=df, x=x, y=y, **kwargs)
            elif gtype == 'histogram':
                sns.histplot(data=df, x=x, **kwargs)
            elif gtype == 'count plot':
                sns.countplot(data=df, x=x, **kwargs)
            elif gtype == 'scatter plot':
                sns.scatterplot(data=df, x=x, y=y, **kwargs)
            elif gtype == 'box plot':
                sns.boxplot(data=df, x=x, y=y, **kwargs)
            elif gtype == 'violin plot':
                sns.violinplot(data=df, x=x, y=y, **kwargs)
            else:
                flash("Unsupported chart type", "error")
                return redirect(url_for('main.upload'))

            if show_legend and hue:
                plt.legend(title=hue)
            elif not show_legend:
                if plt.gca().get_legend() is not None:
                    plt.gca().get_legend().remove()
            plt.xticks(rotation=30, ha='right')

        plt.tight_layout()

    except Exception as e:
        flash(f"Error while plotting: {str(e)}", "error")
        return redirect(url_for('main.upload'))

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return send_file(buf, mimetype='image/png')