package com.example.iudigitalradioapp.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

/** Pruebas del módulo asignado al rol simulado de Luisa Gomez. */
class StationRepositoryTest {

    @Test
    fun stationIdsAreUnique() {
        val ids = StationRepository.stations.map { station -> station.id }

        assertEquals(ids.size, ids.distinct().size)
    }

    @Test
    fun stationRequiredFieldsAreNotBlank() {
        val allRequiredFieldsAreValid = StationRepository.stations.all { station ->
            station.id.isNotBlank() &&
                station.name.isNotBlank() &&
                station.description.isNotBlank()
        }

        assertTrue(allRequiredFieldsAreValid)
    }
}
