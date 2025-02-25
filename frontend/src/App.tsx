import Chat from "./comp/Chat"
import { SocketProvider } from "./provider/SocketContext"

const App = () => {
  return (
    <>
      <SocketProvider>
        <Chat />
      </SocketProvider>
    </>
  )
}

export default App
