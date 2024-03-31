function openCategory(evt, category) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(category).style.display = "block";
  evt.currentTarget.className += " active";
}

// Function to initialize video header
function initializeVideoHeader() {
  var videoPlayer = document.querySelector('.video-player');
  var videoControlsBox = document.querySelector('.video-controls-box');
  var videoPlay = document.getElementById('video-play');
  var videoVolume = document.getElementById('video-volume');

  // Play or pause the video
  videoPlay.addEventListener('click', function() {
    if (videoPlayer.paused) {
      videoPlayer.play();
      videoPlay.classList.remove('fa-play');
      videoPlay.classList.add('fa-pause');
    } else {
      videoPlayer.pause();
      videoPlay.classList.remove('fa-pause');
      videoPlay.classList.add('fa-play');
    }
  });

  // Mute or unmute the video
  videoVolume.addEventListener('click', function() {
    if (videoPlayer.muted) {
      videoPlayer.muted = false;
      videoVolume.classList.remove('fa-volume-off');
      videoVolume.classList.add('fa-volume-up');
    } else {
      videoPlayer.muted = true;
      videoVolume.classList.remove('fa-volume-up');
      videoVolume.classList.add('fa-volume-off');
    }
  });
}

// Initialize video header when the document is loaded
document.addEventListener('DOMContentLoaded', function() {
  initializeVideoHeader();
});


// Add event listener to the send button when clicked
document.getElementById("send-button").addEventListener("click", function() {
    sendMessage(); // Call sendMessage function
});

// Function to send a message
function sendMessage() {
    var messageInput = document.getElementById("message-input"); // Get the message input element
    var message = messageInput.value.trim(); // Get the trimmed value of the message input

    // Check if the message is not empty
    if (message !== "") {
        var chatContainer = document.getElementById("chat-container"); // Get the chat container element
        var newMessage = document.createElement("div"); // Create a new div element for the message
        newMessage.classList.add("message"); // Add the 'message' class to the new message element
        newMessage.innerHTML = `
            <div class="sender">You</div> <!-- Display sender name -->
            <div class="text">${message}</div> <!-- Display message content -->
        `; // Set the inner HTML of the new message element
        
        chatContainer.appendChild(newMessage); // Append the new message to the chat container
        messageInput.value = ""; // Clear the message input field
        chatContainer.scrollTop = chatContainer.scrollHeight; // Scroll to the bottom of the chat container to show the latest message
    }
}

