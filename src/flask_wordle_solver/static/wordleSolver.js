const updateButton = document.getElementById("updateButton");

// update button color on form change
function clickMe(action) {
  if (action == "on") {
    updateButton.classList.add("click-me");
  } else {
    updateButton.classList.remove("click-me");
  }
}

// auto tab between tiles
function autoTab(current) {
  let val = current.value;
  let next = current.nextElementSibling;
  // move to next input if valid character is entered
  if (val.toUpperCase() != val.toLowerCase() || val == " ") {
    // check to see if letter is in puzzle
    if (current.className.includes("invalid")) {
      let corrects = Array.from(document.getElementsByClassName("correct"));
      let valids = Array.from(document.getElementsByClassName("valid"));
      let alreadyPlayed = corrects.concat(valids);
      if (alreadyPlayed.filter((i) => i.value.toLowerCase() == val).length > 0) {
        alert(`${val.toUpperCase()} is already valid in your puzzle!`);
        current.value = "";
        return;
      }
    }
    // remove any space entered
    if (val == " ") {
      current.value = "";
    }
    // stop if at end of tiles
    if (next != null) {
      next.focus();
    }
  }
  // remove invalid characters
  else {
    current.value = "";
  }
}

// reset all tiles in current section
function resetTiles(current, target) {
  let inputs = Array.from(document.getElementsByClassName(target));
  inputs.forEach((i) => (i.value = ""));
}
