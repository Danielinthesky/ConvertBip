package com.example.convertbip.qrcode

import android.app.Activity
import android.content.Context
import android.content.Intent
import com.example.convertbip.ui.QRCodeScannerActivity

class ManipuladorQRCode(private val contexto: Context) {
    fun abrirLeitorQRCode(atividade: Activity, codigoRequisicao: Int) {
        val intent = Intent(contexto, QRCodeScannerActivity::class.java)
        atividade.startActivityForResult(intent, codigoRequisicao)
    }
}
