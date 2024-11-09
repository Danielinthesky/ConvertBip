package com.example.convertbip

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.util.Log
import com.example.convertbip.vibration.GerenciadorVibracao

class RecebedorComandoUSB : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        val action = intent.action
        if (action == "com.example.convertbip.VIBRATE") {
            val duration = intent.getLongExtra("duration", 500)
            val intensity = intent.getIntExtra("intensity", 255)

            // Log para verificar se o broadcast é recebido
            Log.d("RecebedorComandoUSB", "Comando de vibração recebido: duração = $duration, intensidade = $intensity")

            // Usa o contexto da aplicação para criar o GerenciadorVibracao
            val gerenciadorVibracao = GerenciadorVibracao(context.applicationContext)
            gerenciadorVibracao.vibrar(duration, intensity)
        }
    }
}
