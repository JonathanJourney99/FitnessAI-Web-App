// Function to increase the value
function increaseValue(inputId) {
  let input = document.getElementById(inputId);
  let currentValue = parseFloat(input.value);
  let step = parseFloat(input.step);
  let max = parseFloat(input.max);
  if (currentValue < max) {
    input.value = (currentValue + step).toFixed(2);
  }
}

// Function to decrease the value
function decreaseValue(inputId) {
  let input = document.getElementById(inputId);
  let currentValue = parseFloat(input.value);
  let step = parseFloat(input.step);
  let min = parseFloat(input.min);
  if (currentValue > min) {
    input.value = (currentValue - step).toFixed(2);
  }
}
