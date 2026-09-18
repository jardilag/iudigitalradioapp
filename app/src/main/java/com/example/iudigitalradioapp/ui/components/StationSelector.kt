package com.example.iudigitalradioapp.ui.components

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.FilterChip
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.example.iudigitalradioapp.model.Station

/**
 * Rol responsable en la simulación: Juan Pablo Gonzalez.
 *
 * Presenta las cinco emisoras en una cuadrícula de dos columnas para que el
 * usuario pueda verlas sin desplazarse horizontalmente. Devuelve únicamente
 * el identificador seleccionado y no modifica el repositorio.
 */
@Composable
fun StationSelector(
    stations: List<Station>,
    selectedStationId: String?,
    onStationSelected: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "Explorar emisoras",
            style = MaterialTheme.typography.titleMedium
        )

        if (stations.isEmpty()) {
            Text(
                text = "No hay emisoras disponibles.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        } else {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                stations.chunked(2).forEach { stationRow ->
                    if (stationRow.size == 1) {
                        Box(
                            modifier = Modifier.fillMaxWidth(),
                            contentAlignment = Alignment.Center
                        ) {
                            StationChip(
                                station = stationRow.first(),
                                selectedStationId = selectedStationId,
                                onStationSelected = onStationSelected,
                                modifier = Modifier.fillMaxWidth(0.5f)
                            )
                        }
                    } else {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(8.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            stationRow.forEach { station ->
                                StationChip(
                                    station = station,
                                    selectedStationId = selectedStationId,
                                    onStationSelected = onStationSelected,
                                    modifier = Modifier.weight(1f)
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}

/** Botón reutilizable de una emisora dentro de la cuadrícula de Juan Pablo. */
@Composable
private fun StationChip(
    station: Station,
    selectedStationId: String?,
    onStationSelected: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    FilterChip(
        selected = station.id == selectedStationId,
        onClick = {
            onStationSelected(station.id)
        },
        label = {
            Text(text = station.name)
        },
        modifier = modifier
    )
}
