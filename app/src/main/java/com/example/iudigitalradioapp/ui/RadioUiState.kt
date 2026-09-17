package com.example.iudigitalradioapp.ui

import android.graphics.Bitmap
import com.example.iudigitalradioapp.model.Station

data class RadioUiState(
    val stations: List<Station> = emptyList(),
    val selectedStationId: String? = null,
    val isPlaying: Boolean = false,
    val isMuted: Boolean = false,
    val capturedPhoto: Bitmap? = null
) {
    val selectedStation: Station?
        get() = stations.firstOrNull { station ->
            station.id == selectedStationId
        }
}