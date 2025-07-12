document.addEventListener("DOMContentLoaded", function () {
  window.showDropdown = function (graphName) {
    const modal = document.getElementById('dropdownModal');
    const graphInput = document.getElementById('graphTypeInput');
    document.getElementById('selectedGraph').textContent = "Selected: " + graphName;
    graphInput.value = graphName;

    // Divs
    const labelDiv = document.getElementById('labelDiv');
    const xDiv = document.getElementById('xDiv');
    const yDiv = document.getElementById('yDiv');
    const hueDiv = document.getElementById('hueDiv');
    const paletteDiv = document.getElementById('paletteDiv');
    const legendDiv = document.getElementById('legendDiv');

    // Reset all to visible (default)
    [labelDiv, xDiv, yDiv, hueDiv, paletteDiv, legendDiv].forEach(div => {
      div.style.display = 'block';
    });

    const lower = graphName.toLowerCase();

    if (lower === 'pie chart') {
      labelDiv.style.display = 'block';
      xDiv.style.display = 'none';
      yDiv.style.display = 'none';
      hueDiv.style.display = 'none';
      paletteDiv.style.display = 'block';
      legendDiv.style.display = 'block';
    } else if (lower === 'heatmap') {
      [labelDiv, xDiv, yDiv, hueDiv, paletteDiv, legendDiv].forEach(div => {
        div.style.display = 'none';
      });
    } else if (lower === 'histogram' || lower === 'count plot') {
      labelDiv.style.display = 'none';
      yDiv.style.display = 'none';
      hueDiv.style.display = 'none';
      paletteDiv.style.display = 'block';
      legendDiv.style.display = 'none';
    } else {
      labelDiv.style.display = 'none';
    }

    modal.style.display = 'flex';
  };

  window.closeDropdown = function () {
    document.getElementById('dropdownModal').style.display = 'none';
  };

  window.onclick = function (event) {
    const modal = document.getElementById('dropdownModal');
    if (event.target === modal) {
      modal.style.display = 'none';
    }
  };
});
