const modal = document.getElementById("dropdownModal");
const heatmapDiv = document.getElementById("heatmapDiv");
const labelDiv = document.getElementById("labelDiv");
const xDiv = document.getElementById("xDiv");
const yDiv = document.getElementById("yDiv");
const hueDiv = document.getElementById("hueDiv");
const legendDiv = document.getElementById("legendDiv");
const paletteDiv = document.getElementById("paletteDiv");
const colorPickerDiv = document.getElementById("colorPickerDiv");

const graphTypeInput = document.getElementById("graphTypeInput");
const selectedGraphTitle = document.getElementById("selectedGraph");
const hueSelect = document.getElementById("hueSelect");

function toggleColorOptions() {
  if (hueSelect.value) {
    paletteDiv.style.display = "block";
    colorPickerDiv.style.display = "none";
  } else {
    paletteDiv.style.display = "none";
    colorPickerDiv.style.display = "block";
  }
}

hueSelect.addEventListener('change', toggleColorOptions);

function showDropdown(graphType) {
  const allOptionDivs = [heatmapDiv, labelDiv, xDiv, yDiv, hueDiv, legendDiv, paletteDiv, colorPickerDiv];
  allOptionDivs.forEach(div => div.style.display = "none");

  graphTypeInput.value = graphType;
  selectedGraphTitle.textContent = `Selected: ${graphType}`;

  if (graphType === "Heatmap") {
    heatmapDiv.style.display = "block";
  } else if (graphType === "Pie Chart") {
    labelDiv.style.display = "block";
    paletteDiv.style.display = "block";
    legendDiv.style.display = "block";
  } else if (graphType === "Histogram" || graphType === "Count Plot") {
    xDiv.style.display = "block";
    hueDiv.style.display = "block";
    legendDiv.style.display = "block";
    toggleColorOptions();
  } else {
    xDiv.style.display = "block";
    yDiv.style.display = "block";
    hueDiv.style.display = "block";
    legendDiv.style.display = "block";
    toggleColorOptions();
  }
  modal.style.display = "flex";
}

function closeDropdown() {
  modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    closeDropdown();
  }
};

document.addEventListener("DOMContentLoaded", function () {
    const messages = document.querySelectorAll('.flash-message');
    messages.forEach(msg => {
        setTimeout(() => {
            msg.style.transition = 'opacity 0.5s ease';
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 500); 
        }, 4000);
    });
});