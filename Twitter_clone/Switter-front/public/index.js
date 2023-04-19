
// set length cap on posting area on /feed.

var maxLength = 100; // Change this to set the maximum length

// Get the textarea element
var textarea = document.getElementById("posttweet");

// Add an event listener to the textarea to detect changes
textarea.addEventListener("input", function() {
  // Get the current text and check its length
  var text = textarea.value;
  if (text.length > maxLength) {
    // If the text is too long, truncate it
    textarea.value = text.substr(0, maxLength);
  }
});
