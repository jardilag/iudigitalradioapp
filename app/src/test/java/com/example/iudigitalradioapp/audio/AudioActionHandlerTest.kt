package com.example.iudigitalradioapp.audio

import com.example.iudigitalradioapp.model.Station
import com.example.iudigitalradioapp.ui.RadioAction
import com.example.iudigitalradioapp.ui.createInitialRadioUiState
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class AudioActionHandlerTest {

    private val stations = listOf(
        Station("one", "Emisora uno", "Descripción", "https://example.com/one.mp3"),
        Station("two", "Emisora dos", "Descripción", "https://example.com/two.aac")
    )
    private val fakePlayer = FakeRadioPlayer()
    private val handler = AudioActionHandler(fakePlayer)

    @Test
    fun playUsesTheSelectedStationStreamAndUpdatesState() {
        val result = handler.handle(
            createInitialRadioUiState(stations),
            RadioAction.Play
        )

        assertEquals("https://example.com/one.mp3", fakePlayer.playedUrl)
        assertTrue(result.isPlaying)
    }

    @Test
    fun pauseStopsThePlayerAndUpdatesState() {
        val playingState = createInitialRadioUiState(stations).copy(isPlaying = true)

        val result = handler.handle(playingState, RadioAction.Pause)

        assertTrue(fakePlayer.wasPaused)
        assertFalse(result.isPlaying)
    }

    @Test
    fun toggleMuteSendsTheNextVolumeState() {
        val result = handler.handle(
            createInitialRadioUiState(stations),
            RadioAction.ToggleMute
        )

        assertTrue(fakePlayer.mutedValue)
        assertTrue(result.isMuted)
    }

    @Test
    fun selectingAnotherStationPausesCurrentAudio() {
        val result = handler.handle(
            createInitialRadioUiState(stations).copy(isPlaying = true),
            RadioAction.SelectStation("two")
        )

        assertTrue(fakePlayer.wasPaused)
        assertEquals("two", result.selectedStationId)
        assertFalse(result.isPlaying)
    }

    private class FakeRadioPlayer : RadioPlayer {
        var playedUrl: String? = null
        var wasPaused: Boolean = false
        var mutedValue: Boolean = false

        override fun play(streamUrl: String) {
            playedUrl = streamUrl
        }

        override fun pause() {
            wasPaused = true
        }

        override fun setMuted(isMuted: Boolean) {
            mutedValue = isMuted
        }

        override fun release() = Unit
    }
}
