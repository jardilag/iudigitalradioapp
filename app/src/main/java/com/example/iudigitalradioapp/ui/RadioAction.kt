package com.example.iudigitalradioapp.ui

import android.graphics.Bitmap

/**
 * Rol responsable inicial en la simulación: Luisa Gomez.
 *
 * Enumera las acciones que la pantalla puede enviar al coordinador. Los
 * módulos de UI, cámara y audio consumen este contrato sin duplicar eventos.
 */
sealed interface RadioAction {

    data object Play : RadioAction

    data object Pause : RadioAction

    data object ToggleMute : RadioAction

    data object OpenCamera : RadioAction

    data class SelectStation(
        val stationId: String
    ) : RadioAction

    data class PhotoCaptured(
        val bitmap: Bitmap
    ) : RadioAction
}
