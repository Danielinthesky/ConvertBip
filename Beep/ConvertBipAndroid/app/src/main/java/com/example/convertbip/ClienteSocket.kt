import java.io.OutputStream
import java.io.PrintWriter
import java.net.Socket
import java.util.concurrent.Executors

class ClienteSocket(private val ipDoPC: String, private val porta: Int) {

    fun enviarMensagem(mensagem: String) {
        val executor = Executors.newSingleThreadExecutor()
        executor.execute {
            try {
                val socket = Socket(ipDoPC, porta)
                val saida: PrintWriter = PrintWriter(socket.getOutputStream(), true)
                saida.println(mensagem)
                println("Mensagem enviada para o servidor: $mensagem")
                socket.close()
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
}
