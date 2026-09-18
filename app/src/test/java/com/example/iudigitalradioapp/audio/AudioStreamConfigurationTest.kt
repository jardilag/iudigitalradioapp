package com.example.iudigitalradioapp.audio

import com.example.iudigitalradioapp.data.StationRepository
import java.net.URI
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

/** Pruebas de las fuentes de audio asignadas al rol simulado de Jorge Echavarría. */
class AudioStreamConfigurationTest {

    @Test
    fun allStationsHaveASecureStreamUrl() {
        val streams = StationRepository.stations.map { station ->
            URI(station.streamUrl)
        }

        assertEquals(5, streams.size)
        assertTrue(streams.all { uri ->
            uri.scheme == "https" && !uri.host.isNullOrBlank()
        })
    }
}
