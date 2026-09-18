package com.example.iudigitalradioapp.ui

import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue

/**
 * Rol responsable en la simulación: Juan Pablo Gonzalez.
 *
 * Mantiene estado únicamente para demostrar y revisar la interfaz. Esta
 * función no reproduce audio, no abre la cámara y no activa vibración. Juan
 * Ardila conectará esos efectos posteriormente desde RadioRoute.
 */
@Composable
fun RadioScreenDemo() {
    var state by remember {
        mutableStateOf(createInitialRadioUiState())
    }

    RadioScreen(
        state = state,
        onAction = { action ->
            state = RadioReducer.reduce(state, action)
        }
    )
}
