package com.example.iudigitalradioapp.ui

import com.example.iudigitalradioapp.data.StationRepository
import com.example.iudigitalradioapp.model.Station

/**
 * Rol responsable en la simulación: Luisa Gomez.
 *
 * Crea un estado coherente al iniciar la aplicación. Recibe la lista como
 * parámetro para permitir pruebas y usa el repositorio como valor predeterminado.
 */
fun createInitialRadioUiState(
    stations: List<Station> = StationRepository.stations
): RadioUiState {
    return RadioUiState(
        stations = stations,
        selectedStationId = stations.firstOrNull()?.id
    )
}
