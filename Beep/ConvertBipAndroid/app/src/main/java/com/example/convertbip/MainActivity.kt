package com.example.convertbip.ui

import android.Manifest
import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.webkit.WebView
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.core.content.ContextCompat
import com.example.convertbip.bluetooth.GerenciadorBluetooth
import com.example.convertbip.qrcode.ManipuladorQRCode
import com.example.convertbip.vibration.GerenciadorVibracao
import com.example.convertbip.vlibras.GerenciadorVLibras

// Certifique-se de que você criou esses arquivos no seu projeto.
import com.example.convertbip.ui.screens.SettingsScreen
import com.example.convertbip.ui.screens.MainScreen

class MainActivity : ComponentActivity() {
    private lateinit var gerenciadorBluetooth: GerenciadorBluetooth
    private lateinit var gerenciadorVibracao: GerenciadorVibracao
    private lateinit var manipuladorQRCode: ManipuladorQRCode
    private lateinit var gerenciadorVLibras: GerenciadorVLibras
    private lateinit var webViewVLibras: WebView
    private val CODIGO_REQUISICAO_QR_CODE = 1001

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Instanciar gerenciadores
        gerenciadorBluetooth = GerenciadorBluetooth(this)
        gerenciadorVibracao = GerenciadorVibracao(this)
        manipuladorQRCode = ManipuladorQRCode(this)
        gerenciadorVLibras = GerenciadorVLibras(this)

        // Configurar a WebView do VLibras
        webViewVLibras = WebView(this)
        gerenciadorVLibras.configurarWebView(webViewVLibras)

        // Definir o conteúdo da UI
        setContent {
            var mostrarConfiguracoes by remember { mutableStateOf(false) }

            if (mostrarConfiguracoes) {
                SettingsScreen(
                    onBackClick = { mostrarConfiguracoes = false },
                    onVibrationChange = { duracao, intensidade ->
                        gerenciadorVibracao.vibrar(duracao, intensidade)
                    },
                    onQrCodeClick = { manipuladorQRCode.abrirLeitorQRCode(this, CODIGO_REQUISICAO_QR_CODE) }
                )
            } else {
                MainScreen(
                    onSettingsClick = { mostrarConfiguracoes = true },
                    checkBluetoothState = { verificarEstadoBluetooth() }
                )
            }
        }

        verificarEPedirPermissoes()
    }

    // Função para verificar e solicitar permissões
    private fun verificarEPedirPermissoes() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.BLUETOOTH_CONNECT) != PackageManager.PERMISSION_GRANTED ||
            ContextCompat.checkSelfPermission(this, Manifest.permission.BLUETOOTH_SCAN) != PackageManager.PERMISSION_GRANTED) {

            solicitacaoPermissaoBluetooth.launch(
                arrayOf(
                    Manifest.permission.BLUETOOTH_CONNECT,
                    Manifest.permission.BLUETOOTH_SCAN
                )
            )
        } else {
            verificarEstadoBluetooth()
        }
    }

    private val solicitacaoPermissaoBluetooth = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { permissoes ->
        if (permissoes[Manifest.permission.BLUETOOTH_CONNECT] == true &&
            permissoes[Manifest.permission.BLUETOOTH_SCAN] == true) {
            verificarEstadoBluetooth()
        } else {
            Toast.makeText(this, "Permissões de Bluetooth necessárias", Toast.LENGTH_SHORT).show()
        }
    }

    private fun verificarEstadoBluetooth(): String {
        // Certifique-se de que a função verificarEstadoBluetooth está corretamente implementada em GerenciadorBluetooth
        return gerenciadorBluetooth.verificarEstadoBluetooth()
    }

    // Captura o resultado do QR Code
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        if (requestCode == CODIGO_REQUISICAO_QR_CODE && resultCode == Activity.RESULT_OK) {
            val dadosQRCode = data?.getStringExtra("qr_code_data")
            // Processar os dados do QR Code (por exemplo, conectar ao servidor usando o token ou IP)
        }
    }
}
