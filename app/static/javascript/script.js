function showDropdown(graphName) {
  const dropdownSection = document.getElementById('dropdownSection');
  const selectedGraph = document.getElementById('selectedGraph');
  const graphTypeInput = document.getElementById('graphTypeInput');

  dropdownSection.style.display = 'block';
  selectedGraph.textContent = "Selected: " + graphName;
  graphTypeInput.value = graphName;
}
