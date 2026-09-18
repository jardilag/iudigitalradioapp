package com.example.iudigitalradioapp.integration

import com.example.iudigitalradioapp.audio.AudioActionHandler
import com.example.iudigitalradioapp.audio.RadioPlayer
import com.example.iudigitalradioapp.model.Station
import com.example.iudigitalradioapp.ui.RadioAction
import com.example.iudigitalradioapp.ui.createInitialRadioUiState
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

/** Pruebas de integración del rol simulado de Yeison Padron. */
class FinalRadioFlowTest {

    private val stations = listOf(
        Station("one", "Emisora uno", "Primera fuente", "https://example.com/one.mp3"),
        Station("two", "Emisora dos", "Segunda fuente", "https://example.com/two.aac")
    )

    @Test
    fun stationPlaybackMuteAndPauseRemainSynchronized() {
        val fakePlayer = RecordingRadioPlayer()
        val handler = AudioActionHandler(fakePlayer)
        var state = createInitialRadioUiState(stations).copy(isPlaying = true)

        state = handler.handle(state, RadioAction.SelectStation("two"))

        assertEquals("two", state.selectedStationId)
        assertFalse(state.isPlaying)
        assertEquals(1, fakePlayer.pauseCount)

        state = handler.handle(state, RadioAction.Play)

        assertEquals("https://example.com/two.aac", fakePlayer.playedUrl)
        assertTrue(state.isPlaying)

        state = handler.handle(state, RadioAction.ToggleMute)

        assertTrue(fakePlayer.mutedValue)
        assertTrue(state.isMuted)

        state = handler.handle(state, RadioAction.Pause)

        assertEquals(2, fakePlayer.pauseCount)
        assertFalse(state.isPlaying)
    }

    private class RecordingRadioPlayer : RadioPlayer {
        var playedUrl: String? = null
        var pauseCount: Int = 0
        var mutedValue: Boolean = false

        override fun play(streamUrl: String) {
            playedUrl = streamUrl
        }

        override fun pause() {
            pauseCount += 1
        }

        override fun setMuted(isMuted: Boolean) {
            mutedValue = isMuted
        }

        override fun release() = Unit
    }
}
