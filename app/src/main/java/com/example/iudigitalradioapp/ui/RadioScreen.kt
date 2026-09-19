package com.example.iudigitalradioapp.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.ElevatedCard
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.example.iudigitalradioapp.data.StationRepository
import com.example.iudigitalradioapp.ui.components.PhotoPanel
import com.example.iudigitalradioapp.ui.components.PlaybackControls
import com.example.iudigitalradioapp.ui.components.StationSelector
import com.example.iudigitalradioapp.ui.theme.IudigitalradioappTheme

/**
 * Dibuja la pantalla principal a partir de [RadioUiState] y comunica cada
 * interacción mediante [RadioAction]. Al ser una función sin estado propio,
 * puede previsualizarse, probarse y conectarse después con RadioRoute.
 */
@Composable
fun RadioScreen(
    state: RadioUiState,
    onAction: (RadioAction) -> Unit,
    modifier: Modifier = Modifier
) {
    Scaffold(modifier = modifier.fillMaxSize()) { innerPadding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding),
            contentPadding = PaddingValues(horizontal = 20.dp, vertical = 24.dp),
            verticalArrangement = Arrangement.spacedBy(20.dp)
        ) {
            item {
                RadioHeader(isPlaying = state.isPlaying)
            }

            item {
                SelectedStationCard(state = state)
            }

            item {
                StationSelector(
                    stations = state.stations,
                    selectedStationId = state.selectedStationId,
                    onStationSelected = { stationId ->
                        onAction(RadioAction.SelectStation(stationId))
                    }
                )
            }

            item {
                PlaybackControls(
                    hasSelectedStation = state.selectedStation != null,
                    isPlaying = state.isPlaying,
                    isMuted = state.isMuted,
                    onPlayPause = {
                        onAction(
                            if (state.isPlaying) RadioAction.Pause else RadioAction.Play
                        )
                    },
                    onToggleMute = {
                        onAction(RadioAction.ToggleMute)
                    }
                )
            }

            item {
                PhotoPanel(
                    photo = state.capturedPhoto,
                    onOpenCamera = {
                        onAction(RadioAction.OpenCamera)
                    }
                )
            }
        }
    }
}

@Composable
private fun RadioHeader(
    isPlaying: Boolean,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier.fillMaxWidth(),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "IU Digital Radio",
            style = MaterialTheme.typography.headlineMedium,
            fontWeight = FontWeight.Bold
        )
        Text(
            text = "Emisoras universitarias, música y actualidad",
            style = MaterialTheme.typography.bodyLarge,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
        Surface(
            color = if (isPlaying) {
                MaterialTheme.colorScheme.tertiaryContainer
            } else {
                MaterialTheme.colorScheme.surfaceVariant
            },
            contentColor = if (isPlaying) {
                MaterialTheme.colorScheme.onTertiaryContainer
            } else {
                MaterialTheme.colorScheme.onSurfaceVariant
            },
            shape = MaterialTheme.shapes.extraLarge
        ) {
            Text(
                text = if (isPlaying) "EN REPRODUCCIÓN" else "EN PAUSA",
                modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                style = MaterialTheme.typography.labelMedium,
                fontWeight = FontWeight.Bold
            )
        }
    }
}

@Composable
private fun SelectedStationCard(
    state: RadioUiState,
    modifier: Modifier = Modifier
) {
    val station = state.selectedStation

    ElevatedCard(modifier = modifier.fillMaxWidth()) {
        Column(
            modifier = Modifier.padding(20.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            Text(
                text = "Emisora seleccionada",
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.primary
            )
            Text(
                text = station?.name ?: "Selecciona una emisora",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold
            )
            Text(
                text = station?.description
                    ?: "El catálogo no contiene una selección disponible.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

@Preview(showBackground = true, widthDp = 390, heightDp = 844)
@Composable
private fun RadioScreenPreview() {
    IudigitalradioappTheme(dynamicColor = false) {
        RadioScreen(
            state = createInitialRadioUiState(StationRepository.stations),
            onAction = {}
        )
    }
}
