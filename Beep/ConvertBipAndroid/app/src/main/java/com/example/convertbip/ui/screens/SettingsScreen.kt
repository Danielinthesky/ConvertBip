package com.example.convertbip.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.launch
import androidx.datastore.preferences.core.floatPreferencesKey
import androidx.datastore.preferences.core.edit
import com.example.convertbip.dataStore
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(
    onBackClick: () -> Unit,
    onVibrationChange: (Long, Int) -> Unit,
    onQrCodeClick: () -> Unit
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()

    var vibrationStrength by remember { mutableFloatStateOf(50f) }
    var showDialog by remember { mutableStateOf(false) }
    val savedVibrationStrength: Flow<Float> = context.dataStore.data
        .map { preferences -> preferences[floatPreferencesKey("vibration_strength")] ?: 50f }

    LaunchedEffect(Unit) {
        savedVibrationStrength.collect { savedValue -> vibrationStrength = savedValue }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(text = "Configurações") },
                navigationIcon = {
                    IconButton(onClick = onBackClick) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Voltar")
                    }
                }
            )
        },
        content = { paddingValues ->
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues)
                    .padding(16.dp),
                verticalArrangement = Arrangement.Center,
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text(text = "Ajustar Intensidade da Vibração")
                Slider(
                    value = vibrationStrength,
                    onValueChange = { strength ->
                        vibrationStrength = strength
                        onVibrationChange(1000, (strength / 100 * 255).toInt())
                    },
                    valueRange = 0f..100f
                )
                Text(text = "Intensidade: ${vibrationStrength.toInt()}%")

                Spacer(modifier = Modifier.height(16.dp))

                Button(onClick = { onQrCodeClick() }) {
                    Text(text = "Conexão por QR Code")
                }

                Spacer(modifier = Modifier.height(16.dp))

                Button(onClick = {
                    scope.launch {
                        context.dataStore.edit { preferences ->
                            preferences[floatPreferencesKey("vibration_strength")] = vibrationStrength
                        }
                    }
                    onBackClick()
                }) {
                    Text(text = "Salvar e Voltar")
                }

                Spacer(modifier = Modifier.height(16.dp))

                Button(onClick = { showDialog = true }) {
                    Text(text = "Ajuda")
                }

                if (showDialog) {
                    ShowHelpDialog(onDismiss = { showDialog = false })
                }
            }
        }
    )
}

@Composable
fun ShowHelpDialog(onDismiss: () -> Unit) {
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Ajuda (FAQ)") },
        text = {
            Column {
                Text("1. Como conectar o ConvertBip?")
                Text("Conecte o seu dispositivo via Bluetooth e o aplicativo automaticamente detectará o dispositivo.")
                Spacer(modifier = Modifier.height(8.dp))
                Text("2. Quais são os tipos de alertas vibratórios?")
                Text("Quando o aplicativo detecta problemas na RAM ou vídeo, ele envia padrões vibratórios para o seu dispositivo.")
                Spacer(modifier = Modifier.height(8.dp))
                Text("3. Como ajustar a intensidade da vibração?")
                Text("Vá até as configurações e ajuste a intensidade da vibração utilizando o controle deslizante.")
            }
        },
        confirmButton = {
            TextButton(onClick = onDismiss) {
                Text("Fechar")
            }
        }
    )
}
