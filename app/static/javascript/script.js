document.addEventListener("DOMContentLoaded", function () {
  // --- Graph Modal Dropdown Logic ---
  window.showDropdown = function (graphName) {
    const modal = document.getElementById('dropdownModal');
    const graphInput = document.getElementById('graphTypeInput');
    document.getElementById('selectedGraph').textContent = "Selected: " + graphName;
    graphInput.value = graphName;

    const labelDiv = document.getElementById('labelDiv');
    const xDiv = document.getElementById('xDiv');
    const yDiv = document.getElementById('yDiv');
    const hueDiv = document.getElementById('hueDiv');
    const paletteDiv = document.getElementById('paletteDiv');
    const legendDiv = document.getElementById('legendDiv');

    [labelDiv, xDiv, yDiv, hueDiv, paletteDiv, legendDiv].forEach(div => {
      if (div) div.style.display = 'block';
    });

    const lower = graphName.toLowerCase();

    if (lower === 'pie chart') {
      if (labelDiv) labelDiv.style.display = 'block';
      if (xDiv) xDiv.style.display = 'none';
      if (yDiv) yDiv.style.display = 'none';
      if (hueDiv) hueDiv.style.display = 'none';
      if (paletteDiv) paletteDiv.style.display = 'block';
      if (legendDiv) legendDiv.style.display = 'block';
    } else if (lower === 'heatmap') {
      [labelDiv, xDiv, yDiv, hueDiv, paletteDiv, legendDiv].forEach(div => {
        if (div) div.style.display = 'none';
      });
    } else if (lower === 'histogram' || lower === 'count plot') {
      if (labelDiv) labelDiv.style.display = 'none';
      if (yDiv) yDiv.style.display = 'none';
      if (hueDiv) hueDiv.style.display = 'none';
      if (paletteDiv) paletteDiv.style.display = 'block';
      if (legendDiv) legendDiv.style.display = 'none';
    } else {
      if (labelDiv) labelDiv.style.display = 'none';
      // others stay visible
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

  // --- Flash Message Auto-dismiss ---
  const messages = document.querySelectorAll('.flash-message');
  messages.forEach(msg => {
    setTimeout(() => {
      msg.style.opacity = '0';
      setTimeout(() => msg.remove(), 500); // remove after fade out
    }, 4000); // 4 seconds
  });
});
