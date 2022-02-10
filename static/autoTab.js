// auto tab between tiles
function autoTab(current) {
  let val = current.value;
  let next = current.nextElementSibling;
  // move to next input if valid character is entered
  if (val.toUpperCase() != val.toLowerCase() || val == " ") {
    if (val == " ") {
      current.value = "";
    }
    next.focus();
  }
  // remove invalid characters
  else {
    current.value = "";
  }
}
