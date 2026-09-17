package com.example.iudigitalradioapp.data

import com.example.iudigitalradioapp.model.Station

object StationRepository {

    val stations = listOf(
        Station(
            id = "station-1",
            name = "Emisora 1",
            description = "Música y entretenimiento",
            streamUrl = ""
        ),
        Station(
            id = "station-2",
            name = "Emisora 2",
            description = "Noticias y actualidad",
            streamUrl = ""
        ),
        Station(
            id = "station-3",
            name = "Emisora 3",
            description = "Programación universitaria",
            streamUrl = ""
        )
    )
}