package com.example.iudigitalradioapp.ui

import android.graphics.Bitmap
import com.example.iudigitalradioapp.model.Station

/**
 * Rol responsable en la simulación: Luisa Gomez.
 *
 * Reúne los datos observables de la pantalla. Cada cambio produce una copia
 * inmutable para que Compose pueda representar el nuevo estado.
 */
data class RadioUiState(
    val stations: List<Station> = emptyList(),
    val selectedStationId: String? = null,
    val isPlaying: Boolean = false,
    val isMuted: Boolean = false,
    val capturedPhoto: Bitmap? = null
) {
    /** Devuelve la emisora completa que corresponde al identificador activo. */
    val selectedStation: Station?
        get() = stations.firstOrNull { station ->
            station.id == selectedStationId
        }
}
