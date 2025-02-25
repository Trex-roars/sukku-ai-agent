import cors from "cors";
import express from "express";
import { createServer } from "http";
import { WebSocket, WebSocketServer } from "ws";

const app = express();
const server = createServer(app);
const wss = new WebSocketServer({ server });

app.use(cors({ origin: "http://localhost:5173", credentials: true }));

// WebSocket server logic
wss.on("connection", (ws: WebSocket) => {
    console.log("New client connected");

    ws.on("message", (data) => {
        const message = JSON.parse(data.toString());
        console.log("Received:", message);

        wss.clients.forEach((client) => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(JSON.stringify(message));
            }
        });
    });

    ws.on("close", () => {
        console.log("Client disconnected");
    });
});

// Start the server
server.listen(5000, () => console.log("WebSocket server running on port 5000"));
