package com.example.convertbip.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.google.accompanist.swiperefresh.SwipeRefresh
import com.google.accompanist.swiperefresh.rememberSwipeRefreshState
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Settings


@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainScreen(
    onSettingsClick: () -> Unit,
    checkBluetoothState: () -> String
) {
    var bluetoothStatus by remember { mutableStateOf(checkBluetoothState()) }
    var isRefreshing by remember { mutableStateOf(false) }
    val scope = rememberCoroutineScope()

    fun updateBluetoothStatus() {
        scope.launch {
            isRefreshing = true
            bluetoothStatus = checkBluetoothState()
            isRefreshing = false
        }
    }

    LaunchedEffect(Unit) {
        while (true) {
            updateBluetoothStatus()
            delay(30000)
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(text = "ConvertBip") },
                actions = {
                    IconButton(onClick = onSettingsClick) {
                        Icon(Icons.Default.Settings, contentDescription = "Configurações")
                    }
                }
            )
        },
        content = { paddingValues ->
            SwipeRefresh(
                state = rememberSwipeRefreshState(isRefreshing),
                onRefresh = { scope.launch { updateBluetoothStatus() } }
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(paddingValues)
                        .padding(16.dp),
                    verticalArrangement = Arrangement.Center,
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(text = bluetoothStatus)
                }
            }
        }
    )
}
