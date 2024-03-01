document.querySelector("#token-submit").onclick = function (e) {
  const token = document.getElementById("token-input").value;

  url = "ws://" + window.location.host + "/ws/chatrooms/" + `?token=${token}`;

  const chatSocket = new WebSocket(url);

  chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    // If this is the first (initial) message
    if (data.initial) {
      // Set User' name on top of the page
      const greeting = document.createElement("h1");
      greeting.id = "greeting-header";
      greeting.innerText = `Hello ${data.user}`;
      greeting.style.color = "#FF9472";
      document.body.appendChild(greeting);

      // build the chatroom containers
      for (room of data.chatrooms) {
        const roomContainer = document.createElement("div");
        roomContainer.id = room.name;
        roomContainer.className = "roomContainer";
        document.body.appendChild(roomContainer);

        const title = document.createElement("h3");
        title.innerText = room.name;
        roomContainer.appendChild(title);

        const log = document.createElement("textarea");
        log.className = "log";
        log.cols = 50;
        roomContainer.appendChild(log);
        roomContainer.appendChild(document.createElement("br"));

        // Populate log window with history of messages
        for (message of room.messages) {
          log.value += `${message.sender_name}: ${message.content} ${message.date_time}\n`;
        }

        const messageInput = document.createElement("input");
        messageInput.className = "messageInput";
        roomContainer.appendChild(messageInput);

        const messageLabel = document.createElement("label");
        messageLabel.innerText = "message: ";
        roomContainer.insertBefore(messageLabel, messageInput);

        const fileInput = document.createElement("input");
        fileInput.type = "file";
        fileInput.className = "fileInput";
        roomContainer.appendChild(fileInput);

        const sendButton = document.createElement("button");
        sendButton.className = "sendButton";
        sendButton.innerText = "Send";
        roomContainer.appendChild(sendButton);
        roomContainer.appendChild(document.createElement("br"));

        // Ability to kick out members (if admin)
        if (room.is_admin) {
          const kickedUserIdInput = document.createElement("input");
          kickedUserIdInput.className = "kickedUserIdInput";
          kickedUserIdInput.size = 3;
          roomContainer.appendChild(kickedUserIdInput);

          const kickedUserIdLabel = document.createElement("label");
          kickedUserIdLabel.innerText = "kicked user id: ";
          roomContainer.insertBefore(kickedUserIdLabel, kickedUserIdInput);

          const kickButton = document.createElement("button");
          kickButton.className = "kickButton";
          kickButton.innerText = "Kick Out";
          roomContainer.appendChild(kickButton);
          roomContainer.appendChild(document.createElement("br"));
        }

        const leaveButton = document.createElement("button");
        leaveButton.className = "leaveButton";
        leaveButton.innerText = "Leave";
        roomContainer.appendChild(leaveButton);
        roomContainer.appendChild(document.createElement("br"));
        roomContainer.appendChild(document.createElement("hr"));
        roomContainer.appendChild(document.createElement("br"));
      }

      // Sending messages to websocket server
      // Set event for clicking "send" button
      document.querySelectorAll(".sendButton").forEach(function (btn) {
        btn.addEventListener("click", function (e) {
          const roomName = this.parentNode.id;
          const message = this.parentNode.querySelector(".messageInput").value;
          const fileInput = this.parentNode.querySelector(".fileInput");

          // Is there a file included ?
          const file = fileInput.files[0];
          if (file) {
            const reader = new FileReader();

            reader.onload = function (event) {
              const binaryString = event.target.result;
              // Convert binary to Base64 string
              file_data = btoa(binaryString);
              chatSocket.send(
                JSON.stringify({
                  type: "chat.message",
                  room: roomName,
                  content: message,
                  file_name: file.name,
                  file_data: file_data,
                })
              );
              // Make file input empty after sending
              fileInput.value = ''
            };

            reader.readAsBinaryString(file);
          } else {
            chatSocket.send(
              JSON.stringify({
                type: "chat.message",
                room: roomName,
                content: message,
                file_name: "",
                file_data: "",
              })
            );
          }

          // Clear the message input field
          this.parentNode.querySelector(".messageInput").value = "";
        });
      });

      // Leaving a chatroom
      // Set event for clicking "leave" button
      document.querySelectorAll(".leaveButton").forEach(function (btn) {
        btn.addEventListener("click", function (e) {
          const roomName = this.parentNode.id;

          chatSocket.send(
            JSON.stringify({
              room_name: roomName,
              type: "chat.leave",
            })
          );
        });
      });

      // Kicking a user out of chatroom
      // Set event for clicking "kick out" button
      document.querySelectorAll(".kickButton").forEach(function (btn) {
        btn.addEventListener("click", function (e) {
          const roomName = this.parentNode.id;
          const kickedUserId =
            this.parentNode.querySelector(".kickedUserIdInput").value;

          chatSocket.send(
            JSON.stringify({
              room_name: roomName,
              type: "chat.kick_out",
              user_id: kickedUserId,
            })
          );
        });
      });

      // If this is a (Reload) message
    } else if (data.reload) {
      window.location.reload();

      // If Receive a normal message
    } else {
      const roomName = data.room;

      // Prepare the message and sender to be shown
      let text;
      if (data.notify) {
        text = `** ${data.content} **\n`;
      }
      // Show the file
      // else if (data.file) {
      //   text = `${data.sender_name}: ${data.content} ${data.date_time} ${window.location.origin}${data.file}\n`;
      // }
      else {
        text = `${data.sender_name}: ${data.content} ${data.date_time}\n`;
      }
      // Show the message in the related log window
      document.querySelector(`#${roomName} textarea`).value += text;
    }
  };

  chatSocket.onclose = function (e) {
    console.error("Chat socket closed unexpectedly");
  };
};
