# Graphify

Graphify is a powerful, web-based data visualization tool built with Flask, Matplotlib and Seaborn. Upload a CSV or Excel file and generate insightful graphs with just a few clicks — no coding required.

---

## 🌟 Features

- Upload CSV/Excel files
- Select graph type from a clean modal gallery
- Dynamically filter columns for:
  - X, Y, Hue
  - Label column (for pie charts)
  - Seaborn/Matplotlib palette options
- Legend toggle support
- Smart form that adapts based on selected graph type
- Flash messages for warnings and errors
- Responsive, modular CSS across all pages
- Clean UI and deployed web interface

---

## 🚀 How It Works

1. **Upload File**: Accepts `.csv` and `.xlsx`
2. **Select Graph Type**: Choose from bar, line, scatter, pie, heatmap, etc.
3. **Customize Inputs**:
   - Choose X, Y, hue, label column, palette
   - Options update based on graph type
4. **Generate Graph**: Renders using Seaborn/Matplotlib
5. **Download or share** your generated plot(feature yet to add)

---

## 💡 Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Data Visualization**: Seaborn, Matplotlib, Pandas
- **File Handling**: OpenPyXL (for `.xlsx` support)

---

## 🗂️ Project Structure

```
Graphify/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── static/
│   │   ├── css/
│   │   │   ├── common.css
│   │   │   ├── graph_gallery.css
│   │   │   ├── index.css
│   │   │   └── upload.css
│   │   ├── images/
│   │   ├── javascript/
│   │   │   └── script.js
│   │   └── Hero_video.mp4
│   └── templates/
│       ├── graph_gallery.html
│       ├── index.html
│       └── upload.html
│
├── ipl_2025_sample.csv       # Sample dataset
├── README.md
├── requirements.txt
└── run.py                    # Main Flask app entry point
```

---

## 🧪 Example Graph Types

> Since the app is deployed, visit the live demo to try these:
- Bar Plot  
- Line Plot  
- Scatter Plot  
- Pie Chart  
- Heatmap  

All graphs support custom hues and palettes.

---

## 📦 Installation

```bash
git clone https://github.com/your-username/graphify.git
cd graphify
pip install -r requirements.txt
python run.py
```

Visit `http://127.0.0.1:5000` in your browser.

---

## ⚙️ Requirements

- Python 3.7+
- Flask
- Seaborn
- Matplotlib
- Pandas
- OpenPyXL (for `.xlsx` support)

---

## 👤 Author


🔧 Built with ❤️ by [Niharika Nikhare](https://github.com/Niharika2313)

---