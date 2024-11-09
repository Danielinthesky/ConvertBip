package com.example.convertbip.network

import java.io.PrintWriter
import java.net.Socket

class ClienteSocket(private val serverIp: String, private val serverPort: Int = 12345) {
    private var socket: Socket? = null
    private var out: PrintWriter? = null

    // Conectar ao servidor
    fun connect() {
        Thread {
            try {
                socket = Socket(serverIp, serverPort)
                out = PrintWriter(socket?.getOutputStream(), true)
                println("Conectado ao servidor!")
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }.start()
    }

    // Enviar comando
    fun sendCommand(command: String) {
        out?.println(command)
        println("Comando enviado: $command")
    }

    // Desconectar do servidor
    fun disconnect() {
        try {
            socket?.close()
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
}
