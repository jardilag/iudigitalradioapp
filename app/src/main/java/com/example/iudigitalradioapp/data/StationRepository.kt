package com.example.iudigitalradioapp.data

import com.example.iudigitalradioapp.model.Station

/**
 * Rol responsable en la simulación: Luisa Gomez.
 *
 * Mantiene una única colección inicial de emisoras para evitar que cada
 * pantalla defina su propia lista. Jorge Echavarría completó [Station.streamUrl]
 * con fuentes HTTPS oficiales durante la integración del reproductor.
 */
object StationRepository {

    val stations: List<Station> = listOf(
        Station(
            id = "wkdu",
            name = "WKDU Philadelphia 91.7 FM",
            description = "Radio universitaria - Drexel University",
            streamUrl = "https://streams.wkdu.org/listen.mp3"
        ),
        Station(
            id = "kexp",
            name = "KEXP",
            description = "Música alternativa e independiente",
            streamUrl = "https://kexp.streamguys1.com/kexp160.aac"
        ),
        Station(
            id = "nucrooze",
            name = "NUCROOZE Radio",
            description = "Jazz, soul y funk",
            streamUrl = "https://stream.nucrooze.com/listen/nucrooze/radio.mp3"
        ),
        Station(
            id = "groove-salad",
            name = "Groove Salad",
            description = "Ambient y downtempo",
            streamUrl = "https://ice5.somafm.com/groovesalad-128-mp3"
        ),
        Station(
            id = "indie-pop",
            name = "Indie Pop Rocks!",
            description = "Indie y pop alternativo",
            streamUrl = "https://ice5.somafm.com/indiepop-128-mp3"
        )
    )
}
