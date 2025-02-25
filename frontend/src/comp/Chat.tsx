import { useEffect, useState } from "react";
import { useSocket } from "../provider/SocketContext";

export default function Chat() {
    const socket = useSocket();
    const [messages, setMessages] = useState<{ id: number; text: string }[]>([]);
    const [message, setMessage] = useState("");

    useEffect(() => {
        if (!socket) return;

        socket.onmessage = (event) => {
            const receivedMessage = JSON.parse(event.data);
            setMessages((prev) => [...prev, receivedMessage]);
        };

        return () => {
            socket.onmessage = null;
        };
    }, [socket]);

    const sendMessage = () => {
        if (message.trim() && socket) {
            const newMessage = { id: Date.now(), text: message };
            socket.send(JSON.stringify(newMessage));
            setMessage("");
        }
    };

    return (
        <div>
            <h2>WebSocket Chat</h2>
            <div>
                {messages.map((msg) => (
                    <p key={msg.id}>{msg.text}</p>
                ))}
            </div>
            <input
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Type a message..."
            />
            <button onClick={sendMessage}>Send</button>
        </div>
    );
}
