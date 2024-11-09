package com.example.convertbip.vibration

import android.content.Context
import android.os.Build
import android.os.VibrationEffect
import android.os.Vibrator
import android.util.Log


class GerenciadorVibracao(private val contexto: Context) {
    fun vibrar(duracao: Long, intensidade: Int = 255) {
        val vibrador = contexto.getSystemService(Context.VIBRATOR_SERVICE) as Vibrator
        if (!vibrador.hasVibrator()) {
            Log.d("GerenciadorVibracao", "Dispositivo não suporta vibração.")
            return
        }

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val efeito = VibrationEffect.createOneShot(duracao, intensidade)
            vibrador.vibrate(efeito)
        } else {
            vibrador.vibrate(duracao)
        }
    }
}
