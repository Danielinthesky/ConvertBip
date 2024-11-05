package com.example.convertbip.bluetooth
import android.app.Activity
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothSocket
import android.content.Context
import android.widget.Toast
import java.io.InputStream
import java.io.OutputStream
import java.util.*

class GerenciadorBluetooth(private val contexto: Context) {
    private val adaptadorBluetooth: BluetoothAdapter? = BluetoothAdapter.getDefaultAdapter()
    private var socketBluetooth: BluetoothSocket? = null
    private var entradaStream: InputStream? = null
    private var saidaStream: OutputStream? = null

    fun conectarAoDispositivo(dispositivo: BluetoothDevice) {
        try {
            val uuid = UUID.randomUUID()
            socketBluetooth = dispositivo.createRfcommSocketToServiceRecord(uuid)
            socketBluetooth?.connect()

            entradaStream = socketBluetooth?.inputStream
            saidaStream = socketBluetooth?.outputStream

            Toast.makeText(contexto, "Conectado ao dispositivo ${dispositivo.name}", Toast.LENGTH_SHORT).show()

            escutarComandos()
        } catch (e: Exception) {
            e.printStackTrace()
            Toast.makeText(contexto, "Erro ao conectar ao dispositivo Bluetooth", Toast.LENGTH_SHORT).show()
        }
    }

    private fun escutarComandos() {
        Thread {
            try {
                val buffer = ByteArray(1024)
                var bytes: Int

                while (socketBluetooth != null && socketBluetooth!!.isConnected) {
                    bytes = entradaStream?.read(buffer) ?: 0
                    val comando = String(buffer, 0, bytes)

                    (contexto as Activity).runOnUiThread {
                        processarComandoBluetooth(comando.trim())
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }.start()
    }

    private fun processarComandoBluetooth(comando: String) {
        when (comando) {
            "vibrate_short" -> {
                // Chamar função de vibração curta
            }
            "vibrate_long" -> {
                // Chamar função de vibração longa
            }
            else -> {
                Toast.makeText(contexto, "Comando desconhecido: $comando", Toast.LENGTH_SHORT).show()
            }
        }
    }
}
