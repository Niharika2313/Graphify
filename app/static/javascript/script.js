function showDropdown(graphName) {
  const modal = document.getElementById('dropdownModal');
  const selectedGraph = document.getElementById('selectedGraph');
  const graphTypeInput = document.getElementById('graphTypeInput');

  modal.style.display = 'flex';
  selectedGraph.textContent = "Selected: " + graphName;
  graphTypeInput.value = graphName;
}

function closeDropdown() {
  const modal = document.getElementById('dropdownModal');
  modal.style.display = 'none';
}

window.onclick = function (event) {
  const modal = document.getElementById('dropdownModal');
  if (event.target === modal) {
    modal.style.display = 'none';
  }
}
