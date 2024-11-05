package com.example.convertbip.vlibras

import android.content.Context
import android.webkit.WebView
import android.webkit.WebViewClient

class GerenciadorVLibras(private val contexto: Context) {
    fun configurarWebView(webView: WebView) {
        webView.webViewClient = WebViewClient()
        webView.settings.javaScriptEnabled = true
        webView.loadUrl("https://vlibras.gov.br/app")
    }

    fun enviarTextoParaVLibras(webView: WebView, texto: String) {
        webView.evaluateJavascript("document.body.innerText = '$texto';", null)
    }
}
