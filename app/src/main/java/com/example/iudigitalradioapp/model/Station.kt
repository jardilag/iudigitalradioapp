package com.example.iudigitalradioapp.model

/**
 * Rol responsable en la simulación: Luisa Gomez.
 *
 * Representa una emisora disponible en el catálogo. La interfaz usa sus datos
 * para mostrar la selección y el reproductor utiliza [streamUrl] como fuente.
 */
data class Station(
    val id: String,
    val name: String,
    val description: String,
    val streamUrl: String
)
