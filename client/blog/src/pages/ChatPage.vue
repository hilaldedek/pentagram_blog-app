<template>
  <div>
    <NavbarComponent />
    <button @click="leaveRoom" class="leaveButton">Leave Room</button>
    <div class="messages" ref="messageContainer">
      <ul class="ul">
        <div
          v-for="(message, index) in messagesData"
          :key="index"
          class="tagsInput"
        >
          <h2>{{ message }}</h2>
        </div>
      </ul>
    </div>
    <div class="main">
      <div class="search">
        <input placeholder="Message..." type="text" v-model="newMessage" />
        <button type="submit" @click="sendMessage(newMessage)">Send</button>
      </div>
    </div>
  </div>
</template>

<script>
import { io } from "socket.io-client";
import NavbarComponent from "@/components/NavbarComponent.vue";

export default {
  name: "ChatPage",
  components: { NavbarComponent },
  data() {
    return {
      messagesData: null,
      newMessage: "",
      socket: null,
      currentUsername: localStorage.getItem("username"),
      username: this.$route.params.username,
      nameList: [],
      sortedNameList: [],
    };
  },
  created() {
    this.initSocket();
  },
  mounted() {
    this.getMessages();
  },
  methods: {
    async getMessages() {
      const getToken = localStorage.getItem("access_token");
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/chat/${this.username}`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${getToken}`,
              "Content-Type": "application/json",
              "Access-Control-Allow-Origin": "*",
            },
          }
        );
        if (!response.ok) {
          throw new Error("Veri alınamadı");
        }
        const data = await response.json();
        this.messagesData = data.messageHistory.messages;
        console.log("messagedata: ", this.messagesData);
      } catch (error) {
        console.error("Veri alınamadı:", error.message);
      }
    },
    initSocket() {
      const nameList = [this.username, this.currentUsername];
      const sortedNameList = nameList.sort();
      const roomName = `${sortedNameList[0]}_${sortedNameList[1]}_rooms`;
      console.log(roomName);
      this.socket = io.connect("http://localhost:5000");
      this.socket.on("connect", () => {
        this.socket.emit("first_connect", "a user has connected");
      });
      this.socket.on("connect_error", (err) => {
        console.log("Connect error:", err);
      });
      const data = {
        username: this.username,
        currentUser: this.currentUsername,
        room: roomName,
      };
      this.socket.emit("join", data, (data) => {
        console.log("Join response:", data);
      });
      this.socket.on("response", (data) => {
        this.addMessageToContainer(data);
      });
    },
    leaveRoom() {
      console.log("leave room");
      const nameList = [this.username, this.currentUsername];
      const sortedNameList = nameList.sort();
      const roomName = `${sortedNameList[0]}_${sortedNameList[1]}_rooms`;
      this.socket.emit("leave", {
        currentUsername: this.currentUsername,
        room: roomName,
      });
    },
    sendMessage(message) {
      const nameList = [this.username, this.currentUsername];
      const sortedNameList = nameList.sort();
      const roomName = `${sortedNameList[0]}_${sortedNameList[1]}_rooms`;
      const data = {
        currentUsername: this.currentUsername,
        username: this.username,
        message: message,
        room: roomName,
      };
      this.socket.emit("new_message", data);
      this.newMessage = "";
      this.socket.on("notification", (data) => {
        this.message = data;
      });
    },
    addMessageToContainer(data) {
      console.log(data);
      const messageContainer = this.$refs.messageContainer;
      const messageContent = document.createElement("h2");
      messageContent.textContent = `${data.username}: ${data.message}`;
      if (data.username === this.currentUsername) {
        messageContent.classList.add("currentUser");
      } else {
        messageContent.classList.add("user");
      }
      messageContainer.appendChild(messageContent);
      messageContainer.scrollTop = messageContainer.scrollHeight;
    },
  },
};
</script>

<style src="../styles/chat.css" scoped></style>
