package com.example.iudigitalradioapp.ui

/**
 * Rol responsable en la simulación: Luisa Gomez.
 *
 * Transforma un estado y una acción en un nuevo estado inmutable. No abre la
 * cámara, no reproduce audio y no ejecuta vibración; esos efectos se conectan
 * posteriormente desde RadioRoute.
 */
object RadioReducer {

    fun reduce(
        state: RadioUiState,
        action: RadioAction
    ): RadioUiState {
        return when (action) {
            RadioAction.Play -> {
                if (state.selectedStation == null) {
                    state
                } else {
                    state.copy(isPlaying = true)
                }
            }

            RadioAction.Pause -> state.copy(isPlaying = false)

            RadioAction.ToggleMute -> state.copy(isMuted = !state.isMuted)

            RadioAction.OpenCamera -> state

            is RadioAction.SelectStation -> {
                val stationExists = state.stations.any { station ->
                    station.id == action.stationId
                }

                if (stationExists) {
                    // La reproducción se detiene hasta que integración cargue la nueva fuente.
                    state.copy(
                        selectedStationId = action.stationId,
                        isPlaying = false
                    )
                } else {
                    state
                }
            }

            is RadioAction.PhotoCaptured -> {
                state.copy(capturedPhoto = action.bitmap)
            }
        }
    }
}
