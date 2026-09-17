package com.example.iudigitalradioapp.data

import com.example.iudigitalradioapp.model.Station

/**
 * Rol responsable en la simulación: Luisa Gomez.
 *
 * Mantiene una única colección inicial de emisoras para evitar que cada
 * pantalla defina su propia lista. Las URL se completarán con fuentes HTTPS
 * verificadas durante la integración del reproductor.
 */
object StationRepository {

    val stations: List<Station> = listOf(
        Station(
            id = "wkdu",
            name = "WKDU Philadelphia 91.7 FM",
            description = "Radio universitaria - Drexel University",
            streamUrl = ""
        ),
        Station(
            id = "kexp",
            name = "KEXP",
            description = "Música alternativa e independiente",
            streamUrl = ""
        ),
        Station(
            id = "nucrooze",
            name = "NUCROOZE Radio",
            description = "Jazz, soul y funk",
            streamUrl = ""
        ),
        Station(
            id = "groove-salad",
            name = "Groove Salad",
            description = "Ambient y downtempo",
            streamUrl = ""
        ),
        Station(
            id = "indie-pop",
            name = "Indie Pop Rocks!",
            description = "Indie y pop alternativo",
            streamUrl = ""
        )
    )
}
