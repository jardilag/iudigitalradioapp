package com.example.iudigitalradioapp.audio

import com.example.iudigitalradioapp.ui.RadioAction
import com.example.iudigitalradioapp.ui.RadioReducer
import com.example.iudigitalradioapp.ui.RadioUiState

/**
 * Rol responsable en la simulación: Jorge Echavarría.
 *
 * Traduce las acciones puras de la interfaz en órdenes para [RadioPlayer] y
 * después delega la actualización visual a [RadioReducer]. Esta separación
 * permite comprobar el comportamiento con un reproductor falso en pruebas.
 */
class AudioActionHandler(
    private val radioPlayer: RadioPlayer
) {

    fun handle(
        state: RadioUiState,
        action: RadioAction
    ): RadioUiState {
        return when (action) {
            RadioAction.Play -> playSelectedStation(state)

            RadioAction.Pause -> {
                radioPlayer.pause()
                RadioReducer.reduce(state, action)
            }

            RadioAction.ToggleMute -> {
                radioPlayer.setMuted(!state.isMuted)
                RadioReducer.reduce(state, action)
            }

            is RadioAction.SelectStation -> {
                radioPlayer.pause()
                RadioReducer.reduce(state, action)
            }

            RadioAction.OpenCamera,
            is RadioAction.PhotoCaptured -> RadioReducer.reduce(state, action)
        }
    }

    private fun playSelectedStation(state: RadioUiState): RadioUiState {
        val streamUrl = state.selectedStation?.streamUrl
            ?.takeIf(String::isNotBlank)
            ?: return state

        radioPlayer.play(streamUrl)
        return RadioReducer.reduce(state, RadioAction.Play)
    }
}
