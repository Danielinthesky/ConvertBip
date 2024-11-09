package com.example.convertbip.network

import android.util.Log
import java.io.BufferedReader
import java.io.InputStreamReader
import java.net.ServerSocket
import java.net.Socket

class ServidorSocket(private val onCommandReceived: (String) -> Unit) {
    private var serverSocket: ServerSocket? = null
    private val port = 12345 // Porta do servidor Android

    // Iniciar o servidor em uma nova thread
    fun startServer() {
        Thread {
            try {
                serverSocket = ServerSocket(port)
                Log.d("ServidorSocket", "Servidor iniciado na porta $port")

                // Loop para escutar conexões
                while (true) {
                    val clientSocket: Socket = serverSocket!!.accept()
                    Log.d("ServidorSocket", "Cliente conectado: ${clientSocket.inetAddress.hostAddress}")

                    // Ler o comando enviado pelo PC
                    val reader = BufferedReader(InputStreamReader(clientSocket.getInputStream()))
                    val command = reader.readLine()
                    if (command != null) {
                        Log.d("ServidorSocket", "Comando recebido: $command")
                        onCommandReceived(command) // Chama a função para processar o comando
                    }
                    clientSocket.close()
                }
            } catch (e: Exception) {
                e.printStackTrace()
                Log.e("ServidorSocket", "Erro ao iniciar servidor: ${e.message}")
            }
        }.start()
    }

    // Parar o servidor
    fun stopServer() {
        try {
            serverSocket?.close()
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
}
