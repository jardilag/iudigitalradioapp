package com.example.iudigitalradioapp.ui

import com.example.iudigitalradioapp.model.Station
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

/** Pruebas del módulo asignado al rol simulado de Luisa Gomez. */
class RadioReducerTest {

    private val stations = listOf(
        Station("station-1", "Emisora 1", "Descripción 1", ""),
        Station("station-2", "Emisora 2", "Descripción 2", "")
    )

    private val initialState = createInitialRadioUiState(stations)

    @Test
    fun initialStateSelectsFirstStation() {
        assertEquals("station-1", initialState.selectedStationId)
        assertEquals("Emisora 1", initialState.selectedStation?.name)
    }

    @Test
    fun emptyCatalogHasNoSelection() {
        val state = createInitialRadioUiState(emptyList())

        assertNull(state.selectedStationId)
        assertNull(state.selectedStation)
    }

    @Test
    fun selectStationChangesSelectionAndStopsPlayback() {
        val playingState = initialState.copy(isPlaying = true)

        val result = RadioReducer.reduce(
            state = playingState,
            action = RadioAction.SelectStation("station-2")
        )

        assertEquals("station-2", result.selectedStationId)
        assertEquals("Emisora 2", result.selectedStation?.name)
        assertFalse(result.isPlaying)
    }

    @Test
    fun selectUnknownStationKeepsCurrentState() {
        val result = RadioReducer.reduce(
            state = initialState,
            action = RadioAction.SelectStation("unknown")
        )

        assertEquals(initialState, result)
    }

    @Test
    fun playStartsWhenAStationIsSelected() {
        val result = RadioReducer.reduce(initialState, RadioAction.Play)

        assertTrue(result.isPlaying)
    }

    @Test
    fun playDoesNothingWithoutASelectedStation() {
        val stateWithoutSelection = RadioUiState(stations = stations)

        val result = RadioReducer.reduce(stateWithoutSelection, RadioAction.Play)

        assertFalse(result.isPlaying)
    }

    @Test
    fun pauseStopsPlayback() {
        val playingState = initialState.copy(isPlaying = true)

        val result = RadioReducer.reduce(playingState, RadioAction.Pause)

        assertFalse(result.isPlaying)
    }

    @Test
    fun toggleMuteInvertsMutedState() {
        val mutedState = RadioReducer.reduce(initialState, RadioAction.ToggleMute)
        val unmutedState = RadioReducer.reduce(mutedState, RadioAction.ToggleMute)

        assertTrue(mutedState.isMuted)
        assertFalse(unmutedState.isMuted)
    }

    @Test
    fun openCameraDoesNotChangePureUiState() {
        val result = RadioReducer.reduce(initialState, RadioAction.OpenCamera)

        assertEquals(initialState, result)
    }
}
