// Get modal element
const modal = document.getElementById("dropdownModal");

// Get all the form option divs
const heatmapDiv = document.getElementById("heatmapDiv");
const labelDiv = document.getElementById("labelDiv");
const xDiv = document.getElementById("xDiv");
const yDiv = document.getElementById("yDiv");
const hueDiv = document.getElementById("hueDiv");
const legendDiv = document.getElementById("legendDiv");

// Get the hidden input and the title
const graphTypeInput = document.getElementById("graphTypeInput");
const selectedGraphTitle = document.getElementById("selectedGraph");

// Function to open and configure the modal
function showDropdown(graphType) {
  // --- 1. Reset all fields to hidden ---
  heatmapDiv.style.display = "none";
  labelDiv.style.display = "none";
  xDiv.style.display = "none";
  yDiv.style.display = "none";
  hueDiv.style.display = "none";
  legendDiv.style.display = "block"; // Default to showing legend option

  // --- 2. Set the graph type in the hidden input and title ---
  graphTypeInput.value = graphType;
  selectedGraphTitle.textContent = `Selected: ${graphType}`;

  // --- 3. Show only the relevant fields based on graph type ---
  if (graphType === "Heatmap") {
    heatmapDiv.style.display = "block";
    legendDiv.style.display = "none"; // Legend is not applicable for heatmap
  } else if (graphType === "Pie Chart") {
    labelDiv.style.display = "block";
  } else if (graphType === "Histogram" || graphType === "Count Plot") {
    xDiv.style.display = "block";
    hueDiv.style.display = "block"; // Hue is applicable
  } else {
    // For Line, Bar, Scatter, Box, Violin plots
    xDiv.style.display = "block";
    yDiv.style.display = "block";
    hueDiv.style.display = "block";
  }

  // --- 4. Display the modal ---
  modal.style.display = "flex"; // Using flex to align with your CSS
}

// Function to close the modal
function closeDropdown() {
  modal.style.display = "none";
}

// Close the modal if the user clicks outside of the modal content
window.onclick = function(event) {
  if (event.target == modal) {
    closeDropdown();
  }
};

// --- Optional: Flash Message Auto-dismiss ---
document.addEventListener("DOMContentLoaded", function () {
    const messages = document.querySelectorAll('.flash-message');
    messages.forEach(msg => {
        setTimeout(() => {
            // Start fading out
            msg.style.transition = 'opacity 0.5s ease';
            msg.style.opacity = '0';
            // Remove from DOM after fade out transition ends
            setTimeout(() => msg.remove(), 500); 
        }, 4000); // Start fade out after 4 seconds
    });
});