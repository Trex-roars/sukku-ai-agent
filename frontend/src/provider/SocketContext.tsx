import { createContext, useContext, useEffect, useState } from "react";

const SocketContext = createContext<WebSocket | null>(null);

export const SocketProvider = ({ children }: { children: React.ReactNode }) => {
    const [socket, setSocket] = useState<WebSocket | null>(null);

    useEffect(() => {
        const ws = new WebSocket("ws://localhost:5000");

        ws.onopen = () => console.log("Connected to WebSocket ✅");
        ws.onclose = () => console.log("Disconnected from WebSocket ❌");
        ws.onerror = (error) => console.error("WebSocket Error:", error);

        setSocket(ws);

        return () => {
            ws.close();
        };
    }, []);

    return <SocketContext.Provider value={socket}>{children}</SocketContext.Provider>;
};

export const useSocket = () => {
    return useContext(SocketContext);
};
