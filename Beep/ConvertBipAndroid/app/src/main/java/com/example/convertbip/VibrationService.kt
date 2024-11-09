package com.example.convertbip

import android.app.Service
import android.content.Context
import android.content.Intent
import android.os.IBinder
import com.example.convertbip.vibration.GerenciadorVibracao
import android.util.Log

class VibrationService : Service() {

    private lateinit var gerenciadorVibracao: GerenciadorVibracao

    /*
    override fun onCreate() {
        super.onCreate()
        gerenciadorVibracao = GerenciadorVibracao(this)
        Log.d("VibrationService", "VibrationService iniciado")
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        val duration = intent?.getLongExtra("duration", 500) ?: 500
        val intensity = intent?.getIntExtra("intensity", 255) ?: 255

        Log.d("VibrationService", "Comando de vibração recebido: duração = $duration, intensidade = $intensity")

        // Iniciar a vibração
        gerenciadorVibracao.vibrar(duration, intensity)

        // Parar o serviço após a vibração
        stopSelf()
        return START_NOT_STICKY
    }

*/



    override fun onBind(intent: Intent?): IBinder? {
        return null
    }
}
